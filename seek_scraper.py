#!/usr/bin/env python3
"""
Seek.com.au Multi-Category Job Scraper
Scrape toutes les catégories de jobs, tous les états
"""

import os
import csv
import time
import logging
from datetime import datetime
from typing import List, Dict

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


class MultiCategorySeekScraper:
    def __init__(self):
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

    def build_seek_url(self, job_keyword, state_code):
        """Construit l'URL Seek pour une recherche"""
        state_name = AUSTRALIAN_STATES.get(state_code, state_code)
        # Format: https://www.seek.com.au/job-keyword-jobs/in-state
        job_slug = job_keyword.lower().replace(" ", "-")
        state_slug = state_name.lower().replace(" ", "-")
        return f"https://www.seek.com.au/{job_slug}-jobs/in-{state_slug}"

    def scrape_all_jobs(self):
        """Scrape tous les jobs pour toutes les catégories et états"""
        logger.info("="*60)
        logger.info("Starting multi-category scrape...")
        logger.info(f"Categories: {len(JOBS_CATEGORIES)}")
        logger.info(f"States: {len(AUSTRALIAN_STATES)}")
        logger.info("="*60)

        total_jobs_scraped = 0

        for category_key, category_data in JOBS_CATEGORIES.items():
            category_name = category_data['display_name']
            logger.info(f"\n📂 Category: {category_name}")

            for job_keyword in category_data['keywords']:
                for state_code in AUSTRALIAN_STATES.keys():
                    url = self.build_seek_url(job_keyword, state_code)
                    logger.info(f"  → {job_keyword} in {state_code}...")

                    jobs = self._scrape_page(url, category_name, job_keyword, state_code)
                    total_jobs_scraped += len(jobs)
                    self.jobs.extend(jobs)

                    # Petit delay pour ne pas spammer Seek
                    time.sleep(1)

        logger.info(f"\n✅ Scraping complete: {total_jobs_scraped} jobs found")
        return self.jobs

    def _scrape_page(self, url, category, job_keyword, state_code):
        """Scrape une page Seek spécifique"""
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

                time.sleep(2)

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
                            jobs.append(job_data)
                    except:
                        pass

                context.close()
                browser.close()

        except Exception as e:
            logger.debug(f"Error scraping {url}: {e}")

        return jobs

    def _parse_job(self, job_element, category, job_keyword, state_code):
        """Parse une offre d'emploi"""
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

            return {
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
        except:
            return None

    def save_to_csv(self):
        """Sauvegarde dans le CSV courant"""
        if not self.jobs:
            logger.warning("No jobs to save")
            return

        try:
            file_exists = os.path.isfile(self.output_file)

            with open(self.output_file, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'title', 'company', 'location', 'state', 'job_category',
                    'job_keyword', 'job_type', 'salary', 'url', 'scraped_at'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                for job in self.jobs:
                    writer.writerow(job)

            logger.info(f"✓ Saved {len(self.jobs)} jobs to {self.output_file}")

        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")

    def cleanup_old_data(self):
        """Nettoie les vieilles données"""
        logger.info(f"\n🧹 Cleaning data (retention: {DATA_RETENTION_DAYS} days)...")
        cleaner = DataCleaner(retention_days=DATA_RETENTION_DAYS)
        cleaner.cleanup_all(self.output_file, self.archive_file)

    def run(self):
        """Lance le scraping complet"""
        self.jobs = []
        self.scrape_all_jobs()
        self.save_to_csv()
        self.cleanup_old_data()
        logger.info("\n✅ Scrape cycle complete\n")


def main():
    scraper = MultiCategorySeekScraper()
    scraper.run()


if __name__ == "__main__":
    main()
