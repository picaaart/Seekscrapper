"""
Google Drive synchronization module
Upload CSV files to Google Drive automatically
"""

import os
import pickle
import logging
from typing import Optional
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

# Google Drive scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']


class GoogleDriveSync:
    def __init__(self, credentials_file: str, token_file: str, folder_name: str):
        """
        Initialize Google Drive sync

        Args:
            credentials_file: Path to credentials.json from Google Cloud Console
            token_file: Path to store authentication token
            folder_name: Name of folder to sync to on Google Drive
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.folder_name = folder_name
        self.service = None
        self.folder_id = None

    def authenticate(self) -> bool:
        """
        Authenticate with Google Drive
        First time: opens browser for OAuth
        Subsequent times: uses cached token
        """
        try:
            creds = None

            # Load existing token
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
                logger.info("✓ Loaded cached Google credentials")

            # If no valid credentials, get new ones
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    logger.info("✓ Refreshed Google credentials")
                else:
                    if not os.path.exists(self.credentials_file):
                        logger.error(f"❌ Credentials file not found: {self.credentials_file}")
                        logger.error("   Download from Google Cloud Console and save as google_credentials.json")
                        return False

                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                    logger.info("✓ Google authentication successful")

                # Save token
                with open(self.token_file, 'wb') as token:
                    pickle.dump(creds, token)

            self.service = build('drive', 'v3', credentials=creds)
            return True

        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            return False

    def get_or_create_folder(self) -> Optional[str]:
        """
        Get existing folder ID or create new one
        """
        try:
            if not self.service:
                logger.error("Not authenticated with Google Drive")
                return None

            # Search for folder
            query = f"name='{self.folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                pageSize=1
            ).execute()

            files = results.get('files', [])

            if files:
                self.folder_id = files[0]['id']
                logger.info(f"✓ Found Google Drive folder: {self.folder_name}")
                return self.folder_id

            # Create new folder
            file_metadata = {
                'name': self.folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()

            self.folder_id = folder.get('id')
            logger.info(f"✓ Created Google Drive folder: {self.folder_name}")
            return self.folder_id

        except HttpError as e:
            logger.error(f"❌ Google Drive error: {e}")
            return None

    def upload_file(self, file_path: str, file_name: Optional[str] = None) -> bool:
        """
        Upload or update file in Google Drive folder
        """
        try:
            if not self.service:
                logger.error("Not authenticated with Google Drive")
                return False

            if not self.folder_id:
                if not self.get_or_create_folder():
                    return False

            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False

            if not file_name:
                file_name = os.path.basename(file_path)

            # Search for existing file in folder
            query = f"name='{file_name}' and '{self.folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id)',
                pageSize=1
            ).execute()

            files = results.get('files', [])

            # Prepare file metadata
            file_metadata = {'name': file_name}
            media = MediaFileUpload(file_path, mimetype='text/csv', resumable=True)

            if files:
                # Update existing file
                file_id = files[0]['id']
                self.service.files().update(
                    fileId=file_id,
                    media_body=media,
                    fields='id'
                ).execute()
                logger.info(f"✓ Updated file on Google Drive: {file_name}")
            else:
                # Create new file
                file_metadata['parents'] = [self.folder_id]
                self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                logger.info(f"✓ Uploaded file to Google Drive: {file_name}")

            return True

        except HttpError as e:
            logger.error(f"❌ Upload error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return False

    def sync(self, file_path: str) -> bool:
        """
        Full sync: authenticate, create/find folder, and upload file
        """
        if not self.authenticate():
            return False

        if not self.get_or_create_folder():
            return False

        return self.upload_file(file_path)
