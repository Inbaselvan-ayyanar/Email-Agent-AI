import os
import pickle
from urllib.request import Request


def spam(msg):

    import joblib
    model=joblib.load("spam_classifier_pipeline.pkl")
    per=model.predict([msg])
    
    return "spam" if per == 1 else "Ham"


def mark_as_read(id):
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    creds = None
    if os.path.exists('token_modify.pickle'):
        with open('token_modify.pickle', 'rb') as token:
            creds = pickle.load(token)


    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for next run
        with open('token_modify.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    service.users().messages().modify(
    userId='me',
    id=id,
    body={'removeLabelIds': ['UNREAD']}
    ).execute()


def main():
    import Unread_Mail_Extraction 
    datas = Unread_Mail_Extraction.main()
    
    for data in datas:
        if  "no-reply" not in data["From"] and "noreply" not in data["From"]:
            
            if  not data["Body"] == '[No content found]' and spam(data["Body"])=="Ham":
                print("Ham")
             
                import email_generator

                email_content=email_generator.generate_email(data["Body"],data["Subject"])
                
                import reply_email
                reply_email.send_email(data["From"],email_content)
                mark_as_read(data["id"])
                
            else:
                print("Spam Mail")
                mark_as_read(data["id"])
        else:
            print("no reply mail")
            mark_as_read(data["id"])

main()

