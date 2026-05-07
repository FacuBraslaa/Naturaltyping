"""
Google Drive integration module for Natural Typing.
Handles authentication and writing to Google Docs with human-like timing.
Supports multiple Gmail accounts.
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth import default
from googleapiclient.discovery import build
import json

# Google Docs API scope
SCOPES = ['https://www.googleapis.com/auth/documents']

class GoogleDocsTyper:
    def __init__(self, credentials_path="credentials.json", user_email=None):
        """
        Initialize Google Docs Typer.
        
        Args:
            credentials_path: Path to OAuth2 credentials JSON file
            user_email: Optional email to use specific token file for multi-user support
        """
        self.credentials_path = credentials_path
        self.user_email = user_email
        self.service = None
        self.authenticate()
    
    def get_token_path(self):
        """Get the token path, supporting multiple users."""
        if self.user_email:
            # Create user-specific token file
            email_safe = self.user_email.replace("@", "_at_").replace(".", "_")
            return f"token_{email_safe}.pickle"
        return "token.pickle"
    
    def authenticate(self):
        """
        Authenticate with Google Docs API using OAuth2.
        Creates a token.pickle file for subsequent authentications.
        Supports multiple users with separate token files.
        """
        creds = None
        token_path = self.get_token_path()
        
        # Check if token exists
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    print(f"Error: {self.credentials_path} not found.")
                    print("Visit https://console.cloud.google.com/ to create OAuth2 credentials.")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('docs', 'v1', credentials=creds)
        return True
    
    def get_document_id(self, doc_name):
        """
        Find a Google Doc by name.
        
        Args:
            doc_name: Name of the document to find
        
        Returns:
            Document ID if found, None otherwise
        """
        try:
            drive_service = build('drive', 'v3', credentials=self.service._http.credentials)
            results = drive_service.files().list(
                spaces='drive',
                pageSize=10,
                q=f"name='{doc_name}' and trashed=false and mimeType='application/vnd.google-apps.document'",
                fields='files(id, name)'
            ).execute()
            
            items = results.get('files', [])
            if items:
                return items[0]['id']
            return None
        except Exception as e:
            print(f"Error finding document: {e}")
            return None
    
    def create_document(self, doc_name):
        """
        Create a new Google Doc.
        
        Args:
            doc_name: Name for the new document
        
        Returns:
            Document ID
        """
        try:
            drive_service = build('drive', 'v3', credentials=self.service._http.credentials)
            file_metadata = {
                'name': doc_name,
                'mimeType': 'application/vnd.google-apps.document'
            }
            file = drive_service.files().create(body=file_metadata, fields='id').execute()
            return file.get('id')
        except Exception as e:
            print(f"Error creating document: {e}")
            return None
    
    def insert_text(self, document_id, text, index=1):
        """
        Insert text into a Google Doc.
        
        Args:
            document_id: ID of the document
            text: Text to insert
            index: Position to insert (default: 1 = start of document)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            requests = [
                {
                    'insertText': {
                        'text': text,
                        'location': {
                            'index': index
                        }
                    }
                }
            ]
            
            self.service.documents().batchUpdate(
                documentId=document_id,
                body={'requests': requests}
            ).execute()
            return True
        except Exception as e:
            print(f"Error inserting text: {e}")
            return False
    
    def delete_text(self, document_id, start_index, end_index):
        """
        Delete text from a Google Doc (used for typo correction).
        
        Args:
            document_id: ID of the document
            start_index: Start position
            end_index: End position
        
        Returns:
            True if successful, False otherwise
        """
        try:
            requests = [
                {
                    'deleteContentRange': {
                        'range': {
                            'startIndex': start_index,
                            'endIndex': end_index
                        }
                    }
                }
            ]
            
            self.service.documents().batchUpdate(
                documentId=document_id,
                body={'requests': requests}
            ).execute()
            return True
        except Exception as e:
            print(f"Error deleting text: {e}")
            return False
    
    def get_document_content(self, document_id):
        """
        Get the current content of a Google Doc.
        
        Args:
            document_id: ID of the document
        
        Returns:
            Document content as string
        """
        try:
            doc = self.service.documents().get(documentId=document_id).execute()
            content = doc.get('body', {}).get('content', [])
            
            text = ""
            for item in content:
                if 'paragraph' in item:
                    for element in item['paragraph'].get('elements', []):
                        if 'textRun' in element:
                            text += element['textRun'].get('content', '')
            return text
        except Exception as e:
            print(f"Error getting document content: {e}")
            return ""
    
    def find_section_index(self, document_id, section_name):
        """
        Find the index position of a section (heading/title) in the document.
        
        Args:
            document_id: ID of the document
            section_name: Name of the section to find
        
        Returns:
            Index position if found, None otherwise
        """
        try:
            doc = self.service.documents().get(documentId=document_id).execute()
            content = doc.get('body', {}).get('content', [])
            
            current_index = 1
            for item in content:
                if 'paragraph' in item:
                    for element in item['paragraph'].get('elements', []):
                        if 'textRun' in element:
                            text_content = element['textRun'].get('content', '')
                            # Check if this element contains the section name
                            if section_name.lower() in text_content.lower():
                                # Return index at the end of this section line
                                return current_index + len(text_content)
                            current_index += len(text_content)
            return None
        except Exception as e:
            print(f"Error finding section: {e}")
            return None
    
    def list_sections(self, document_id):
        """
        List all headings/sections in the document.
        
        Args:
            document_id: ID of the document
        
        Returns:
            List of section names
        """
        try:
            doc = self.service.documents().get(documentId=document_id).execute()
            content = doc.get('body', {}).get('content', [])
            
            sections = []
            for item in content:
                if 'paragraph' in item:
                    style = item['paragraph'].get('paragraphStyle', {})
                    # Check if it's a heading
                    heading_id = style.get('headingId')
                    if heading_id:
                        for element in item['paragraph'].get('elements', []):
                            if 'textRun' in element:
                                text = element['textRun'].get('content', '').strip()
                                if text:
                                    sections.append(text)
                    else:
                        # Also capture paragraphs that might be section titles (bold, etc)
                        for element in item['paragraph'].get('elements', []):
                            if 'textRun' in element:
                                text_run = element['textRun']
                                text = text_run.get('content', '').strip()
                                if text and len(text) < 100:  # Likely a title
                                    style_info = text_run.get('textStyle', {})
                                    if style_info.get('bold') or style_info.get('italic'):
                                        sections.append(text)
            
            return sections
        except Exception as e:
            print(f"Error listing sections: {e}")
            return []
    
    @staticmethod
    def list_available_tokens():
        """List all available token files for different Gmail accounts."""
        tokens = [f for f in os.listdir('.') if f.startswith('token_') and f.endswith('.pickle')]
        if os.path.exists('token.pickle'):
            tokens.insert(0, 'token.pickle')
        return tokens

