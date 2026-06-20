#!/usr/bin/env python3
"""
Seek Scraper Scheduler
Runs the scraper every 2 hours, 24/7
"""

import schedule
import time
import sys
import os
import logging
from datetime import datetime
import subprocess

from config import SCRAPE_INTERVAL_HOURS, LOG_FILE

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


def run_scraper():
    """Execute the scraper script"""
    try:
        logger.info(f"{'='*60}")
        logger.info(f"Starting scraper run")
        logger.info(f"{'='*60}")

        scraper_path = os.path.join(os.path.dirname(__file__), 'seek_scraper.py')
        result = subprocess.run([sys.executable, scraper_path],
                              capture_output=True, text=True)

        if result.stdout:
            logger.info(result.stdout)
        if result.stderr:
            logger.error(f"STDERR: {result.stderr}")

        logger.info(f"Scraper run completed\n")
    except Exception as e:
        logger.error(f"Error running scraper: {e}", exc_info=True)


def main():
    logger.info("Seek Scraper Scheduler started")
    logger.info(f"Scraping every {SCRAPE_INTERVAL_HOURS} hour(s)")

    # Schedule the scraper
    schedule.every(SCRAPE_INTERVAL_HOURS).hours.do(run_scraper)

    # Run first scrape immediately
    run_scraper()

    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Scheduler error: {e}", exc_info=True)
        sys.exit(1)
