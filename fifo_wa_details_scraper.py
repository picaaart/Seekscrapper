#!/usr/bin/env python3
"""
FIFO WA Details Scraper
Scrape full job descriptions for FIFO jobs in WA < 2 hours
Extract certifications and detailed info
"""

import os
import csv
import time
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    pass

from bs4 import BeautifulSoup
from certifications_extractor import CertificationsExtractor
from config import USER_AGENT, HEADLESS, TIMEOUT_SECONDS

logger = logging.getLogger(__name__)


class FIFOWADetailsScraper:
    """Scrape full job details for FIFO jobs in WA (< 2 hours old)"""

    def __init__(self):
        self.output_file = "data/jobs_australia_fifo_wa_details.csv"
        self.scraped_urls = self._load_scraped_urls()

    def _load_scraped_urls(self) -> set:
        """Load URLs already scraped"""
        if os.path.exists(self.output_file):
            try:
                urls = set()
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('url'):
                            urls.add(row['url'])
                logger.info(f"✓ Loaded {len(urls)} previously scraped FIFO WA jobs")
                return urls
            except Exception as e:
                logger.warning(f"Could not load scraped URLs: {e}")
        return set()

    def filter_fifo_wa_recent(self, jobs: List[Dict]) -> List[Dict]:
        """Filter jobs: FIFO category, WA state, < 2 hours old"""
        cutoff_time = datetime.now() - timedelta(hours=2)
        filtered = []

        for job in jobs:
            # Check category
            if job.get('job_category') != 'FIFO / Mines':
                continue

            # Check state
            if job.get('state') != 'WA':
                continue

            # Check age
            try:
                scraped_at = datetime.strptime(
                    job.get('scraped_at', ''),
                    '%Y-%m-%d %H:%M:%S'
                )
                if scraped_at < cutoff_time:
                    continue
            except:
                continue

            # Already scraped?
            if job.get('url') in self.scraped_urls:
                continue

            filtered.append(job)

        logger.info(f"Found {len(filtered)} new FIFO WA jobs (< 2 hours)")
        return filtered

    def scrape_job_details(self, job_url: str) -> Dict:
        """Scrape full job details from job URL"""
        details = {
            'title': 'N/A',
            'company': 'N/A',
            'description': 'N/A',
            'required_certifications': 'N/A',
            'desirable_certifications': 'N/A',
            'experience_required': 'N/A',
        }

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=HEADLESS,
                    args=['--disable-blink-features=AutomationControlled']
                )
                context = browser.new_context(user_agent=USER_AGENT)
                page = context.new_page()

                try:
                    page.goto(job_url, wait_until="load", timeout=TIMEOUT_SECONDS * 1000)
                except:
                    logger.debug(f"Timeout loading {job_url}")
                    context.close()
                    browser.close()
                    return details

                time.sleep(1)

                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')

                # Extract title
                title_elem = soup.find('h1')
                if title_elem:
                    details['title'] = title_elem.get_text(strip=True)

                # Extract company
                company_elem = soup.find('span', {'data-testid': 'job-company-name'})
                if company_elem:
                    details['company'] = company_elem.get_text(strip=True)

                # Extract full description
                description_elem = soup.find('div', {'data-automation': 'jobAdDetails'})
                if not description_elem:
                    # Alternative selectors
                    description_elem = soup.find('div', class_=lambda x: x and 'description' in str(x).lower())

                if description_elem:
                    full_text = description_elem.get_text(strip=True)
                    details['description'] = full_text[:1500]  # First 1500 chars

                    # Extract certifications
                    cert_result = CertificationsExtractor.extract(full_text)
                    details['required_certifications'] = CertificationsExtractor.format_for_csv(cert_result)
                    details['desirable_certifications'] = CertificationsExtractor.format_desirable_for_csv(cert_result)

                    # Extract experience level
                    exp_keywords = {
                        'entry_level': ['entry level', 'no experience', 'graduate', 'junior'],
                        'mid_level': ['3+ years', '5+ years', 'experienced', 'mid-level'],
                        'senior': ['10+ years', 'senior', 'lead', 'manager'],
                    }

                    for level, keywords in exp_keywords.items():
                        if any(kw in full_text.lower() for kw in keywords):
                            details['experience_required'] = level
                            break

                context.close()
                browser.close()

        except Exception as e:
            logger.debug(f"Error scraping details from {job_url}: {e}")

        return details

    def scrape_and_save(self, jobs: List[Dict]):
        """Scrape details for filtered jobs and save to CSV"""
        if not jobs:
            logger.info("No new FIFO WA jobs to scrape details for")
            return

        logger.info(f"Scraping details for {len(jobs)} FIFO WA jobs...")

        file_exists = os.path.isfile(self.output_file)
        saved_count = 0

        with open(self.output_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'title', 'company', 'location', 'state', 'salary',
                'job_type', 'url', 'scraped_at',
                'required_certifications', 'desirable_certifications',
                'experience_required', 'description'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for i, job in enumerate(jobs, 1):
                logger.info(f"  [{i}/{len(jobs)}] Scraping {job.get('title', 'N/A')}...")

                # Scrape details
                details = self.scrape_job_details(job.get('url', ''))

                # Merge with original job data
                row = {
                    'title': job.get('title', 'N/A'),
                    'company': job.get('company', 'N/A'),
                    'location': job.get('location', 'N/A'),
                    'state': job.get('state', 'N/A'),
                    'salary': job.get('salary', 'N/A'),
                    'job_type': job.get('job_type', 'N/A'),
                    'url': job.get('url', 'N/A'),
                    'scraped_at': job.get('scraped_at', 'N/A'),
                    'required_certifications': details['required_certifications'],
                    'desirable_certifications': details['desirable_certifications'],
                    'experience_required': details['experience_required'],
                    'description': details['description']
                }

                writer.writerow(row)
                saved_count += 1
                self.scraped_urls.add(job.get('url'))

                # Small delay between requests
                time.sleep(0.5)

        logger.info(f"✓ Saved details for {saved_count} FIFO WA jobs")

    def run(self, jobs: List[Dict]):
        """Main entry point"""
        filtered_jobs = self.filter_fifo_wa_recent(jobs)
        if filtered_jobs:
            self.scrape_and_save(filtered_jobs)


# Usage
if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Load jobs from CSV
    jobs = []
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "data/jobs_australia_current.csv"

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        jobs = list(reader)

    scraper = FIFOWADetailsScraper()
    scraper.run(jobs)
