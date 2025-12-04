"""
Configuration management
"""

import json
import os

class ConfigManager:
    """Manages application configuration"""
    
    CONFIG_FILE = 'config/config.json'
    DEFAULT_CONFIG = {
        'cards_per_session': 20,
        'spreadsheet_id': '',
        'sheet_gid': ''
    }
    
    def __init__(self):
        """Initialize configuration"""
        self.config = self.load()
        
    def load(self) -> dict:
        """Load configuration from file"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    return {**self.DEFAULT_CONFIG, **json.load(f)}
            except:
                pass
        return self.DEFAULT_CONFIG.copy()
        
    def save(self):
        """Save configuration to file"""
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
        
    def set(self, key: str, value):
        """Set configuration value"""
        self.config[key] = value