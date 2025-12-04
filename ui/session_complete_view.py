"""
Session complete view showing statistics with skip count
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QGridLayout)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QFontMetrics
from ui.styles import Styles

class SessionCompleteView(QWidget):
    """View displayed when practice session is complete"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 30, 40, 30)
        
        # Title
        self.title = QLabel("🎉 Session Complete!")
        self.title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        self.title.setWordWrap(True)
        
        # Stats container
        self.stats_frame = QFrame()
        self.stats_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 30px;
                border: 2px solid #e5e5e5;
            }
        """)
        
        stats_grid = QGridLayout(self.stats_frame)
        stats_grid.setSpacing(20)
        stats_grid.setContentsMargins(20, 20, 20, 20)
        
        # Total Cards
        self.total_header = QLabel("Total Cards")
        self.total_header.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.total_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_header.setStyleSheet("color: #7f8c8d; text-transform: uppercase;")
        self.total_header.setWordWrap(True)
        
        self.total_cards_label = QLabel("0")
        self.total_cards_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.total_cards_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_cards_label.setStyleSheet("color: #34495e;")
        self.total_cards_label.setWordWrap(True)
        
        # Correct
        self.correct_header = QLabel("Correct")
        self.correct_header.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.correct_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.correct_header.setStyleSheet("color: #7f8c8d; text-transform: uppercase;")
        self.correct_header.setWordWrap(True)
        
        self.correct_label = QLabel("0")
        self.correct_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.correct_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.correct_label.setStyleSheet("color: #27ae60;")
        self.correct_label.setWordWrap(True)
        
        # Incorrect
        self.incorrect_header = QLabel("Incorrect")
        self.incorrect_header.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.incorrect_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.incorrect_header.setStyleSheet("color: #7f8c8d; text-transform: uppercase;")
        self.incorrect_header.setWordWrap(True)
        
        self.incorrect_label = QLabel("0")
        self.incorrect_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.incorrect_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.incorrect_label.setStyleSheet("color: #e74c3c;")
        self.incorrect_label.setWordWrap(True)
        
        # Skipped
        self.skipped_header = QLabel("Skipped")
        self.skipped_header.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.skipped_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.skipped_header.setStyleSheet("color: #7f8c8d; text-transform: uppercase;")
        self.skipped_header.setWordWrap(True)
        
        self.skipped_label = QLabel("0")
        self.skipped_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.skipped_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.skipped_label.setStyleSheet("color: #f39c12;")
        self.skipped_label.setWordWrap(True)
        
        # Accuracy
        self.accuracy_header = QLabel("Accuracy")
        self.accuracy_header.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.accuracy_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.accuracy_header.setStyleSheet("color: #7f8c8d; text-transform: uppercase;")
        self.accuracy_header.setWordWrap(True)
        
        self.accuracy_label = QLabel("0%")
        self.accuracy_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.accuracy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.accuracy_label.setStyleSheet("color: #3498db;")
        self.accuracy_label.setWordWrap(True)
        
        # Store all value labels for dynamic resizing
        self.value_labels = [
            self.total_cards_label,
            self.correct_label,
            self.incorrect_label,
            self.skipped_label,
            self.accuracy_label
        ]
        
        # Add to grid (row, column)
        # Row 0: Headers
        stats_grid.addWidget(self.total_header, 0, 0)
        stats_grid.addWidget(self.correct_header, 0, 1)
        stats_grid.addWidget(self.incorrect_header, 0, 2)
        stats_grid.addWidget(self.skipped_header, 0, 3)
        stats_grid.addWidget(self.accuracy_header, 0, 4)
        
        # Row 1: Values
        stats_grid.addWidget(self.total_cards_label, 1, 0)
        stats_grid.addWidget(self.correct_label, 1, 1)
        stats_grid.addWidget(self.incorrect_label, 1, 2)
        stats_grid.addWidget(self.skipped_label, 1, 3)
        stats_grid.addWidget(self.accuracy_label, 1, 4)
        
        # Make columns equally sized
        for col in range(5):
            stats_grid.setColumnStretch(col, 1)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        home_btn = QPushButton("Home")
        home_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        home_btn.setMinimumSize(150, 50)
        home_btn.clicked.connect(self.go_home)
        
        practice_again_btn = QPushButton("Practice Again")
        practice_again_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        practice_again_btn.setMinimumSize(150, 50)
        practice_again_btn.clicked.connect(self.start_new_session)
        
        button_layout.addStretch()
        button_layout.addWidget(home_btn)
        button_layout.addWidget(practice_again_btn)
        button_layout.addStretch()
        
        # Add all to main layout
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.stats_frame)
        layout.addLayout(button_layout)
        layout.addStretch()
        
    def show_stats(self, stats):
        """Display session statistics"""
        total = stats['total_cards']
        correct = stats['correct']
        incorrect = stats['incorrect']
        skipped = stats.get('skipped', 0)
        
        # Calculate accuracy (excluding skipped)
        reviewed = correct + incorrect
        accuracy = (correct / reviewed * 100) if reviewed > 0 else 0
        
        self.total_cards_label.setText(str(total))
        self.correct_label.setText(str(correct))
        self.incorrect_label.setText(str(incorrect))
        self.skipped_label.setText(str(skipped))
        self.accuracy_label.setText(f"{accuracy:.1f}%")
        
        # Adjust font sizes after a short delay to ensure widgets are rendered
        QTimer.singleShot(50, self.adjust_font_sizes)
    
    def adjust_font_sizes(self):
        """Dynamically adjust font sizes to fit available space"""
        # Get available width per column (total width / 5 columns - spacing)
        frame_width = self.stats_frame.width() - 40  # Subtract padding
        column_width = (frame_width - 80) / 5  # Subtract spacing between columns
        
        if column_width <= 0:
            return
        
        # Adjust each value label
        for label in self.value_labels:
            text = label.text()
            current_font_size = 24  # Starting font size
            min_font_size = 12       # Minimum readable size
            
            # Try decreasing font sizes until text fits
            while current_font_size >= min_font_size:
                font = QFont("Arial", current_font_size, QFont.Weight.Bold)
                metrics = QFontMetrics(font)
                text_width = metrics.horizontalAdvance(text)
                
                # Add some padding (10px on each side)
                if text_width <= column_width - 20:
                    label.setFont(font)
                    break
                
                current_font_size -= 1
            
            # If still too large, use minimum size
            if current_font_size < min_font_size:
                label.setFont(QFont("Arial", min_font_size, QFont.Weight.Bold))
        
        # Also adjust title if needed
        self.adjust_title_font()
    
    def adjust_title_font(self):
        """Adjust title font size to fit"""
        available_width = self.width() - 80  # Subtract margins
        if available_width <= 0:
            return
        
        text = self.title.text()
        current_font_size = 28
        min_font_size = 18
        
        while current_font_size >= min_font_size:
            font = QFont("Arial", current_font_size, QFont.Weight.Bold)
            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(text)
            
            if text_width <= available_width:
                self.title.setFont(font)
                break
            
            current_font_size -= 1
        
        if current_font_size < min_font_size:
            self.title.setFont(QFont("Arial", min_font_size, QFont.Weight.Bold))
    
    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        # Readjust fonts when window is resized
        QTimer.singleShot(50, self.adjust_font_sizes)
    
    def go_home(self):
        """Return to home screen"""
        self.main_window.show_home()
        
    def start_new_session(self):
        """Start a new practice session"""
        self.main_window.start_practice()