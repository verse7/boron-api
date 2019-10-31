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

class EmailService:
    """ class to deal with gmail api services and custom manipulation of emails """

    def __init__(self, userId="me"): 
        """ init gmail service object - uses 'me' as user ID by default"""
        self.userId = userId
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
        self.creds = creds
        self.service = build('gmail', 'v1', credentials=self.creds)

    def emailList(self):
        """ get list of emails - list of messages with thread and email IDs (no actual content) """
        results = self.service.users().messages().list(userId='me').execute()
        return results.get('messages', [])

    def emails(self):
        """ get email objects from user inbox
            returns email Resource object - see gmail API docs """
        results = []
        for mail in self.emailList():
            results.append(self.service.users().messages().get(userId=self.userId, id=mail['id']).execute())
        return results
   
    def bodyText(self, mail):
        """ Get text body of email message """
        text_data = self.payload(mail)['parts'][0]['body']['data']  # grabs plain text portion of email (base64 bytes)
        decoded_text = base64.urlsafe_b64decode(text_data)  # decodes base 64 byte text
        message = email.message_from_bytes(decoded_text)    # parses text from email in decoded text
        return str(message)

    def payload(self, mail):
        return mail['payload']

    def headers(self, mail):
        """ get list of headers in email """
        return self.payload(mail)['headers']
    
    def header(self, mail, name):
        for header in self.headers(mail):
            if(header['name'] == name):
                return header
        raise Exception("header name provided not found")

    def whoTo(self, mail):
        """ email address of recipient """
        try:
            header = self.header(mail, "To")
            return header['value']
        except Exception as e:
            print(e)

    def whoFrom(self, mail):
        """ email address of sender """

        def extractAddress(user):
            """ extract email address from Sender field | Rowan Atkinson <rowaneatkinson@gmail.com> """
            address = user.split()[-1]
            return address.translate({ord(i): None for i in '<>'})

        try:
            header = self.header(mail, "From")
            return extractAddress(header['value'])
        except Exception as e:
            print(e)


    def labels(self):
        return self.service.users().labels().list(userId=self.userId).execute()['labels']

    def getlatest(self, sender=""):
        for mail in self.emails():
            if self.whoFrom(mail) == sender:
                return mail
        return None


eservice = EmailService()
"""
if __name__ == "__main__":
    eService = EmailService()
    emails = eService.emails()
    for mail in emails:
        print(eService.whoFrom(mail))
        # print(eService.bodyText(mail))
    for label in eService.labels():
        print(label)
 """