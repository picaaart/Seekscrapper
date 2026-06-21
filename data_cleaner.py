"""
Data Cleaner - Nettoie les vieilles offres et gère l'archivage
"""

import csv
import os
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class DataCleaner:
    def __init__(self, retention_days=30):
        """
        Initialize data cleaner

        Args:
            retention_days: Nombre de jours à garder
        """
        self.retention_days = retention_days
        self.cutoff_date = datetime.now() - timedelta(days=retention_days)

    def parse_date(self, date_string):
        """Parse la date depuis le CSV (format: YYYY-MM-DD HH:MM:SS)"""
        try:
            return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        except:
            return None

    def is_expired(self, date_string):
        """Check si une entrée a expiré"""
        date = self.parse_date(date_string)
        if not date:
            return False
        return date < self.cutoff_date

    def clean_csv(self, csv_file):
        """
        Nettoie un CSV en supprimant les vieilles entrées
        Retourne le nombre d'entrées supprimées
        """
        if not os.path.exists(csv_file):
            logger.warning(f"CSV not found: {csv_file}")
            return 0

        try:
            # Lire le CSV
            rows = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)

            # Filtrer les vieilles entrées
            initial_count = len(rows)
            rows_kept = [r for r in rows if not self.is_expired(r.get('scraped_at', ''))]
            rows_removed = initial_count - len(rows_kept)

            if rows_removed > 0:
                # Sauvegarder le CSV nettoyé
                if rows_kept:  # Si des lignes restent
                    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=rows_kept[0].keys())
                        writer.writeheader()
                        writer.writerows(rows_kept)
                else:
                    # Si tout est supprimé, garder le header seulement
                    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                        if rows:
                            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                            writer.writeheader()

                logger.info(f"✓ Cleaned {csv_file}: removed {rows_removed} old entries, kept {len(rows_kept)}")
            else:
                logger.info(f"✓ {csv_file}: no old entries to remove")

            return rows_removed

        except Exception as e:
            logger.error(f"Error cleaning CSV {csv_file}: {e}")
            return 0

    def archive_removed_entries(self, csv_file, archive_file):
        """
        Archive les vieilles entrées dans un fichier séparé
        """
        if not os.path.exists(csv_file):
            return 0

        try:
            # Lire le CSV
            rows = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)

            # Filtrer les vieilles entrées à archiver
            rows_to_archive = [r for r in rows if self.is_expired(r.get('scraped_at', ''))]

            if rows_to_archive:
                # Ajouter à l'archive
                file_exists = os.path.exists(archive_file)

                with open(archive_file, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=rows_to_archive[0].keys())
                    if not file_exists:
                        writer.writeheader()
                    writer.writerows(rows_to_archive)

                logger.info(f"✓ Archived {len(rows_to_archive)} old entries to {archive_file}")
                return len(rows_to_archive)
            else:
                logger.info(f"✓ No entries to archive")
                return 0

        except Exception as e:
            logger.error(f"Error archiving entries: {e}")
            return 0

    def cleanup_all(self, current_csv, archive_csv=None):
        """
        Nettoie le CSV courant et archive les vieilles entrées
        """
        logger.info(f"Starting cleanup (retention: {self.retention_days} days)...")
        logger.info(f"Cutoff date: {self.cutoff_date.strftime('%Y-%m-%d')}")

        # Track trends BEFORE cleanup
        try:
            from trends_tracker import TrendsTracker
            logger.info("📊 Capturing trends before cleanup...")
            tracker = TrendsTracker(current_csv)
            tracker.track_trends()
        except Exception as e:
            logger.warning(f"Could not track trends: {e}")

        # Archive d'abord (avant de nettoyer)
        if archive_csv:
            self.archive_removed_entries(current_csv, archive_csv)

        # Puis nettoie
        removed = self.clean_csv(current_csv)

        logger.info(f"Cleanup complete: removed {removed} entries")
        return removed


# Exemple d'utilisation
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    cleaner = DataCleaner(retention_days=30)
    cleaner.cleanup_all(
        current_csv="data/jobs_australia_current.csv",
        archive_csv="data/jobs_australia_archive.csv"
    )
