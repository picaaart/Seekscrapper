#!/usr/bin/env python3
"""
Trends Tracker
Capture monthly aggregations before deleting old jobs
Track seasonality, hiring patterns, and market trends
"""

import csv
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class TrendsTracker:
    """Track monthly trends from job data"""

    def __init__(self, jobs_csv_file: str, output_dir: str = "data"):
        self.jobs_csv_file = jobs_csv_file
        self.output_dir = output_dir
        self.trends_file = os.path.join(output_dir, "monthly_trends.json")

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
            logger.info(f"Loaded {len(jobs)} jobs for trend analysis")
            return jobs
        except Exception as e:
            logger.error(f"Error loading jobs: {e}")
            return []

    def extract_month(self, scraped_at: str) -> str:
        """Extract month from scraped_at timestamp (YYYY-MM)"""
        try:
            dt = datetime.strptime(scraped_at, '%Y-%m-%d %H:%M:%S')
            return dt.strftime('%Y-%m')
        except:
            return None

    def aggregate_monthly_trends(self, jobs):
        """Aggregate data by month"""
        trends = defaultdict(lambda: {
            'total_jobs': 0,
            'categories': defaultdict(int),
            'states': defaultdict(int),
            'companies': set(),
            'salaries': [],
            'avg_salary': 'N/A'
        })

        for job in jobs:
            month = self.extract_month(job.get('scraped_at', ''))
            if not month:
                continue

            month_data = trends[month]
            month_data['total_jobs'] += 1

            # Track by category
            category = job.get('job_category', 'N/A')
            if category != 'N/A':
                month_data['categories'][category] += 1

            # Track by state
            state = job.get('state', 'N/A')
            if state != 'N/A':
                month_data['states'][state] += 1

            # Track companies
            company = job.get('company', 'N/A')
            if company != 'N/A':
                month_data['companies'].add(company)

            # Track salaries
            salary = job.get('salary', 'N/A')
            if salary != 'N/A' and salary:
                try:
                    import re
                    numbers = re.findall(r'\d+', salary.replace(',', ''))
                    if numbers:
                        month_data['salaries'].append(int(numbers[0]))
                except:
                    pass

        # Calculate averages and convert sets to lists
        for month, data in trends.items():
            if data['salaries']:
                avg = int(sum(data['salaries']) / len(data['salaries']))
                data['avg_salary'] = f"${avg:,}"

            data['categories'] = dict(data['categories'])
            data['states'] = dict(data['states'])
            data['unique_companies'] = len(data['companies'])
            del data['companies']
            del data['salaries']

        return dict(sorted(trends.items()))

    def load_existing_trends(self):
        """Load existing trends from JSON"""
        if os.path.exists(self.trends_file):
            try:
                with open(self.trends_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load existing trends: {e}")
        return {}

    def merge_trends(self, existing_trends: dict, new_monthly_trends: dict):
        """Merge new monthly trends with existing ones"""
        merged = existing_trends.copy()

        for month, new_data in new_monthly_trends.items():
            if month in merged:
                # Aggregate with existing data
                old_data = merged[month]

                # Merge counts
                old_data['total_jobs'] = max(old_data['total_jobs'], new_data['total_jobs'])

                # Merge categories
                for cat, count in new_data['categories'].items():
                    old_data['categories'][cat] = max(
                        old_data['categories'].get(cat, 0),
                        count
                    )

                # Merge states
                for state, count in new_data['states'].items():
                    old_data['states'][state] = max(
                        old_data['states'].get(state, 0),
                        count
                    )

                # Update company count
                old_data['unique_companies'] = max(
                    old_data['unique_companies'],
                    new_data['unique_companies']
                )

                # Keep latest salary
                if new_data['avg_salary'] != 'N/A':
                    old_data['avg_salary'] = new_data['avg_salary']
            else:
                merged[month] = new_data

        return merged

    def save_trends(self, trends: dict):
        """Save trends to JSON file"""
        try:
            with open(self.trends_file, 'w') as f:
                json.dump(trends, f, indent=2)
            logger.info(f"✓ Saved trends for {len(trends)} months")
        except Exception as e:
            logger.error(f"Error saving trends: {e}")

    def generate_csv_report(self, trends: dict):
        """Generate a CSV report from trends for easier viewing"""
        csv_file = os.path.join(self.output_dir, "monthly_trends.csv")

        try:
            rows = []
            for month in sorted(trends.keys()):
                data = trends[month]

                # Get top 3 categories
                top_cats = sorted(
                    data['categories'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]
                top_categories = ', '.join([f"{cat}({count})" for cat, count in top_cats])

                # Get top 3 states
                top_states = sorted(
                    data['states'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]
                top_state_str = ', '.join([f"{state}({count})" for state, count in top_states])

                rows.append({
                    'month': month,
                    'total_jobs': data['total_jobs'],
                    'avg_salary': data['avg_salary'],
                    'unique_companies': data['unique_companies'],
                    'top_categories': top_categories,
                    'top_states': top_state_str
                })

            # Write CSV
            if rows:
                with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                    writer.writeheader()
                    writer.writerows(rows)
                logger.info(f"✓ Generated monthly trends report: {csv_file}")

        except Exception as e:
            logger.error(f"Error generating CSV report: {e}")

    def track_trends(self):
        """Main method to track trends"""
        logger.info("Tracking monthly trends...")

        # Load jobs
        jobs = self.load_jobs()
        if not jobs:
            logger.warning("No jobs to analyze for trends")
            return

        # Aggregate monthly trends
        new_trends = self.aggregate_monthly_trends(jobs)

        # Load and merge with existing trends
        existing_trends = self.load_existing_trends()
        merged_trends = self.merge_trends(existing_trends, new_trends)

        # Save merged trends
        self.save_trends(merged_trends)

        # Generate CSV report
        self.generate_csv_report(merged_trends)

        logger.info("✓ Trends tracking complete")


# Usage example
if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    jobs_file = sys.argv[1] if len(sys.argv) > 1 else "data/jobs_australia_current.csv"
    tracker = TrendsTracker(jobs_file)
    tracker.track_trends()
