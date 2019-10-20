from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email
from apiclient import errors
from pprint import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])

    for message in messages:
        # print(message.get(userId='me', id=message['id']))
        # print(message.get('me', message['id']))
        # print(message['id'])
        # print(message)
        print("\n\n")
        pprint(getMessage(service, "me", message['id']))
        


def getMessage(service, uId, mId):
    raw_msg = service.users().messages().get(userId=uId, id=mId, format="full").execute()
    # print(raw_msg['payload']['parts'])
    text_data = raw_msg['payload']['parts'][0]['body']['data']
    # print(text_data)
    decoded_text = base64.urlsafe_b64decode(text_data)
    # print(decoded_text)
    message = email.message_from_bytes(decoded_text)
    print(message)
    return message


if __name__ == '__main__':
    main()
