"""
Flashcard data model with Tick-8 SRS support
"""

class Flashcard:
    """Represents a single flashcard with Tick-8 SRS metadata"""
    
    MAX_STAGE = 8  # Mastery stage
    
    def __init__(self, data: dict):
        """Initialize flashcard from dictionary"""
        self.row_index = data['row_index']
        self.front = data['front']
        self.back = data['back']
        self.last_practice_date = data['last_practice_date']
        self.srs_stage = data.get('srs_stage', 0)  # SRS stage 0-8
        self.failed_count = data.get('failed_count', 0)  # Number of failures
        
    def is_new(self) -> bool:
        """Check if this is a new word (never practiced)"""
        return not self.last_practice_date or self.last_practice_date == ''
    
    def is_due_today(self, today: str) -> bool:
        """Check if this card is due for review today (Tick-8 method)"""
        # Mastered cards are not due
        if self.is_mastered():
            return False
        
        # New cards are always due
        if self.is_new():
            return True
        
        # In Tick-8, if practiced yesterday or before, it's due today
        return self.last_practice_date < today
    
    def is_mastered(self) -> bool:
        """Check if card has reached mastery"""
        return self.srs_stage >= self.MAX_STAGE
        
    def __repr__(self):
        return f"Flashcard({self.front} -> {self.back}, Stage: {self.srs_stage})"