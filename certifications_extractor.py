#!/usr/bin/env python3
"""
Certifications Extractor
Extract required and desirable certifications/tickets from job descriptions
Focused on FIFO/Mining and Construction roles in Australia
"""

import re
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class CertificationsExtractor:
    """Extract certifications from job descriptions"""

    # Certification patterns - Australia focused
    REQUIRED_PATTERNS = {
        'white_card': {
            'patterns': [
                r'white\s*card',
                r'(?:induction|wh&s|work\s*health\s*safety)\b',
            ],
            'keywords': ['white card', 'induction', 'wh&s'],
            'confidence': 0.95,
        },
        'drivers_license': {
            'patterns': [
                r'(?:QLD|NSW|WA|VIC|current)?\s*drivers?\s*licen[sc]e',
                r'(?:driver.*license|drivers.*license)\b',
                r'\bDL\b',
            ],
            'keywords': ['drivers license', 'driver license', 'dl'],
            'confidence': 0.90,
        },
        'first_aid': {
            'patterns': [
                r'first\s*aid',
                r'first\s*aid\s*cert(?:ificate)?',
                r'\bfac\b',
            ],
            'keywords': ['first aid', 'fac'],
            'confidence': 0.92,
        },
        'drug_alcohol_test': {
            'patterns': [
                r'(?:drug|alcohol)(?:\s+and)?(?:\s+alcohol|\s+drug)?(?:\s*test)?',
                r'd[&a]a\b',
                r'drug\s*screen',
                r'pass\s+(?:a\s+)?(?:drug|alcohol)',
            ],
            'keywords': ['drug test', 'alcohol test', 'd&a'],
            'confidence': 0.88,
        },
        'forklift_license': {
            'patterns': [
                r'forklift\s*(?:license|cert|ticket)?',
                r'fork\s*lift',
            ],
            'keywords': ['forklift', 'flt'],
            'confidence': 0.90,
        },
        'heavy_vehicle_license': {
            'patterns': [
                r'(?:HR|HC|heavy\s*(?:rigid|combination))\s*licen[sc]e',
                r'(?:HR|HC)\s*licence',
                r'heavy\s*vehicle',
                r'truck\s*license',
            ],
            'keywords': ['hr license', 'hc license', 'heavy vehicle'],
            'confidence': 0.92,
        },
        'excavator_ticket': {
            'patterns': [
                r'excavator\s*(?:license|cert|ticket)',
                r'excavator\s*ticket',
            ],
            'keywords': ['excavator'],
            'confidence': 0.85,
        },
        'bobcat_ticket': {
            'patterns': [
                r'bobcat\s*(?:license|cert|ticket)',
                r'skid\s*steer',
            ],
            'keywords': ['bobcat', 'skid steer'],
            'confidence': 0.85,
        },
        'machinery_ticket': {
            'patterns': [
                r'machinery\s*tickets?',
                r'plant\s*operator',
                r'dozer\s*(?:license|cert)',
            ],
            'keywords': ['machinery ticket', 'plant operator', 'dozer'],
            'confidence': 0.80,
        },
    }

    DESIRABLE_PATTERNS = {
        'forklift_license': {
            'patterns': [r'forklift.*(?:desirable|preferred|bonus|advantage)'],
        },
        'machinery_ticket': {
            'patterns': [r'machinery.*(?:desirable|preferred|bonus|advantage)'],
        },
        'hr_hc_licence': {
            'patterns': [r'HR/HC.*(?:desirable|preferred|bonus|advantage)'],
        },
        'excavator_ticket': {
            'patterns': [r'excavator.*(?:desirable|preferred|bonus|advantage)'],
        },
    }

    @classmethod
    def extract(cls, description: str) -> Dict:
        """
        Extract certifications from job description

        Returns:
            {
                'required': [
                    {'name': 'white_card', 'confidence': 0.95, 'found': 'White Card'},
                    ...
                ],
                'desirable': [
                    {'name': 'forklift_license', 'confidence': 0.85, 'found': 'Forklift...'},
                    ...
                ],
                'raw_text': [extracted text snippets]
            }
        """
        if not description:
            return {'required': [], 'desirable': [], 'raw_text': []}

        required = []
        desirable = []
        raw_text = []

        # Extract required certifications
        for cert_name, cert_config in cls.REQUIRED_PATTERNS.items():
            for pattern in cert_config['patterns']:
                matches = re.finditer(
                    pattern,
                    description,
                    re.IGNORECASE | re.MULTILINE
                )

                for match in matches:
                    # Check if it's in a "not required" or "not necessary" context (before only)
                    start_pos = max(0, match.start() - 50)
                    context_before = description[start_pos:match.end()]
                    if cls._is_negated(context_before):
                        continue

                    required.append({
                        'name': cert_name,
                        'confidence': cert_config['confidence'],
                        'found': match.group(),
                        'context': context_before[:50] + '...' if len(context_before) > 50 else context_before
                    })
                    raw_text.append(context_before)
                    break  # Only count once per cert

        # Extract desirable certifications
        for cert_name, cert_config in cls.DESIRABLE_PATTERNS.items():
            for pattern in cert_config['patterns']:
                matches = re.finditer(
                    pattern,
                    description,
                    re.IGNORECASE | re.MULTILINE
                )

                for match in matches:
                    desirable.append({
                        'name': cert_name,
                        'confidence': 0.75,
                        'found': match.group()[:60] + '...' if len(match.group()) > 60 else match.group(),
                        'context': cls._get_context(description, match.start(), window=100)[:50] + '...'
                    })
                    raw_text.append(match.group())
                    break

        # Remove duplicates while preserving order
        required = cls._deduplicate_certs(required)
        desirable = cls._deduplicate_certs(desirable)

        return {
            'required': required,
            'desirable': desirable,
            'raw_text': list(dict.fromkeys(raw_text))  # Remove duplicates, keep order
        }

    @staticmethod
    def _is_negated(text: str) -> bool:
        """Check if text contains negation"""
        negations = [
            'not required',
            'not necessary',
            'dont need',
            "don't need",
            'no need',
            'not essential',
            "you won't need",
        ]
        return any(neg in text.lower() for neg in negations)

    @staticmethod
    def _get_context(text: str, position: int, window: int = 100) -> str:
        """Get context around a match position"""
        start = max(0, position - window)
        end = min(len(text), position + window)
        return text[start:end]

    @staticmethod
    def _deduplicate_certs(certs: List[Dict]) -> List[Dict]:
        """Remove duplicate certifications by name, keep highest confidence"""
        seen = {}
        for cert in certs:
            name = cert['name']
            if name not in seen or cert['confidence'] > seen[name]['confidence']:
                seen[name] = cert
        return list(seen.values())

    @classmethod
    def format_for_csv(cls, extracted: Dict) -> str:
        """Format extracted certs for CSV column"""
        required_names = [c['name'] for c in extracted['required']]
        return '|'.join(required_names) if required_names else 'N/A'

    @classmethod
    def format_desirable_for_csv(cls, extracted: Dict) -> str:
        """Format desirable certs for CSV column"""
        desirable_names = [c['name'] for c in extracted['desirable']]
        return '|'.join(desirable_names) if desirable_names else 'N/A'


# Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    test_description = """
    FIFO Labourer

    EDC Electrical & Co. is based in Weipa.

    Due to an increasing client base and project commitments, we are currently looking for Labourers to join our team.

    Immediate Start

    2:1 Roster out of Cairns or Brisbane

    Positions Available:

    General Laborer

    Amrun dewatering project

    About You:

    To be successful for this role you must have:

    A current QLD drivers licence

    White Card

    The ability to work unsupervised

    A positive attitude

    Self-Motivation

    A strong work ethic and a willingness to work the hours that are required to meet project deadlines

    Commitment to delivering quality results for our clients

    Must pass a drug and Alcohol

    The following is desirable but not necessary:

    Machinery Tickets (Bobcat, excavator etc)

    HR/HC Licence

    What is on offer:

    Attractive Hourly Rate

    A great work life balance

    be a part of a close-knit team, working for a family business who actually care about their employees.
    """

    result = CertificationsExtractor.extract(test_description)

    print("REQUIRED CERTIFICATIONS:")
    for cert in result['required']:
        print(f"  ✅ {cert['name']} (confidence: {cert['confidence']})")
        print(f"     Found: {cert['found']}")

    print("\nDESIRABLE CERTIFICATIONS:")
    for cert in result['desirable']:
        print(f"  ⚠️  {cert['name']} (confidence: {cert['confidence']})")

    print("\nCSV FORMAT:")
    print(f"  Required: {CertificationsExtractor.format_for_csv(result)}")
    print(f"  Desirable: {CertificationsExtractor.format_desirable_for_csv(result)}")
