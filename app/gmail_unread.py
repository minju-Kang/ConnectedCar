from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def gmailFirstSignin(name):
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=8080)

    with open('gmail_tokens/'+name+'_token.json', 'w') as token:
        token.write(creds.to_json())

    return get_mails(creds)


def gmailUnread(name):
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

    if os.path.exists('gmail_tokens/'+name+'_token.json'):
        # while signed in
        creds = Credentials.from_authorized_user_file('gmail_tokens/'+name+'_token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # when access token expired
            creds.refresh(Request())
        else:
            # first sign in
            context = {'first_signin' : 1}
            return context

        with open('gmail_tokens/'+name+'_token.json', 'w') as token:
            token.write(creds.to_json())

    return get_mails(creds)


def get_mails(creds):
    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    mfrom = []
    msub = []

    msglist = service.users().messages().list(userId='me', q='is:unread', maxResults=10).execute()
    messages = msglist.get('messages')
    for message in messages:
        msg_id = message.get('id')
        msg = service.users().messages().get(userId='me', id=msg_id).execute()
        payload = msg.get('payload')
        headers = payload.get('headers')
        if headers:
            for header in headers:
                name = header.get('name')
                value = header.get('value')
                if name.lower() == 'from':
                    mfrom.append(value)
                if name.lower() == "subject":
                    msub.append(value)

    context = {
        'first-signin' : 0,
        'From': mfrom,
        'Subject' : msub
    }

    return context
