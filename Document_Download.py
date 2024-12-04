import os
import base64
import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Constants
TMP_DIR = 'temp_attachments'
LOG_FILE = "process_log.txt"

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def authenticate_gmail():
    """
    Authenticates the Gmail API using the token.json file.
    Returns:
        service: Authenticated Gmail API service object.
    """
    try:
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.readonly'])
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        logging.error(f"Failed to authenticate Gmail API: {e}")
        raise

def download_attachments(service):
    """
    Downloads attachments from Gmail and saves them to TMP_DIR.
    Args:
        service: Authenticated Gmail API service object.
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        os.makedirs(TMP_DIR, exist_ok=True)
        results = service.users().messages().list(userId='me', q="has:attachment").execute()
        messages = results.get('messages', [])

        if not messages:
            logging.info("No emails with attachments found.")
            return True

        for msg in messages:
            msg = service.users().messages().get(userId='me', id=msg['id']).execute()
            for part in msg['payload'].get('parts', []):
                if part['filename'] and 'attachmentId' in part['body']:
                    attachment_id = part['body']['attachmentId']
                    attachment = service.users().messages().attachments().get(
                        userId='me', messageId=msg['id'], id=attachment_id
                    ).execute()
                    data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                    file_path = os.path.join(TMP_DIR, part['filename'])

                    with open(file_path, 'wb') as f:
                        f.write(data)

                    logging.info(f"Downloaded {part['filename']} to {file_path}")
        return True
    except Exception as e:
        logging.error(f"Error downloading attachments: {e}")
        return False

def main():
    """
    Main execution flow for the script.
    """
    try:
        service = authenticate_gmail()
        download_success = download_attachments(service)
        if download_success:
            logging.info("Process completed successfully.")
        else:
            logging.warning("Process completed with errors.")
    except Exception as e:
        logging.error(f"Failed to complete the process: {e}")

if __name__ == "__main__":
    main()
