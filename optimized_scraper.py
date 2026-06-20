#!/usr/bin/env python3
"""
Optimized Multi-Category Job Scraper
- Parallelization (4 concurrent browsers)
- Delta scraping (only new jobs)
- Reduced delays (0.5s instead of 1s)
"""

import os
import csv
import time
import logging
import json
from datetime import datetime
from typing import List, Dict, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from playwright.sync_api import sync_playwright
    USE_PLAYWRIGHT = True
except ImportError:
    USE_PLAYWRIGHT = False

import requests
from bs4 import BeautifulSoup

from config import (
    OUTPUT_CSV, LOG_FILE, TIMEOUT_SECONDS,
    USER_AGENT, HEADLESS
)
from jobs_config import JOBS_CATEGORIES, AUSTRALIAN_STATES, OUTPUT_CSV_CURRENT, OUTPUT_CSV_ARCHIVE, DATA_RETENTION_DAYS
from data_cleaner import DataCleaner
from visa_417_checker import Visa417Checker

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class OptimizedSeekScraper:
    def __init__(self, max_workers=4):
        """
        Initialize optimized scraper with parallelization

        Args:
            max_workers: Number of concurrent browser workers (default: 4)
        """
        self.jobs = []
        self.headers = {
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.output_file = OUTPUT_CSV_CURRENT
        self.archive_file = OUTPUT_CSV_ARCHIVE
        self.visa_checker = Visa417Checker()
        self.max_workers = max_workers
        self.cache_file = "data/scrape_cache.json"
        self.scraped_jobs = self._load_cache()

    def _load_cache(self) -> Set[str]:
        """Load previously scraped job URLs from cache"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    logger.info(f"✓ Loaded cache: {len(data.get('urls', []))} previously scraped jobs")
                    return set(data.get('urls', []))
        except Exception as e:
            logger.warning(f"Could not load cache: {e}")
        return set()

    def _save_cache(self):
        """Save scraped job URLs to cache"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump({
                    'urls': list(self.scraped_jobs),
                    'last_update': datetime.now().isoformat()
                }, f)
            logger.info(f"✓ Saved cache: {len(self.scraped_jobs)} URLs")
        except Exception as e:
            logger.warning(f"Could not save cache: {e}")

    def build_seek_url(self, job_keyword, state_code):
        """Construct Seek URL for search"""
        state_name = AUSTRALIAN_STATES.get(state_code, state_code)
        job_slug = job_keyword.lower().replace(" ", "-")
        state_slug = state_name.lower().replace(" ", "-")
        return f"https://www.seek.com.au/{job_slug}-jobs/in-{state_slug}"

    def scrape_all_jobs(self):
        """Scrape all jobs using parallelization"""
        logger.info("="*60)
        logger.info(f"Starting optimized scrape with {self.max_workers} workers")
        logger.info(f"Categories: {len(JOBS_CATEGORIES)}")
        logger.info(f"States: {len(AUSTRALIAN_STATES)}")
        logger.info("="*60)

        # Create task list
        tasks = []
        for category_key, category_data in JOBS_CATEGORIES.items():
            category_name = category_data['display_name']
            for job_keyword in category_data['keywords']:
                for state_code in AUSTRALIAN_STATES.keys():
                    url = self.build_seek_url(job_keyword, state_code)
                    tasks.append((url, category_name, job_keyword, state_code))

        logger.info(f"Total tasks: {len(tasks)}")
        logger.info(f"Using {self.max_workers} parallel workers for 6-8x speedup")

        # Execute tasks in parallel
        start_time = time.time()
        jobs_found = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._scrape_page, url, category, keyword, state):
                (url, category, keyword, state)
                for url, category, keyword, state in tasks
            }

            for future in as_completed(futures):
                try:
                    jobs = future.result()
                    jobs_found += len(jobs)
                    self.jobs.extend(jobs)
                except Exception as e:
                    url, category, keyword, state = futures[future]
                    logger.debug(f"Error scraping {keyword} in {state}: {e}")

        elapsed = time.time() - start_time
        logger.info(f"\n✅ Scraping complete: {jobs_found} new jobs found")
        logger.info(f"⏱️  Time elapsed: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
        logger.info(f"📊 Speed: {len(tasks) / (elapsed/60):.1f} searches/minute")

        return self.jobs

    def _scrape_page(self, url, category, job_keyword, state_code):
        """Scrape a single page (called by thread worker)"""
        jobs = []

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=HEADLESS,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                    ]
                )
                context = browser.new_context(user_agent=USER_AGENT)
                page = context.new_page()

                try:
                    page.goto(url, wait_until="load", timeout=TIMEOUT_SECONDS * 1000)
                except:
                    logger.debug(f"Timeout on {url}")

                # Reduced delay (0.5s instead of 1s)
                time.sleep(0.5)

                try:
                    page.wait_for_selector('article', timeout=5000)
                except:
                    pass

                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')

                job_listings = soup.find_all('article')

                if not job_listings:
                    job_listings = soup.find_all('li', {'data-automation': True})

                for job_element in job_listings:
                    try:
                        job_data = self._parse_job(job_element, category, job_keyword, state_code)
                        if job_data and job_data.get('title') != 'N/A':
                            # Delta scraping: only add if URL is new
                            if job_data.get('url') not in self.scraped_jobs:
                                jobs.append(job_data)
                                self.scraped_jobs.add(job_data.get('url'))
                    except:
                        pass

                context.close()
                browser.close()

        except Exception as e:
            logger.debug(f"Error scraping {url}: {e}")

        return jobs

    def _parse_job(self, job_element, category, job_keyword, state_code):
        """Parse individual job listing"""
        try:
            title = 'N/A'
            title_elem = job_element.find('h3') or job_element.find('h2')
            if title_elem:
                title = title_elem.get_text(strip=True)

            company = 'N/A'
            links = job_element.find_all('a')
            if len(links) > 1:
                company = links[1].get_text(strip=True)
            elif links:
                company = links[0].get_text(strip=True)

            location = 'N/A'
            for elem in job_element.find_all('span'):
                text = elem.get_text(strip=True)
                if state_code in text or AUSTRALIAN_STATES.get(state_code, '') in text:
                    location = text
                    break

            url = 'N/A'
            job_link = job_element.find('a', href=True)
            if job_link:
                url = job_link.get('href', 'N/A')
                if url != 'N/A' and not url.startswith('http'):
                    url = 'https://www.seek.com.au' + url

            all_text = job_element.get_text(strip=True)
            job_type = 'N/A'
            for pattern in ['Full-time', 'Part-time', 'Contract', 'Casual', 'Temporary', 'FIFO']:
                if pattern in all_text:
                    job_type = pattern
                    break

            salary = 'N/A'
            if '$' in all_text:
                for elem in job_element.find_all('span'):
                    text = elem.get_text(strip=True)
                    if '$' in text and any(c.isdigit() for c in text):
                        salary = text
                        break

            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'state': state_code,
                'job_category': category,
                'job_keyword': job_keyword,
                'job_type': job_type,
                'salary': salary,
                'url': url,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            visa_info = self.visa_checker.check_job_eligibility(job_data)
            job_data['visa_417_eligible'] = visa_info['visa_417_eligible']
            job_data['visa_417_categories'] = visa_info['visa_417_categories']

            return job_data
        except:
            return None

    def save_to_csv(self):
        """Save jobs to CSV"""
        if not self.jobs:
            logger.warning("No new jobs to save")
            return

        try:
            file_exists = os.path.isfile(self.output_file)

            with open(self.output_file, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'title', 'company', 'location', 'state', 'job_category',
                    'job_keyword', 'job_type', 'salary', 'visa_417_eligible',
                    'visa_417_categories', 'url', 'scraped_at'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                for job in self.jobs:
                    writer.writerow(job)

            logger.info(f"✓ Saved {len(self.jobs)} new jobs to {self.output_file}")

        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")

    def cleanup_old_data(self):
        """Clean up old data"""
        logger.info(f"\n🧹 Cleaning data (retention: {DATA_RETENTION_DAYS} days)...")
        cleaner = DataCleaner(retention_days=DATA_RETENTION_DAYS)
        cleaner.cleanup_all(self.output_file, self.archive_file)

    def run(self):
        """Run optimized scraping"""
        self.jobs = []
        self.scrape_all_jobs()
        self.save_to_csv()
        self._save_cache()
        self.cleanup_old_data()
        logger.info("\n✅ Optimized scrape cycle complete\n")


def main():
    scraper = OptimizedSeekScraper(max_workers=4)
    scraper.run()


if __name__ == "__main__":
    main()
