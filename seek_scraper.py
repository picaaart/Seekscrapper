#!/usr/bin/env python3
"""
Seek.com.au Labourer Job Scraper
Scrape labourer jobs in Queensland and save to CSV
"""

import os
import csv
import json
from datetime import datetime
from typing import List, Dict
import time
import logging

try:
    from playwright.sync_api import sync_playwright
    USE_PLAYWRIGHT = True
except ImportError:
    USE_PLAYWRIGHT = False

import requests
from bs4 import BeautifulSoup

try:
    from google_drive_sync import GoogleDriveSync
    HAS_GOOGLE_DRIVE = True
except ImportError:
    HAS_GOOGLE_DRIVE = False

from config import (
    OUTPUT_CSV, LOG_FILE, SEEK_URL, TIMEOUT_SECONDS,
    USER_AGENT, HEADLESS, SCRAPE_INTERVAL_HOURS,
    ENABLE_GOOGLE_DRIVE, GOOGLE_DRIVE_FOLDER_NAME,
    GOOGLE_CREDENTIALS_FILE, GOOGLE_TOKEN_FILE
)

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


class SeekScraper:
    def __init__(self):
        self.base_url = SEEK_URL
        self.jobs = []
        self.headers = {
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.output_file = OUTPUT_CSV

    def scrape_jobs(self) -> List[Dict]:
        """
        Scrape jobs from Seek.com.au using Playwright
        """
        logger.info(f"Scraping labourer jobs from Queensland...")

        if USE_PLAYWRIGHT:
            return self._scrape_with_playwright()
        else:
            return self._scrape_with_requests()

    def _scrape_with_playwright(self) -> List[Dict]:
        """Use Playwright to render JavaScript and bypass protections"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=HEADLESS,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-first-run',
                        '--no-default-browser-check',
                    ]
                )
                context = browser.new_context(user_agent=USER_AGENT)
                page = context.new_page()

                logger.info("Loading page with browser...")
                try:
                    page.goto(self.base_url, wait_until="load", timeout=TIMEOUT_SECONDS * 1000)
                except:
                    logger.warning("Timeout on load, proceeding anyway...")

                # Wait for Cloudflare and content to load
                time.sleep(5)

                # Try to wait for job listings to appear
                try:
                    page.wait_for_selector('article', timeout=10000)
                except:
                    logger.debug("No articles found with wait_for_selector")

                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')

                # Find job listings
                job_listings = soup.find_all('article')

                if not job_listings:
                    job_listings = soup.find_all('li', {'data-automation': True})

                if not job_listings:
                    job_listings = soup.find_all('div', {'data-testid': lambda x: x and 'job' in str(x).lower()})

                if not job_listings:
                    logger.warning("No job listings found. Structure may have changed.")

                for job in job_listings:
                    try:
                        job_data = self._parse_job(job)
                        if job_data and job_data.get('title') != 'N/A':
                            self.jobs.append(job_data)
                    except Exception:
                        pass

                context.close()
                browser.close()
                logger.info(f"Found {len(self.jobs)} jobs with data")
                return self.jobs

        except Exception as e:
            logger.error(f"Error with Playwright: {e}", exc_info=True)
            return []

    def _scrape_with_requests(self) -> List[Dict]:
        """Fallback to requests if Playwright not available"""
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            job_listings = soup.find_all('article', {'data-card-type': 'JobCard'})

            if not job_listings:
                logger.warning("No job listings found. HTML structure may have changed.")
                return []

            for job in job_listings:
                try:
                    job_data = self._parse_job(job)
                    if job_data:
                        self.jobs.append(job_data)
                except Exception:
                    pass

            logger.info(f"Found {len(self.jobs)} jobs")
            return self.jobs

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            return []

    def _parse_job(self, job_element) -> Dict:
        """
        Parse individual job listing - flexible approach
        """
        try:
            # Try multiple ways to get title
            title = 'N/A'
            title_elem = job_element.find('h3') or job_element.find('h2')
            if title_elem:
                title = title_elem.get_text(strip=True)
            else:
                for elem in job_element.find_all(['a', 'div']):
                    text = elem.get_text(strip=True)
                    if len(text) > 5 and len(text) < 200:
                        title = text
                        break

            # Try to get all links and text
            company = 'N/A'
            links = job_element.find_all('a')
            if len(links) > 1:
                company = links[1].get_text(strip=True)
            elif links:
                company = links[0].get_text(strip=True)

            # Try to get location
            location = 'N/A'
            location_elem = job_element.find('span', class_=lambda x: x and 'location' in str(x).lower())
            if location_elem:
                location = location_elem.get_text(strip=True)
            else:
                for elem in job_element.find_all('span'):
                    text = elem.get_text(strip=True)
                    if any(state in text for state in ['Queensland', 'QLD', 'Brisbane', 'Gold Coast']):
                        location = text
                        break

            # Get URL
            url = 'N/A'
            job_link = job_element.find('a', href=True)
            if job_link:
                url = job_link.get('href', 'N/A')
                if url != 'N/A' and not url.startswith('http'):
                    url = 'https://www.seek.com.au' + url

            # Get job type and salary
            all_text = job_element.get_text(strip=True)
            job_type = 'N/A'
            salary = 'N/A'

            for pattern in ['Full-time', 'Part-time', 'Contract', 'Casual', 'Temporary']:
                if pattern in all_text:
                    job_type = pattern
                    break

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
                'job_type': job_type,
                'salary': salary,
                'url': url,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception:
            return None

    def save_to_csv(self):
        """
        Save jobs to CSV file and sync to Google Drive
        """
        if not self.jobs:
            logger.warning("No jobs to save")
            return

        try:
            file_exists = os.path.isfile(self.output_file)

            with open(self.output_file, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['title', 'company', 'location', 'job_type', 'salary', 'url', 'scraped_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                for job in self.jobs:
                    writer.writerow(job)

            logger.info(f"✓ Saved {len(self.jobs)} jobs to {self.output_file}")

            # Sync to Google Drive if enabled
            if ENABLE_GOOGLE_DRIVE and HAS_GOOGLE_DRIVE:
                self._sync_to_google_drive()

        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")

    def _sync_to_google_drive(self):
        """
        Sync CSV file to Google Drive
        """
        try:
            if not os.path.exists(GOOGLE_CREDENTIALS_FILE):
                logger.warning(f"Google Drive credentials not found. Skipping sync.")
                logger.warning(f"To enable Google Drive sync:")
                logger.warning(f"  1. Visit https://console.cloud.google.com/")
                logger.warning(f"  2. Create OAuth 2.0 credentials (Desktop app)")
                logger.warning(f"  3. Download and save as: {GOOGLE_CREDENTIALS_FILE}")
                return

            logger.info("Syncing to Google Drive...")
            sync = GoogleDriveSync(
                GOOGLE_CREDENTIALS_FILE,
                GOOGLE_TOKEN_FILE,
                GOOGLE_DRIVE_FOLDER_NAME
            )

            if sync.sync(self.output_file):
                logger.info("✓ Google Drive sync successful")
            else:
                logger.warning("✗ Google Drive sync failed")

        except Exception as e:
            logger.warning(f"Google Drive sync error: {e}")

    def run(self):
        """
        Main scraping cycle
        """
        self.jobs = []
        self.scrape_jobs()
        self.save_to_csv()
        logger.info("Scrape cycle complete\n")


def main():
    scraper = SeekScraper()
    scraper.run()


if __name__ == "__main__":
    main()
