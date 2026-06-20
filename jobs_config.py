"""
Jobs Configuration - Toutes les catégories et jobs à scraper
Facile à étendre avec de nouvelles catégories
"""

# Configuration principale
JOBS_CATEGORIES = {
    "construction": {
        "display_name": "Construction",
        "keywords": [
            "labourer", "carpenter", "electrician", "plumber",
            "scaffolder", "concrete finisher", "welder", "bricklayer",
            "tiler", "painter", "roofer", "steel fixer", "construction worker"
        ]
    },
    "fifo_mines": {
        "display_name": "FIFO / Mines",
        "keywords": [
            "underground operator", "truck driver", "drill operator", "blaster",
            "plant operator", "haul truck driver", "production operator",
            "plant mechanic", "loader operator", "dozer operator", "miner",
            "mining operator", "haul truck", "dump truck"
        ]
    },
    "agriculture": {
        "display_name": "Agriculture / Farms",
        "keywords": [
            "farm labourer", "fruit picker", "vegetable picker", "dairy hand",
            "livestock handler", "seasonal worker", "farm manager", "packer",
            "farm worker", "picker", "harvester", "agricultural worker"
        ]
    },
    "logistics": {
        "display_name": "Logistics / Transport",
        "keywords": [
            "truck driver", "forklift operator", "warehouse worker", "loader",
            "delivery driver", "courier", "transport driver", "logistics",
            "order picker", "warehouse assistant", "stock handler"
        ]
    },
    "hospitality": {
        "display_name": "Hospitality",
        "keywords": [
            "chef", "cook", "waiter", "barista", "bartender", "dishwasher",
            "kitchen hand", "food prep", "restaurant", "café", "hotel staff",
            "hospitality", "counter staff", "sous chef"
        ]
    },
    "healthcare": {
        "display_name": "Healthcare / Aged Care",
        "keywords": [
            "aged care", "support worker", "nurse", "healthcare", "carer",
            "nursing", "care assistant", "personal care", "disability support",
            "health worker", "medical", "hospital", "care worker"
        ]
    },
    "retail": {
        "display_name": "Retail",
        "keywords": [
            "sales", "retail", "cashier", "stock", "shop assistant",
            "customer service", "till operator", "sales assistant",
            "retail worker", "stockroom", "merchandiser"
        ]
    },
    "warehouse": {
        "display_name": "Warehouse / Distribution",
        "keywords": [
            "warehouse", "packer", "picker", "forklift", "loader",
            "distribution", "packaging", "labeller", "stock", "inventory",
            "warehouse worker", "dispatch", "fulfillment"
        ]
    },
    "security": {
        "display_name": "Security",
        "keywords": [
            "security guard", "security", "bouncer", "reception",
            "security officer", "nightlife", "event security", "site security",
            "loss prevention", "security patrol"
        ]
    },
    "cleaning": {
        "display_name": "Cleaning / Facilities",
        "keywords": [
            "cleaner", "housekeeper", "janitor", "cleaning", "housekeeping",
            "facilities", "maintenance", "cleaning assistant", "office cleaner",
            "domestic cleaner", "house cleaning", "industrial cleaner"
        ]
    }
}

# États d'Australie
AUSTRALIAN_STATES = {
    "QLD": "Queensland",
    "NSW": "New South Wales",
    "VIC": "Victoria",
    "WA": "Western Australia",
    "SA": "South Australia",
    "TAS": "Tasmania",
    "NT": "Northern Territory",
    "ACT": "Australian Capital Territory"
}

# Data retention et nettoyage
DATA_RETENTION_DAYS = 30  # Garder les offres de moins de 30 jours

# Optionnel : retention différente par catégorie
# DATA_RETENTION_DAYS = {
#     "construction": 30,
#     "agriculture": 14,      # Plus saisonnier
#     "hospitality": 7,       # Change plus vite
# }

# Fichiers de sortie
OUTPUT_CSV_CURRENT = "data/jobs_australia_current.csv"      # Jobs actuels (< 30 jours)
OUTPUT_CSV_ARCHIVE = "data/jobs_australia_archive.csv"      # Tout l'historique
OUTPUT_CSV_ALL_STATES = "data/jobs_australia_all.csv"       # Combiné pour analyses

# Logging
LOG_CLEANING = True  # Log les suppressions

print(f"✓ Jobs config loaded: {len(JOBS_CATEGORIES)} catégories")
