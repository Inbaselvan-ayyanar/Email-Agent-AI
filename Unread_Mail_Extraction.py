from urllib.request import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import base64
import os
import pickle
from google.auth.transport.requests import Request  

# 1. Scope for read-only access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = None
if os.path.exists('token_read.pickle'):
    with open('token_read.pickle', 'rb') as token:
        creds = pickle.load(token)


if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('client.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save credentials for next run
    with open('token_read.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)


def details():
    results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=1).execute()
    messages = results.get('messages', [])
    mail_details=[]
    if not messages:
        print("No unread messages found.")
    else:
        for msg in messages:
            msg_id = msg['id']
            msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

            # Extract headers
            headers = msg_data['payload']['headers']
            subject = sender = None
            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
                if header['name'] == 'From':
                    sender = header['value']

            # Function to get and clean email body
            def get_clean_body(payload):
                parts = payload.get("parts")
                body_data = None

                if parts:
                    for part in parts:
                        mime_type = part.get("mimeType")
                        data = part.get('body', {}).get('data')
                        if data:
                            decoded = base64.urlsafe_b64decode(data).decode()
                            if mime_type == "text/plain":
                                return decoded.strip()
                            elif mime_type == "text/html":
                                # Fallback if plain text not found
                                soup = BeautifulSoup(decoded, "html.parser")
                                body_data = soup.get_text().strip()
                else:
                    data = payload.get("body", {}).get("data")
                    if data:
                        decoded = base64.urlsafe_b64decode(data).decode()
                        mime_type = payload.get("mimeType", "")
                        if mime_type == "text/plain":
                            return decoded.strip()
                        elif mime_type == "text/html":
                            soup = BeautifulSoup(decoded, "html.parser")
                            return soup.get_text().strip()
                return body_data or "[No content found]"

            body = get_clean_body(msg_data['payload'])

            # Print and store data
            print("\n--- UNREAD EMAIL ---")
            print("From:", sender)
            print("Subject:", subject)
            print("Body:\n", body)
            
            def extract_email_address(from_header):
                import re
                match = re.search(r'<(.+?)>', from_header)
                if match:
                    return match.group(1)  
                else:
                    return from_header
            unread_email_data = {
                "From": extract_email_address(sender),
                "Subject": subject,
                "Body": body,
                "id": msg_id
            }

            print("\nExtracted Data:\n", unread_email_data)

            mail_details.append(unread_email_data)
    return mail_details

def main():
    print("Extracting process starts")
    email_details=details()
    print("Extracting process finished")
    return email_details
