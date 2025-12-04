"""
Settings view for configuring the application
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSpinBox, QGroupBox, QFormLayout,
                             QLineEdit, QMessageBox, QTextEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.styles import Styles

class SettingsView(QWidget):
    """Settings configuration view"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)
        
        # Header
        header_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Back")
        back_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        back_btn.setMaximumWidth(120)
        back_btn.clicked.connect(self.save_and_return)
        
        title = QLabel("Settings")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        
        # Create a spacer widget for symmetry
        spacer = QWidget()
        spacer.setMaximumWidth(120)
        
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(spacer)
        
        layout.addLayout(header_layout)
        
        # Google Sheets Configuration
        sheets_group = QGroupBox("Google Sheets Configuration")
        sheets_group.setStyleSheet(Styles.GROUP_BOX)
        sheets_layout = QVBoxLayout()
        sheets_layout.setSpacing(15)
        
        # Spreadsheet ID
        sheet_id_layout = QFormLayout()
        sheet_id_label = QLabel("Spreadsheet ID:")
        sheet_id_label.setStyleSheet("color: #2c3e50; font-size: 14px; background: transparent;")
        
        self.spreadsheet_id_input = QLineEdit()
        self.spreadsheet_id_input.setPlaceholderText("Enter your Google Sheets ID")
        self.spreadsheet_id_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                color: #2c3e50;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        
        sheet_id_layout.addRow(sheet_id_label, self.spreadsheet_id_input)
        sheets_layout.addLayout(sheet_id_layout)
        
        # Sheet GID (optional)
        sheet_gid_layout = QFormLayout()
        sheet_gid_label = QLabel("Sheet GID (optional):")
        sheet_gid_label.setStyleSheet("color: #2c3e50; font-size: 14px; background: transparent;")
        
        self.sheet_gid_input = QLineEdit()
        self.sheet_gid_input.setPlaceholderText("Enter Sheet GID (leave empty for first sheet)")
        self.sheet_gid_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                color: #2c3e50;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        
        sheet_gid_layout.addRow(sheet_gid_label, self.sheet_gid_input)
        sheets_layout.addLayout(sheet_gid_layout)
        
        # Help text
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setMaximumHeight(100)
        help_text.setStyleSheet("""
            QTextEdit {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
                color: #7f8c8d;
                font-size: 12px;
            }
        """)
        help_text.setHtml("""
            <b>How to find your Spreadsheet ID:</b><br>
            Open your Google Sheet, look at the URL:<br>
            <code>https://docs.google.com/spreadsheets/d/<span style="color: #e74c3c;">SPREADSHEET_ID</span>/edit#gid=<span style="color: #3498db;">SHEET_GID</span></code><br>
            Copy the <span style="color: #e74c3c;">SPREADSHEET_ID</span> and optionally the <span style="color: #3498db;">SHEET_GID</span>. 
        """)
        sheets_layout.addWidget(help_text)
        
        # Connect button
        self.connect_btn = QPushButton("Connect to Google Sheet")
        self.connect_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        self.connect_btn.setMinimumHeight(45)
        self.connect_btn.clicked.connect(self.connect_to_sheet)
        sheets_layout.addWidget(self.connect_btn)
        
        # Connection status
        self.connection_status = QLabel("Status: Not Connected")
        self.connection_status.setStyleSheet("color: #95a5a6; font-size: 14px; background: transparent; padding: 5px;")
        self.connection_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sheets_layout.addWidget(self.connection_status)
        
        sheets_group.setLayout(sheets_layout)
        layout.addWidget(sheets_group)
        
        # Session settings
        session_group = QGroupBox("Session Settings")
        session_group.setStyleSheet(Styles.GROUP_BOX)
        session_layout = QFormLayout()
        session_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        session_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Label for spin box
        cards_label = QLabel("Cards per session:")
        cards_label.setStyleSheet("color: #2c3e50; font-size: 14px; background: transparent;")
        
        self.cards_per_session = QSpinBox()
        self.cards_per_session.setMinimum(5)
        self.cards_per_session.setMaximum(100)
        self.cards_per_session.setValue(20)
        self.cards_per_session.setStyleSheet(Styles.SPIN_BOX)
        self.cards_per_session.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        session_layout.addRow(cards_label, self.cards_per_session)
        session_group.setLayout(session_layout)
        
        layout.addWidget(session_group)
        
        layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        save_btn.setMinimumHeight(50)
        save_btn.clicked.connect(self.save_and_return)
        
        layout.addWidget(save_btn)
        
    def load_settings(self):
        """Load current settings from config"""
        config = self.main_window.config
        self.cards_per_session.setValue(config.get('cards_per_session', 20))
        self.spreadsheet_id_input.setText(config.get('spreadsheet_id', ''))
        self.sheet_gid_input.setText(config.get('sheet_gid', ''))
        
        # Update connection status
        self.update_connection_status()
    
    def update_connection_status(self):
        """Update the connection status label"""
        if self.main_window.sheets_service and self.main_window.sheets_service.is_connected():
            word_count = len(self.main_window.flashcard_manager.words_data) if self.main_window.flashcard_manager else 0
            self.connection_status.setText(f"Status: Connected ✓ ({word_count} words loaded)")
            self.connection_status.setStyleSheet("color: #27ae60; font-size: 14px; background: transparent; padding: 5px;")
        else:
            self.connection_status.setText("Status: Not Connected ✗")
            self.connection_status.setStyleSheet("color: #e74c3c; font-size: 14px; background: transparent; padding: 5px;")
    
    def connect_to_sheet(self):
        """Connect to the configured Google Sheet"""
        spreadsheet_id = self.spreadsheet_id_input.text().strip()
        sheet_gid = self.sheet_gid_input.text().strip()
        
        if not spreadsheet_id:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter a Spreadsheet ID."
            )
            return
        
        # Show loading status
        self.connection_status.setText("Connecting...")
        self.connection_status.setStyleSheet("color: #f39c12; font-size: 14px; background: transparent; padding: 5px;")
        self.connect_btn.setEnabled(False)
        
        try:
            # Import here to avoid circular dependency
            from services.google_sheets import GoogleSheetsService
            from services.flashcard_logic import FlashcardManager
            
            # Create new sheets service with provided ID
            sheets_service = GoogleSheetsService(spreadsheet_id, sheet_gid if sheet_gid else None)
            
            # Fetch words to test connection
            words_data = sheets_service.fetch_words()
            
            if not words_data:
                raise Exception("No words found in the spreadsheet. Please ensure your sheet has the correct format.")
            
            # Update main window's services
            self.main_window.sheets_service = sheets_service
            self.main_window.flashcard_manager = FlashcardManager(
                words_data,
                sheets_service,
                self.main_window.config
            )
            
            # Save to config
            self.main_window.config.set('spreadsheet_id', spreadsheet_id)
            self.main_window.config.set('sheet_gid', sheet_gid)
            self.main_window.config.save()
            
            # Update status
            self.update_connection_status()
            
            # Update home view
            self.main_window.update_home_view_connection()
            
            QMessageBox.information(
                self,
                "Success",
                f"Successfully connected to Google Sheet!\n{len(words_data)} words loaded."
            )
            
        except Exception as e:
            self.connection_status.setText("Status: Connection Failed ✗")
            self.connection_status.setStyleSheet("color: #e74c3c; font-size: 14px; background: transparent; padding: 5px;")
            
            QMessageBox.critical(
                self,
                "Connection Error",
                f"Failed to connect to Google Sheets:\n{str(e)}"
            )
        finally:
            self.connect_btn.setEnabled(True)
            
    def save_and_return(self):
        """Save settings and return to home"""
        config = self.main_window.config
        config.set('cards_per_session', self.cards_per_session.value())
        config.set('spreadsheet_id', self.spreadsheet_id_input.text().strip())
        config.set('sheet_gid', self.sheet_gid_input.text().strip())
        config.save()
        
        self.main_window.show_home()