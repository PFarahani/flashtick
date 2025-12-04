"""
Google Sheets integration service with Tick-8 SRS support
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from typing import List, Dict, Optional

class GoogleSheetsService:
    """Service for interacting with Google Sheets"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self, spreadsheet_id: Optional[str] = None, sheet_gid: Optional[str] = None):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_gid = sheet_gid
        self.client = None
        self.sheet = None
        self.worksheet = None
        
        if spreadsheet_id:
            self._connect()
        
    def _connect(self):
        """Establish connection to Google Sheets"""
        try:
            # Load credentials
            creds = Credentials.from_service_account_file(
                'config/credentials.json',
                scopes=self.SCOPES
            )
            
            # Authorize client
            self.client = gspread.authorize(creds)
            
            # Open spreadsheet
            self.sheet = self.client.open_by_key(self.spreadsheet_id)
            
            # Get specific worksheet by gid (if provided)
            if self.sheet_gid:
                for ws in self.sheet.worksheets():
                    if str(ws.id) == self.sheet_gid:
                        self.worksheet = ws
                        break
            
            # Fall back to first sheet if gid not found or not provided
            if not self.worksheet:
                self.worksheet = self.sheet.get_worksheet(0)
                
        except FileNotFoundError:
            raise Exception("config/credentials.json file not found. Please follow the setup instructions.")
        except Exception as e:
            raise Exception(f"Failed to connect to Google Sheets: {str(e)}")
    
    def connect_to_sheet(self, spreadsheet_id: str, sheet_gid: Optional[str] = None):
        """Connect to a specific Google Sheet"""
        self.spreadsheet_id = spreadsheet_id
        self.sheet_gid = sheet_gid
        self._connect()
    
    def is_connected(self) -> bool:
        """Check if connected to a Google Sheet"""
        return self.client is not None and self.worksheet is not None
            
    def fetch_words(self) -> List[Dict]:
        """Fetch all words from the spreadsheet
        
        Expected columns:
        A: Front
        B: Back
        C: Last Practice Date
        D: SRS Stage (0-8)
        E: Number of Failed
        """
        if not self.is_connected():
            raise Exception("Not connected to a Google Sheet")
            
        try:
            # Get all values (columns A-E)
            all_values = self.worksheet.get_all_values()
            
            if len(all_values) < 2:
                return []
                
            # Skip header row
            data_rows = all_values[1:]
            
            words = []
            for idx, row in enumerate(data_rows, start=2):  # Start at 2 (1 is header)
                if len(row) >= 2 and row[0].strip():  # Check if Front exists
                    words.append({
                        'row_index': idx,
                        'front': row[0].strip(),
                        'back': row[1].strip(),
                        'last_practice_date': row[2].strip() if len(row) > 2 else '',
                        'srs_stage': int(row[3]) if len(row) > 3 and row[3].isdigit() else 0,
                        'failed_count': int(row[4]) if len(row) > 4 and row[4].isdigit() else 0
                    })
                    
            return words
        except Exception as e:
            raise Exception(f"Failed to fetch words: {str(e)}")
        
    def update_word_stats(self, row_index: int, correct: bool, new_stage: int):
        """Update statistics and SRS data for a word (Tick-8 method)
        
        Updates:
        - Column C: Last Practice Date
        - Column D: SRS Stage
        - Column E: Number of Failed (only if wrong)
        """
        if not self.is_connected():
            return
            
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Update last practice date (Column C)
            self.worksheet.update_cell(row_index, 3, today)
            
            # Update SRS stage (Column D)
            self.worksheet.update_cell(row_index, 4, new_stage)
            
            # Update failed count only if incorrect (Column E)
            if not correct:
                current_failed = self.worksheet.cell(row_index, 5).value
                new_failed = int(current_failed) + 1 if current_failed and current_failed.isdigit() else 1
                self.worksheet.update_cell(row_index, 5, new_failed)
            
        except Exception as e:
            print(f"Warning: Failed to update word stats: {str(e)}")