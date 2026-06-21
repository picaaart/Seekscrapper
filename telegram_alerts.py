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

    def format_fifo_wa_jobs(self, jobs: List[Dict]) -> str:
        """
        Format FIFO WA jobs for Telegram alert

        Args:
            jobs: List of job dictionaries

        Returns:
            Formatted message string
        """
        if not jobs:
            return "No new FIFO WA jobs"

        message = f"🚨 <b>FIFO WA Jobs Alert</b> ({len(jobs)} new)\n\n"

        for i, job in enumerate(jobs[:5], 1):  # Max 5 jobs per alert
            title = job.get('title', 'N/A')
            company = job.get('company', 'N/A')
            location = job.get('location', 'N/A')
            salary = job.get('salary', 'N/A')
            url = job.get('url', '#')

            # Format salary
            salary_text = ""
            if salary != 'N/A':
                salary_text = f"💰 {salary}\n"

            message += f"""<b>{i}. {title}</b>
🏢 {company}
📍 {location}
{salary_text}<a href="{url}">View Job</a>

"""

        if len(jobs) > 5:
            message += f"... and {len(jobs) - 5} more jobs!"

        return message

    def format_salary_report(self, stats: Dict) -> str:
        """Format salary report for Telegram"""
        message = """📊 <b>Weekly Salary Report - FIFO WA</b>

"""
        message += f"💰 Average: {stats.get('avg_salary', 'N/A')}\n"
        message += f"📈 Range: {stats.get('salary_min', 'N/A')} - {stats.get('salary_max', 'N/A')}\n"
        message += f"📌 Jobs posted: {stats.get('total_jobs', 'N/A')}\n"

        return message

    def send_jobs_alert(self, jobs: List[Dict]) -> bool:
        """Send jobs alert to Telegram"""
        if not jobs:
            return False

        message = self.format_fifo_wa_jobs(jobs)
        return self.send_message(message)

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
