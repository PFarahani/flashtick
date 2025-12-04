"""
Flashcard display view with fade animation and skip functionality
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QProgressBar, QScrollArea, QGraphicsOpacityEffect)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont
from ui.styles import Styles

class FlashcardView(QWidget):
    """View for displaying and interacting with flashcards"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.manager = None
        self.is_revealed = False
        self.animation_running = False
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)
        
        # Header with progress
        header_layout = QHBoxLayout()
        
        # Back button
        back_btn = QPushButton("← Home")
        back_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        back_btn.setMaximumWidth(120)
        back_btn.clicked.connect(self.main_window.show_home)
        
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        
        # Progress label
        self.progress_label = QLabel("Card 1 / 20")
        self.progress_label.setFont(QFont("Arial", 14))
        self.progress_label.setStyleSheet("color: #7f8c8d;")
        
        header_layout.addWidget(self.progress_label)
        layout.addLayout(header_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(Styles.PROGRESS_BAR)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximumHeight(8)
        layout.addWidget(self.progress_bar)
        
        # Flashcard container with proper structure for badge
        card_container_layout = QVBoxLayout()
        card_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Wrapper widget to hold both card and badge
        card_wrapper = QWidget()
        card_wrapper.setMinimumSize(600, 400)
        card_wrapper.setMaximumSize(700, 450)
        card_wrapper_layout = QVBoxLayout(card_wrapper)
        card_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        card_wrapper_layout.setSpacing(0)
        
        # Card widget with scroll area
        self.card = QWidget()
        self.card.setStyleSheet(Styles.FLASHCARD)
        self.card.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # Opacity effect for animation
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(1.0)
        self.card.setGraphicsEffect(self.opacity_effect)
        
        # New badge - positioned in top-right corner
        badge_container = QWidget()
        badge_container.setStyleSheet("background: transparent;")
        badge_layout = QHBoxLayout(badge_container)
        badge_layout.setContentsMargins(0, 15, 15, 0)
        badge_layout.addStretch()
        
        self.new_badge = QLabel("NEW")
        self.new_badge.setStyleSheet("""
            QLabel {
                background-color: #1CB0F6;
                color: white;
                padding: 6px 14px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
                border: none;
            }
        """)
        self.new_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.new_badge.setFixedHeight(26)
        self.new_badge.hide()
        
        badge_layout.addWidget(self.new_badge)
        
        badge_container.setGeometry(0, 0, 700, 50)
        badge_container.raise_()  # Ensure badge is on top
        
        # Scroll area for card content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #2980b9;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        scroll_content = QWidget()
        scroll_content.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Card text
        self.card_text = QLabel()
        self.card_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_text.setWordWrap(True)
        self.card_text.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        self.card_text.setStyleSheet("color: #2c3e50; padding: 20px; background: transparent;")
        self.card_text.setScaledContents(False)
        self.card_text.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # Side indicator
        self.side_indicator = QLabel("Front - Click to reveal")
        self.side_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.side_indicator.setFont(QFont("Arial", 12))
        self.side_indicator.setStyleSheet("color: #95a5a6; margin-top: 20px; background: transparent;")
        self.side_indicator.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # SRS stage indicator
        self.stage_indicator = QLabel()
        self.stage_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stage_indicator.setFont(QFont("Arial", 10))
        self.stage_indicator.setStyleSheet("color: #bdc3c7; margin-top: 10px; background: transparent;")
        self.stage_indicator.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        scroll_layout.addStretch()
        scroll_layout.addWidget(self.card_text)
        scroll_layout.addWidget(self.side_indicator)
        scroll_layout.addWidget(self.stage_indicator)
        scroll_layout.addStretch()
        
        self.scroll_area.setWidget(scroll_content)
        
        # Add scroll area to card
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.addWidget(self.scroll_area)
        
        # Make card clickable
        self.card.mousePressEvent = self.reveal_card
        
        # Add card to wrapper
        card_wrapper_layout.addWidget(self.card)
        badge_container.setParent(card_wrapper)
        badge_container.setGeometry(0, 0, 700, 50)
        badge_container.raise_()
        badge_container.setStyleSheet("background: transparent;")

        # Add wrapper to container
        card_container_layout.addWidget(card_wrapper)
        layout.addLayout(card_container_layout)
        
        # Action buttons (hidden initially)
        self.action_layout = QHBoxLayout()
        self.action_layout.setSpacing(15)
        self.action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.incorrect_btn = QPushButton("✗ Incorrect")
        self.incorrect_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.incorrect_btn.setMinimumSize(150, 60)
        self.incorrect_btn.setStyleSheet(Styles.INCORRECT_BUTTON)
        self.incorrect_btn.clicked.connect(lambda: self.handle_answer(False))
        
        self.correct_btn = QPushButton("✓ Correct")
        self.correct_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.correct_btn.setMinimumSize(150, 60)
        self.correct_btn.setStyleSheet(Styles.CORRECT_BUTTON)
        self.correct_btn.clicked.connect(lambda: self.handle_answer(True))
        
        # Skip button
        self.skip_btn = QPushButton("⏭ Skip")
        self.skip_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.skip_btn.setMinimumSize(120, 60)
        self.skip_btn.setStyleSheet(Styles.SKIP_BUTTON)
        self.skip_btn.clicked.connect(self.handle_skip)
        
        self.action_layout.addWidget(self.incorrect_btn)
        self.action_layout.addWidget(self.correct_btn)
        self.action_layout.addWidget(self.skip_btn)
        
        self.action_widget = QWidget()
        self.action_widget.setLayout(self.action_layout)
        self.action_widget.setVisible(False)
        
        layout.addWidget(self.action_widget)
        layout.addStretch()
        
    def load_session(self, manager):
        """Load a new practice session"""
        self.manager = manager
        self.show_current_card()
        
    def show_current_card(self):
        """Display the current flashcard"""
        if not self.manager or not self.manager.has_next_card():
            return
            
        self.is_revealed = False
        self.action_widget.setVisible(False)
        
        # Update progress
        current = self.manager.current_index + 1
        total = self.manager.session_size
        self.progress_label.setText(f"Card {current} / {total}")
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        
        # Show front of the card
        card = self.manager.get_current_card()
        self.update_card_text(card.front)
        self.side_indicator.setText("Front - Click to reveal")
        
        # Show SRS stage
        stage_text = f"Stage {card.srs_stage}/8"
        if card.srs_stage == 0:
            stage_text += " (Learning)"
        elif card.srs_stage >= 6:
            stage_text += " (Mastered)"
        self.stage_indicator.setText(stage_text)
        
        # Show NEW badge if card is new
        if card.is_new():
            self.new_badge.show()
        else:
            self.new_badge.hide()
        
        self.card.setStyleSheet(Styles.FLASHCARD)
        
        # Reset opacity
        self.opacity_effect.setOpacity(1.0)
        
        # Reset scroll position
        self.scroll_area.verticalScrollBar().setValue(0)
        
    def update_card_text(self, text):
        """Update card text with dynamic font sizing"""
        self.card_text.setText(text)
        
        text_length = len(text)
        
        if text_length < 20:
            font_size = 32
        elif text_length < 40:
            font_size = 28
        elif text_length < 60:
            font_size = 24
        elif text_length < 100:
            font_size = 20
        else:
            font_size = 18
            
        self.card_text.setFont(QFont("Arial", font_size, QFont.Weight.Bold))
        
    def reveal_card(self, event):
        """Animate card reveal to show the back side"""
        if self.animation_running or self.is_revealed or not self.manager:
            return
            
        self.animation_running = True
        card = self.manager.get_current_card()
        
        # Create fade out animation
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(250)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.finished.connect(lambda: self.reveal_complete(card))
        self.animation.start()
        
    def reveal_complete(self, card):
        """Complete the reveal by showing the back side"""
        self.update_card_text(card.back)
        self.side_indicator.setText("Back")
        self.card.setStyleSheet(Styles.FLASHCARD_REVEALED)
        self.is_revealed = True
        
        # Reset scroll position for new content
        self.scroll_area.verticalScrollBar().setValue(0)
        
        # Create fade in animation
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(250)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.finished.connect(self.show_action_buttons)
        self.animation.start()
        
    def show_action_buttons(self):
        """Show correct/incorrect buttons after reveal"""
        self.animation_running = False
        self.action_widget.setVisible(True)
        
    def handle_answer(self, is_correct):
        """Handle user's answer (correct/incorrect)"""
        if not self.manager:
            return
            
        # Record answer
        self.manager.record_answer(is_correct)
        
        # Move to next card or finish session
        if self.manager.has_next_card():
            self.manager.next_card()
            self.show_current_card()
        else:
            stats = self.manager.get_session_stats()
            self.main_window.show_session_complete(stats)
    
    def handle_skip(self):
        """Handle skip button click"""
        if not self.manager:
            return
        
        # Skip card (adds it back to queue)
        self.manager.skip_card()
        
        # Show next card or finish
        if self.manager.has_next_card():
            self.show_current_card()
        else:
            stats = self.manager.get_session_stats()
            self.main_window.show_session_complete(stats)