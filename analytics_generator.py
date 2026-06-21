#!/usr/bin/env python3
"""
Analytics Generator
Generate statistics from job data for backpackers
Creates multiple CSV files with insights
"""

import csv
import os
from collections import defaultdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AnalyticsGenerator:
    """Generate analytics from scraped job data"""

    def __init__(self, jobs_csv_file: str, output_dir: str = "data"):
        self.jobs_csv_file = jobs_csv_file
        self.output_dir = output_dir
        self.company_stats = defaultdict(lambda: {
            'count': 0,
            'salaries': [],
            'last_posted': None,
            'locations': set(),
            'categories': set()
        })
        self.location_stats = defaultdict(lambda: {
            'count': 0,
            'salaries': [],
            'last_posted': None,
            'categories': defaultdict(int)
        })
        self.category_stats = defaultdict(lambda: {
            'count': 0,
            'salaries': [],
            'companies': set(),
            'states': defaultdict(int)
        })

    def load_jobs(self):
        """Load jobs from CSV"""
        if not os.path.exists(self.jobs_csv_file):
            logger.warning(f"Jobs file not found: {self.jobs_csv_file}")
            return []

        jobs = []
        try:
            with open(self.jobs_csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('title') != 'N/A':
                        jobs.append(row)
            logger.info(f"Loaded {len(jobs)} jobs")
            return jobs
        except Exception as e:
            logger.error(f"Error loading jobs: {e}")
            return []

    def generate_company_stats(self, jobs):
        """Generate company statistics"""
        for job in jobs:
            company = job.get('company', 'N/A')
            if company == 'N/A':
                continue

            state = job.get('state', 'N/A')
            location = job.get('location', 'N/A')
            salary = job.get('salary', 'N/A')
            category = job.get('job_category', 'N/A')
            scraped_at = job.get('scraped_at', '')

            key = (company, state)
            stats = self.company_stats[key]

            stats['count'] += 1
            stats['locations'].add(location)
            stats['categories'].add(category)

            # Extract numeric salary if available
            if salary != 'N/A' and salary:
                try:
                    # Try to extract first number from salary string
                    import re
                    numbers = re.findall(r'\d+', salary.replace(',', ''))
                    if numbers:
                        stats['salaries'].append(int(numbers[0]))
                except:
                    pass

            # Update last posted
            if scraped_at:
                stats['last_posted'] = scraped_at

        # Convert to CSV format
        rows = []
        for (company, state), stats in sorted(self.company_stats.items()):
            avg_salary = 'N/A'
            if stats['salaries']:
                avg_salary = f"${int(sum(stats['salaries']) / len(stats['salaries'])):,}"

            rows.append({
                'company': company,
                'state': state,
                'locations': '|'.join(sorted(stats['locations'])),
                'job_categories': '|'.join(sorted(stats['categories'])),
                'total_jobs': stats['count'],
                'avg_salary': avg_salary,
                'last_posted': stats['last_posted'] or 'N/A'
            })

        return rows

    def generate_location_stats(self, jobs):
        """Generate location statistics"""
        for job in jobs:
            state = job.get('state', 'N/A')
            location = job.get('location', 'N/A')
            category = job.get('job_category', 'N/A')
            salary = job.get('salary', 'N/A')
            scraped_at = job.get('scraped_at', '')

            if state == 'N/A' or location == 'N/A':
                continue

            key = (state, location)
            stats = self.location_stats[key]

            stats['count'] += 1
            stats['categories'][category] += 1

            if salary != 'N/A' and salary:
                try:
                    import re
                    numbers = re.findall(r'\d+', salary.replace(',', ''))
                    if numbers:
                        stats['salaries'].append(int(numbers[0]))
                except:
                    pass

            if scraped_at:
                stats['last_posted'] = scraped_at

        # Convert to CSV format
        rows = []
        for (state, location), stats in sorted(self.location_stats.items()):
            avg_salary = 'N/A'
            if stats['salaries']:
                avg_salary = f"${int(sum(stats['salaries']) / len(stats['salaries'])):,}"

            top_category = max(stats['categories'].items(), key=lambda x: x[1])[0] if stats['categories'] else 'N/A'

            rows.append({
                'state': state,
                'location': location,
                'total_jobs': stats['count'],
                'top_category': top_category,
                'avg_salary': avg_salary,
                'last_posted': stats['last_posted'] or 'N/A'
            })

        return rows

    def generate_category_stats(self, jobs):
        """Generate job category statistics"""
        for job in jobs:
            category = job.get('job_category', 'N/A')
            state = job.get('state', 'N/A')
            company = job.get('company', 'N/A')
            salary = job.get('salary', 'N/A')

            if category == 'N/A':
                continue

            stats = self.category_stats[category]
            stats['count'] += 1
            stats['states'][state] += 1
            if company != 'N/A':
                stats['companies'].add(company)

            if salary != 'N/A' and salary:
                try:
                    import re
                    numbers = re.findall(r'\d+', salary.replace(',', ''))
                    if numbers:
                        stats['salaries'].append(int(numbers[0]))
                except:
                    pass

        # Convert to CSV format
        rows = []
        for category, stats in sorted(self.category_stats.items()):
            avg_salary = 'N/A'
            if stats['salaries']:
                avg_salary = f"${int(sum(stats['salaries']) / len(stats['salaries'])):,}"

            top_state = max(stats['states'].items(), key=lambda x: x[1])[0] if stats['states'] else 'N/A'
            demand = 'HIGH' if stats['count'] > 1000 else 'MEDIUM' if stats['count'] > 500 else 'LOW'

            rows.append({
                'job_category': category,
                'total_jobs': stats['count'],
                'avg_salary': avg_salary,
                'unique_companies': len(stats['companies']),
                'top_state': top_state,
                'demand_level': demand
            })

        return rows

    def save_csv(self, rows: list, filename: str):
        """Save rows to CSV file"""
        if not rows:
            logger.warning(f"No data to save for {filename}")
            return

        filepath = os.path.join(self.output_dir, filename)

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            logger.info(f"✓ Saved {len(rows)} rows to {filename}")
        except Exception as e:
            logger.error(f"Error saving {filename}: {e}")

    def generate_all(self):
        """Generate all analytics"""
        logger.info("Generating analytics...")

        # Load jobs
        jobs = self.load_jobs()
        if not jobs:
            logger.warning("No jobs to analyze")
            return

        # Generate statistics
        logger.info("Generating company statistics...")
        company_rows = self.generate_company_stats(jobs)
        self.save_csv(company_rows, 'company_stats.csv')

        logger.info("Generating location statistics...")
        location_rows = self.generate_location_stats(jobs)
        self.save_csv(location_rows, 'location_stats.csv')

        logger.info("Generating category statistics...")
        category_rows = self.generate_category_stats(jobs)
        self.save_csv(category_rows, 'category_stats.csv')

        logger.info("✓ Analytics generation complete")


# Usage example
if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    jobs_file = sys.argv[1] if len(sys.argv) > 1 else "data/jobs_australia_current.csv"
    generator = AnalyticsGenerator(jobs_file)
    generator.generate_all()
