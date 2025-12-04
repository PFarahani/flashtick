"""
Flashcard Practice Application
Main entry point for the application
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
from services.config_manager import ConfigManager

def main():
    """Initialize and run the application"""
    config = ConfigManager()
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Flashcard Practice")
    app.setStyle('Fusion')
    
    # Set application icon (this affects taskbar on Windows/Linux)
    icon_paths = [
        "icon.png",
        "icon_256.png",
        "icon.ico",
        "assets/icon.png",
        "assets/icon.ico"
    ]
    
    icon_set = False
    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            app.setWindowIcon(app_icon)
            icon_set = True
            break
    
    window = MainWindow(config)
    
    if icon_set:
        window.setWindowIcon(app.windowIcon())
    
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()