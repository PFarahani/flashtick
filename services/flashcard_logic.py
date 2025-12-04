"""
Flashcard selection and session management logic with Tick-8 SRS
"""

from datetime import datetime
from typing import List, Dict, Optional, Set
from models.flashcard import Flashcard

class FlashcardManager:
    """Manages flashcard selection and practice sessions with Tick-8 SRS"""
    
    MAX_STAGE = 8
    
    def __init__(self, words_data: List[Dict], sheets_service, config):
        """Initialize the flashcard manager"""
        self.words_data = words_data
        self.sheets_service = sheets_service
        self.config = config
        self.session_cards = []
        self.current_index = 0
        self.session_size = 0
        self.session_stats = {'correct': 0, 'incorrect': 0, 'skipped': 0}
        self.session_active = False
        self.seen_card_ids = set()  # Track which cards have been SEEN (shown to user)
        
    def get_due_cards_count(self) -> int:
        """Get count of cards due for review today"""
        today = datetime.now().strftime('%Y-%m-%d')
        due_count = sum(1 for word in self.words_data 
                       if self._is_card_due(word, today))
        return due_count
    
    def _is_card_due(self, word: Dict, today: str) -> bool:
        """Check if a card is due for review"""
        temp_card = Flashcard(word)
        return temp_card.is_due_today(today)
        
    def start_new_session(self, force_new=False):
        """Start a new practice session or resume existing one"""
        if self.session_active and not force_new and self.has_next_card():
            return
        
        # Reset stats for completely new session
        self.session_stats = {'correct': 0, 'incorrect': 0, 'skipped': 0}
        self.current_index = 0
        self.seen_card_ids = set()  # Reset seen cards tracker
        
        # Select cards based on due date and priority
        selected = self._select_cards()
        
        # Convert to Flashcard objects
        self.session_cards = [Flashcard(data) for data in selected]
        self.session_size = len(self.session_cards)
        self.session_active = True
        
    def _select_cards(self) -> List[Dict]:
        """Select cards due for review based on Tick-8 SRS"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Filter to only cards due today
        due_cards = [word for word in self.words_data 
                    if self._is_card_due(word, today)]
        
        if not due_cards:
            return []
        
        # Prioritize by:
        # 1. Failed cards with failures (stage 0 + has been practiced before)
        # 2. New failed cards (stage 0 + never practiced)
        # 3. Lower stages (less progress)
        # 4. Failed count (more failures = higher priority)
        for word in due_cards:
            stage = word.get('srs_stage', 0)
            failed = word.get('failed_count', 0)
            is_new = not word.get('last_practice_date')
            
            # Priority score
            priority = 0
            
            # FIXED LOGIC:
            if stage == 0 and not is_new:
                # Failed cards (practiced before, now at stage 0)
                priority += 2000  # HIGHEST priority
            elif stage == 0 and is_new:
                # New cards (never practiced)
                priority += 1000  # Second priority
            else:
                # Cards in progress (stages 1-7)
                priority += (10 - stage) * 10  # Lower stages = higher priority
            
            # Add bonus for more failures
            priority += failed * 50  # Increased weight for failed cards
            
            word['priority_score'] = priority
        
        # Sort by priority
        sorted_cards = sorted(due_cards, key=lambda x: x['priority_score'], reverse=True)
        
        # Take up to batch size
        cards_per_session = self.config.get('cards_per_session', 20)
        return sorted_cards[:min(cards_per_session, len(sorted_cards))]
        
    def get_current_card(self) -> Optional[Flashcard]:
        """Get the current flashcard"""
        if 0 <= self.current_index < len(self.session_cards):
            card = self.session_cards[self.current_index]
            # Mark as seen when retrieved
            self.seen_card_ids.add(card.row_index)
            return card
        return None
        
    def has_next_card(self) -> bool:
        """Check if there are more cards in the session"""
        # Session ends when we've seen enough unique cards
        if len(self.seen_card_ids) >= self.session_size:
            return False
        
        # Also check if there are cards in the queue
        return self.current_index < len(self.session_cards)
        
    def next_card(self):
        """Move to the next card"""
        self.current_index += 1
        
    def skip_card(self):
        """Skip the current card (counts toward batch size)"""
        card = self.get_current_card()
        if card:
            self.session_stats['skipped'] += 1
            self.next_card()
        
    def record_answer(self, is_correct: bool):
        """Record user's answer and update SRS data"""
        card = self.get_current_card()
        if not card:
            return
        
        if is_correct:
            self.session_stats['correct'] += 1
        else:
            self.session_stats['incorrect'] += 1
        
        if is_correct:
            new_stage = min(card.srs_stage + 1, self.MAX_STAGE)
        else:
            new_stage = 0  # Reset to beginning on wrong answer
        
        # Update Google Sheets
        self.sheets_service.update_word_stats(
            card.row_index,
            is_correct,
            new_stage
        )
        
        # Update local data
        for word in self.words_data:
            if word['row_index'] == card.row_index:
                word['last_practice_date'] = datetime.now().strftime('%Y-%m-%d')
                word['srs_stage'] = new_stage
                if not is_correct:
                    word['failed_count'] += 1
                break
            
    def end_session(self):
        """Mark session as complete"""
        self.session_active = False
        self.session_cards = []
        self.current_index = 0
        self.seen_card_ids = set()
            
    def get_session_stats(self) -> Dict:
        """Get current session statistics"""
        return {
            'total_cards': len(self.seen_card_ids),  # How many cards were actually seen
            'correct': self.session_stats['correct'],
            'incorrect': self.session_stats['incorrect'],
            'skipped': self.session_stats['skipped'],
            'remaining': self.session_size - len(self.seen_card_ids)
        }
    
    def get_session_progress(self) -> Dict:
        """Get current session progress info"""
        return {
            'current': len(self.seen_card_ids),
            'total': self.session_size,
            'completed': len(self.seen_card_ids),
            'remaining': self.session_size - len(self.seen_card_ids),
            'is_active': self.session_active
        }