"""
Visa 417 Eligibility Checker
Extracts postcode from job location and checks visa 417 eligibility
"""

import re
import logging
from visa_417_config import check_postcode_eligibility

logger = logging.getLogger(__name__)


class Visa417Checker:
    """Check if jobs are eligible for Visa 417 extension"""

    # Common Australian postcodes patterns
    POSTCODE_PATTERN = re.compile(r'\b(\d{4})\b')

    # Suburb to postcode mappings (common ones for backpackers)
    SUBURB_TO_POSTCODE = {
        # Queensland
        "cairns": "4870",
        "townsville": "4810",
        "mount isa": "4825",
        "mackay": "4740",
        "rockhampton": "4700",
        "gladstone": "4680",
        "toowoomba": "4350",
        "gold coast": "4217",
        "sunshine coast": "4560",
        "brisbane": "4000",
        "ipswich": "4305",
        "logan city": "4114",
        "bundaberg": "4670",
        "hervey bay": "4655",
        "maryborough": "4650",

        # New South Wales
        "sydney": "2000",
        "newcastle": "2300",
        "wollongong": "2500",
        "coffs harbour": "2450",
        "orange": "2800",
        "bathurst": "2795",
        "armidale": "2350",
        "lismore": "2480",
        "canberra": "2600",

        # Victoria
        "melbourne": "3000",
        "geelong": "3220",
        "ballarat": "3350",
        "bendigo": "3550",
        "shepparton": "3630",
        "albury": "3640",

        # Western Australia
        "perth": "6000",
        "fremantle": "6160",
        "mandurah": "6210",
        "bunbury": "6230",
        "kalgoorlie": "6430",
        "broome": "6725",
        "geraldton": "6530",

        # South Australia
        "adelaide": "5000",
        "port augusta": "5700",
        "mount gambier": "5290",

        # Tasmania
        "hobart": "7000",
        "launceston": "7250",

        # Northern Territory
        "darwin": "0800",
        "alice springs": "0870",
    }

    def __init__(self):
        pass

    def extract_postcode(self, location_str, state):
        """
        Extract postcode from location string

        Args:
            location_str: Location string (e.g., "4670 Bundaberg, QLD")
            state: State code (e.g., "QLD")

        Returns:
            postcode (int) or None
        """
        if not location_str:
            return None

        # Try to find 4-digit postcode
        match = self.POSTCODE_PATTERN.search(str(location_str))
        if match:
            return match.group(1)

        # Try suburb to postcode lookup
        location_lower = location_str.lower()
        for suburb, postcode in self.SUBURB_TO_POSTCODE.items():
            if suburb in location_lower:
                return postcode

        return None

    def check_job_eligibility(self, job_data):
        """
        Check if a job is eligible for Visa 417

        Args:
            job_data: Dictionary with job info (must have 'location' and 'state')

        Returns:
            dict with eligibility info
        """
        location = job_data.get('location', '')
        state = job_data.get('state', '')

        if not location or not state:
            return {
                'visa_417_eligible': 'UNKNOWN',
                'visa_417_categories': 'No location/state',
                'postcode': None
            }

        # Extract postcode
        postcode = self.extract_postcode(location, state)

        if not postcode:
            return {
                'visa_417_eligible': 'UNKNOWN',
                'visa_417_categories': 'Could not extract postcode',
                'postcode': None
            }

        # Check eligibility
        result = check_postcode_eligibility(postcode, state)

        return {
            'visa_417_eligible': result['short_status'],
            'visa_417_categories': result['details'],
            'postcode': postcode
        }

    def add_visa_fields(self, job_data):
        """
        Add visa 417 fields to job data

        Args:
            job_data: Job dictionary

        Returns:
            job_data with added visa 417 fields
        """
        visa_info = self.check_job_eligibility(job_data)
        job_data.update(visa_info)
        return job_data


# Test examples
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    checker = Visa417Checker()

    test_jobs = [
        {
            'title': 'Fruit Picker',
            'location': 'Bundaberg, QLD',
            'state': 'QLD'
        },
        {
            'title': 'Construction Labourer',
            'location': 'Cairns 4870, QLD',
            'state': 'QLD'
        },
        {
            'title': 'Chef',
            'location': 'Brisbane CBD, QLD',
            'state': 'QLD'
        },
        {
            'title': 'Truck Driver',
            'location': '4670 Bundaberg, QLD',
            'state': 'QLD'
        }
    ]

    print("Testing Visa 417 Eligibility Checker\n")
    print("=" * 80)

    for job in test_jobs:
        visa_info = checker.check_job_eligibility(job)
        print(f"\n📋 {job['title']} - {job['location']}")
        print(f"   Postcode: {visa_info['postcode']}")
        print(f"   Visa 417 Eligible: {visa_info['visa_417_eligible']}")
        print(f"   Categories: {visa_info['visa_417_categories']}")

    print("\n" + "=" * 80)
