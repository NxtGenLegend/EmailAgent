import os
import base64
import pickle
import time
import argparse
from datetime import datetime
from typing import Dict, List

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class EmailAgent:
    def __init__(self):
        self.service = self._gmail_authenticate()
        self.processed_emails = set()
        
    def _gmail_authenticate(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                
        return build('gmail', 'v1', credentials=creds)
    
    def fetch_recent_emails(self, max_emails: int = 20) -> List[Dict]:
        try:
            results = self.service.users().messages().list(
                userId='me', maxResults=max_emails
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                if message['id'] in self.processed_emails:
                    continue
                    
                msg = self.service.users().messages().get(
                    userId='me', id=message['id'], format='full'
                ).execute()
                
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                
                body = self._get_email_body(msg)
                
                emails.append({
                    'id': message['id'],
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'body': body[:200] + '...' if len(body) > 200 else body
                })
                
                self.processed_emails.add(message['id'])
                
            return emails
        
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []
    
    def _get_email_body(self, message: Dict) -> str:
        try:
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            elif 'body' in message['payload'] and 'data' in message['payload']['body']:
                return base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
        except:
            pass
        return "No body content found"
    
    def generate_summary(self, emails: List[Dict]) -> str:
        if not emails:
            return "No new emails found."
        
        summary = f"\n=== EMAIL SUMMARY ({len(emails)} new emails) ===\n"
        summary += f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for i, email in enumerate(emails, 1):
            summary += f"{i}. FROM: {email['sender']}\n"
            summary += f"   SUBJECT: {email['subject']}\n"
            summary += f"   DATE: {email['date']}\n"
            summary += f"   PREVIEW: {email['body']}\n\n"
        
        return summary
    
    def run(self, check_interval: int = 60, summary_interval: int = 300):
        print(f"Email Agent started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Checking every {check_interval} seconds, summary every {summary_interval} seconds")
        print("Press Ctrl+C to stop monitoring")
        
        last_summary_time = time.time()
        new_emails_since_summary = []
        
        try:
            while True:
                current_time = time.time()
                
                new_emails = self.fetch_recent_emails()
                new_emails_since_summary.extend(new_emails)
                
                if new_emails:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(new_emails)} new emails")
                
                if current_time - last_summary_time >= summary_interval:
                    summary = self.generate_summary(new_emails_since_summary)
                    print(summary)
                    new_emails_since_summary = []
                    last_summary_time = current_time
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print(f"\nEmail Agent stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    parser = argparse.ArgumentParser(description="Monitor Gmail inbox and provide periodic summaries")
    parser.add_argument("--check-interval", type=int, default=30,
                       help="How often to check for new emails in seconds (default: 30)")
    parser.add_argument("--summary-interval", type=int, default=180,
                       help="How often to print summary in seconds (default: 180)")
    parser.add_argument("--max-emails", type=int, default=20,
                       help="Maximum number of emails to check (default: 20)")
    
    args = parser.parse_args()
    
    print("Email Agent - Monitor your Gmail inbox")
    print("Make sure you have credentials.json in your current directory")
    print()
    
    try:
        agent = EmailAgent()
        agent.run(check_interval=args.check_interval, 
                          summary_interval=args.summary_interval)
    except FileNotFoundError:
        print("Error: credentials.json not found!")
        print("Please download credentials.json from Google Cloud Console")
        print("See README for setup instructions")
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your setup and try again")

if __name__ == "__main__":
    main()