#!/usr/bin/env python3
"""
Telegram Alerts
Send job alerts to Telegram channel/group
"""

import requests
import logging
from typing import List, Dict
from telegram_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED

logger = logging.getLogger(__name__)


class TelegramAlerts:
    """Send alerts to Telegram"""

    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.enabled = TELEGRAM_ENABLED

    def send_message(self, message: str) -> bool:
        """
        Send a message to Telegram

        Args:
            message: Message text (supports HTML formatting)

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.debug("Telegram alerts disabled")
            return False

        if not self.token or not self.chat_id:
            logger.warning("Telegram config missing (token or chat_id)")
            return False

        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"

            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML",  # Allow HTML formatting
                "disable_web_page_preview": True
            }

            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                logger.info("✓ Telegram alert sent")
                return True
            else:
                error = response.json().get('description', 'Unknown error')
                logger.warning(f"Telegram error: {error}")
                return False

        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False

    def format_fifo_jobs_by_state(self, jobs: List[Dict]) -> str:
        """
        Format FIFO jobs grouped by state with full details

        Args:
            jobs: List of job dictionaries

        Returns:
            Formatted message string
        """
        if not jobs:
            return "No new FIFO jobs"

        # Group jobs by state
        jobs_by_state = {}
        for job in jobs:
            state = job.get('state', 'N/A')
            if state not in jobs_by_state:
                jobs_by_state[state] = []
            jobs_by_state[state].append(job)

        # Sort states
        sorted_states = sorted(jobs_by_state.keys())

        message = f"🚨 <b>FIFO Jobs Alert</b> ({len(jobs)} new)\n\n"

        for state in sorted_states:
            state_jobs = jobs_by_state[state]
            message += f"<b>📍 {state}</b> ({len(state_jobs)} jobs)\n\n"

            for i, job in enumerate(state_jobs[:3], 1):  # Max 3 per state
                title = job.get('title', 'N/A')
                company = job.get('company', 'N/A')
                location = job.get('location', 'N/A')
                salary = job.get('salary', 'N/A')
                job_type = job.get('job_type', 'N/A')
                url = job.get('url', '#')
                visa_417 = job.get('visa_417_eligible', 'N/A')
                visa_cats = job.get('visa_417_categories', 'N/A')

                # Format visa 417
                visa_text = ""
                if visa_417 == 'Yes':
                    visa_text = f"🇦🇺 Visa 417: ✅ Eligible ({visa_cats})"
                elif visa_417 == 'No':
                    visa_text = "🇦🇺 Visa 417: ❌ Not eligible"

                message += f"""<b>{i}. {title}</b>
🏢 {company} | {location}
💰 {salary} | 🎯 {job_type}

{visa_text}

<a href="{url}">→ Apply Now</a>

"""

            if len(state_jobs) > 3:
                message += f"<i>... and {len(state_jobs) - 3} more in {state}</i>\n"

            message += "\n"

        return message

    def format_salary_report(self, stats: Dict) -> str:
        """Format salary report for Telegram"""
        message = """📊 <b>Weekly Salary Report - FIFO WA</b>

"""
        message += f"💰 Average: {stats.get('avg_salary', 'N/A')}\n"
        message += f"📈 Range: {stats.get('salary_min', 'N/A')} - {stats.get('salary_max', 'N/A')}\n"
        message += f"📌 Jobs posted: {stats.get('total_jobs', 'N/A')}\n"

        return message

    def send_jobs_alert_by_state(self, jobs: List[Dict]) -> bool:
        """Send separate alert for each state"""
        if not jobs:
            return False

        # Group jobs by state
        jobs_by_state = {}
        for job in jobs:
            state = job.get('state', 'N/A')
            if state not in jobs_by_state:
                jobs_by_state[state] = []
            jobs_by_state[state].append(job)

        # Send one message per state
        total_sent = 0
        for state in sorted(jobs_by_state.keys()):
            state_jobs = jobs_by_state[state]
            message = f"🚨 <b>FIFO Jobs Alert - {state}</b> ({len(state_jobs)} new)\n\n"

            for i, job in enumerate(state_jobs[:5], 1):  # Max 5 per state
                title = job.get('title', 'N/A')
                company = job.get('company', 'N/A')
                location = job.get('location', 'N/A')
                salary = job.get('salary', 'N/A')
                job_type = job.get('job_type', 'N/A')
                url = job.get('url', '#')
                visa_417 = job.get('visa_417_eligible', 'N/A')
                visa_cats = job.get('visa_417_categories', 'N/A')

                visa_text = ""
                if visa_417 == 'Yes':
                    visa_text = f"🇦🇺 Visa 417: ✅ Eligible ({visa_cats})"
                elif visa_417 == 'No':
                    visa_text = "🇦🇺 Visa 417: ❌ Not eligible"

                message += f"""<b>{i}. {title}</b>
🏢 {company} | {location}
💰 {salary} | 🎯 {job_type}

{visa_text}

<a href="{url}">→ Apply Now</a>

"""

            if len(state_jobs) > 5:
                message += f"<i>... and {len(state_jobs) - 5} more jobs in {state}</i>"

            if self.send_message(message):
                total_sent += 1

        logger.info(f"✓ Sent {total_sent} state alerts")
        return total_sent > 0

    def send_jobs_alert(self, jobs: List[Dict]) -> bool:
        """Send jobs alert to Telegram (one per state)"""
        if not jobs:
            return False

        return self.send_jobs_alert_by_state(jobs)

    def send_test_alert(self) -> bool:
        """Send a test alert"""
        message = """✅ <b>Bot is working!</b>

This is a test message from BackpackersJobsBot.
You'll receive job alerts here.

🚨 Alert types:
- New FIFO jobs in WA
- Salary reports
- Trend updates
- Special opportunities
"""
        return self.send_message(message)


# Quick test
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    alerts = TelegramAlerts()

    # Test alert
    print("Sending test alert...")
    success = alerts.send_test_alert()

    if success:
        print("✅ Test alert sent successfully!")
    else:
        print("❌ Failed to send test alert")

    # Example jobs alert
    test_jobs = [
        {
            'title': 'FIFO Labourer',
            'company': 'EDC Electrical',
            'location': 'Weipa, Cairns',
            'salary': '$45/hour',
            'url': 'https://seek.com.au/job/123456'
        },
        {
            'title': 'Underground Operator',
            'company': 'Mining Corp',
            'location': 'Perth',
            'salary': '$55/hour',
            'url': 'https://seek.com.au/job/123457'
        }
    ]

    print("\nSending jobs alert...")
    success = alerts.send_jobs_alert(test_jobs)

    if success:
        print("✅ Jobs alert sent successfully!")
    else:
        print("❌ Failed to send jobs alert")
