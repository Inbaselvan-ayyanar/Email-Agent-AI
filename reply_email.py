import os
from urllib.request import Request 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import base64
from email.mime.text import MIMEText

sender_name="xyz" #modify it according to the requirement
from_email="abc@gmail.com" #modify it according to the requirement

def create_msg(sender,to ,subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_email(to_email,email_content="Hello from Gmail API with OAuth!"):
    
    SCOPES=['https://www.googleapis.com/auth/gmail.send']

    creds=None

    if os.path.exists("token_send.pickle"):
        with open('token_send.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token_send.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service=build("gmail",'v1',credentials=creds)
    
   
    email_content=email_content.replace("[Your Name]",sender_name)
    email_content=email_content.replace("[Recipient's Name]","sir/madam")
    print(email_content)
    message = create_msg(from_email,to_email, "Subject", email_content)
    sent_message = service.users().messages().send(userId="me", body=message).execute()
    print(f'Message Id: {sent_message["id"]}')


