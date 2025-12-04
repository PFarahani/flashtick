"""
UI styling constants for consistent design
"""

class Styles:
    """Centralized styling for the application"""
    
    GLOBAL_STYLE = """
        QWidget {
            background-color: #ecf0f1;
            font-family: 'Arial', 'Helvetica', sans-serif;
        }
        QMessageBox {
            background-color: #ecf0f1;
        }
        QMessageBox QLabel {
            color: #2c3e50;
            font-size: 14px;
        }
        QMessageBox QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 20px;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #2980b9;
        }
        QMessageBox QPushButton:focus {
            outline: none;
            border: none;
        }
    """
    
    PRIMARY_BUTTON = """
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 15px 30px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #21618c;
        }
        QPushButton:disabled {
            background-color: #bdc3c7;
        }
        QPushButton:focus {
            outline: none;
            border: none;
        }
    """
    
    SECONDARY_BUTTON = """
        QPushButton {
            background-color: #95a5a6;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
        }
        QPushButton:hover {
            background-color: #7f8c8d;
        }
        QPushButton:pressed {
            background-color: #6c7a7b;
        }
        QPushButton:focus {
            outline: none;
            border: none;
        }
    """
    
    CORRECT_BUTTON = """
        QPushButton {
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 15px 30px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #229954;
        }
        QPushButton:pressed {
            background-color: #1e8449;
        }
        QPushButton:focus {
            outline: none;
            border: none;
        }
    """
    
    INCORRECT_BUTTON = """
        QPushButton {
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 15px 30px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #c0392b;
        }
        QPushButton:pressed {
            background-color: #a93226;
        }
        QPushButton:focus {
            outline: none;
            border: none;
        }
    """
    
    SKIP_BUTTON = """
        QPushButton {
            background-color: #f39c12;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 15px 30px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #e67e22;
        }
        QPushButton:pressed {
            background-color: #d68910;
        }
        QPushButton:focus {
            outline: none;
            border: none;
        }
    """
    
    FLASHCARD = """
        QWidget {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            border: none;
        }
        QWidget:focus {
            outline: none;
            border: none;
        }
    """
    
    FLASHCARD_REVEALED = """
        QWidget {
            background-color: #e8f8f5;
            border-radius: 15px;
            padding: 20px;
            border: none;
        }
        QWidget:focus {
            outline: none;
            border: none;
        }
    """
    
    PROGRESS_BAR = """
        QProgressBar {
            border: none;
            border-radius: 4px;
            background-color: #d5dbdb;
        }
        QProgressBar::chunk {
            background-color: #3498db;
            border-radius: 4px;
        }
    """
    
    GROUP_BOX = """
        QGroupBox {
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            margin-top: 15px;
            padding: 20px;
            background-color: white;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            background-color: #ecf0f1;
            color: #2c3e50;
        }
        QGroupBox QLabel {
            background-color: transparent;
        }
    """
    
    SPIN_BOX = """
        QSpinBox {
            padding: 8px 10px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            font-size: 14px;
            color: #2c3e50;
            min-width: 100px;
        }
        QSpinBox:focus {
            border: 2px solid #3498db;
            outline: none;
        }
        QSpinBox::up-button {
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #bdc3c7;
            border-top-right-radius: 5px;
            background-color: #ecf0f1;
        }
        QSpinBox::up-button:hover {
            background-color: #3498db;
        }
        QSpinBox::up-arrow {
            image: none;
            width: 0px;
            height: 0px;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-bottom: 5px solid #2c3e50;
            margin: 0 auto;
        }
        QSpinBox::up-button:hover QSpinBox::up-arrow {
            border-bottom-color: white;
        }
        QSpinBox::down-button {
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-left: 1px solid #bdc3c7;
            border-bottom-right-radius: 5px;
            background-color: #ecf0f1;
        }
        QSpinBox::down-button:hover {
            background-color: #3498db;
        }
        QSpinBox::down-arrow {
            image: none;
            width: 0px;
            height: 0px;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #2c3e50;
            margin: 0 auto;
        }
        QSpinBox::down-button:hover QSpinBox::down-arrow {
            border-top-color: white;
        }
    """