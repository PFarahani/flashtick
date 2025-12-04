"""
Main window containing flashcard view and settings
"""

import os
from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QVBoxLayout, 
                             QWidget, QPushButton, QHBoxLayout, QLabel,
                             QMessageBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon
from ui.flashcard_view import FlashcardView
from ui.settings_view import SettingsView
from ui.session_complete_view import SessionCompleteView
from services.google_sheets import GoogleSheetsService
from services.flashcard_logic import FlashcardManager
from ui.styles import Styles

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.sheets_service = None
        self.flashcard_manager = None
        
        self.setWindowTitle("Flashcard Practice")
        self.setMinimumSize(900, 700)
        
        # Set window icon
        self.set_window_icon()
        
        # Apply global stylesheet
        self.setStyleSheet(Styles.GLOBAL_STYLE)
        
        self.init_ui()
        self.init_services()
    
    def set_window_icon(self):
        """Set the window icon"""
        # Try multiple icon paths
        icon_paths = [
            "icon.png",
            "icon.ico",
            "assets/icon.png",
            "assets/icon.ico",
            os.path.join(os.path.dirname(__file__), ". .", "icon.png"),
            os.path.join(os.path.dirname(__file__), "..", "icon.ico"),
        ]
        
        for path in icon_paths:
            if os.path.exists(path):
                self.setWindowIcon(QIcon(path))
                return
        
        # If no icon found, create a simple one in memory
        self.create_simple_icon()
    
    def create_simple_icon(self):
        """Create icon from embedded SVG"""
        from PySide6.QtSvg import QSvgRenderer
        from PySide6.QtGui import QPixmap, QPainter
        from PySide6.QtCore import QByteArray
        
        # Embedded SVG (minified)
        svg_data = b'''<?xml version="1.0" encoding="UTF-8"?>
        <svg width="100%" height="100%" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;"><g><path d="M0.3,223.541c6.053,-120.578 102.966,-217.381 223.59,-223.258c29.257,-0.211 121.185,-0.255 290.11,-0.133l287.293,0.193c119.688,6.43 215.755,102.394 222.346,222.039c0.183,29.827 0.304,102.451 0.361,187.005l0,230.798c-0.052,73.687 -0.159,134.842 -0.321,160.685c-3.156,60.776 -29.397,115.486 -70.113,155.521c-17.507,17.036 -38.269,31.935 -59.316,42.458c-4.404,2.202 -8.661,4.225 -12.839,6.078c-25.004,10.761 -52.239,17.314 -80.811,18.765c-35.26,0.179 -138.366,0.307 -288.649,0.307c-159.017,0 -255.257,-0.094 -288.524,-0.306c-35.338,-1.791 -68.632,-11.386 -98.19,-27.095c-11.727,-6.273 -22.924,-13.509 -33.236,-21.549c-19.403,-15.091 -36.538,-33.169 -50.363,-52.891c-24.308,-35.172 -39.297,-77.267 -41.386,-122.705l0.048,-288.454l0,-287.459Zm723.65,696.309c13.65,-2.85 28.65,-9.4 38.95,-16.95c22.95,-16.8 36.95,-39.3 41.5,-66.55c0.75,-4.75 0.85,-26.6 1,-314.85c0.1,-209.55 0,-311.8 -0.35,-316.1c-2.2,-27.15 -12.4,-49.3 -31.2,-67.9c-16.6,-16.5 -36.1,-26.1 -60.35,-29.85c-5.45,-0.85 -16.5,-0.9 -202.5,-0.9l-196.75,0l-6.25,1.15c-24.15,4.4 -43.05,14.3 -59.7,31.3c-8.35,8.6 -13.45,15.8 -18.8,26.95c-5,10.25 -7.5,18.2 -9.6,30.1l-1.15,6.5l0,312.25c0,247.6 0.15,313.3 0.65,317.45c1.65,13.95 7.35,30.7 13.9,41.15c5.25,8.35 14.75,18.9 23.2,25.75c14.8,11.95 34.05,19.85 53,21.8c0.95,0.1 93.1,0.15 204.75,0.15l203,-0.05l6.7,-1.4Z" style="fill:#5ac4d0;"/></g><g><path d="M761.549,509.201c0.168,13.397 0.284,78.976 0.239,157.149c-0.101,145.8 -0.151,159.8 -0.907,163.9c-3.074,16.55 -12.447,30.75 -26.304,39.9c-8.315,5.5 -16.226,8.6 -25.196,9.85c-4.283,0.6 -372.289,1.05 -387.205,0.45c-13.001,-0.5 -22.626,-3.65 -33.006,-10.85c-14.865,-10.3 -24.49,-26.4 -26.455,-44.2c-0.664,-6.307 -0.703,-283.933 -0.117,-316.118c0.037,-2.006 0.076,-3.059 0.117,-3.032c0.162,0.107 0.542,0.661 1.008,1.453c0.402,0.683 0.867,1.544 1.31,2.447c5.14,10.15 12.043,19.5 20.761,28.2c21.97,21.95 48.678,34.15 79.063,36.15c22.525,1.5 46.259,-3.65 65.659,-14.25c22.525,-12.35 41.169,-31.75 52.004,-54.25c3.779,-7.8 5.039,-11.1 6.954,-17.9c3.376,-12.1 4.535,-20.55 4.535,-32.7c0,-10.25 -0.554,-9.15 6.299,-11.95c3.93,-1.6 4.233,-1.65 11.338,-1.7c5.694,0 7.911,0.2 10.078,0.9c5.341,1.7 8.012,2.95 8.264,3.8c0.151,0.45 0.252,4.3 0.202,8.55c-0.05,8.55 0.302,13.15 1.411,19.5c1.26,6.85 4.132,17.4 6.047,22c1.008,2.35 2.066,4.95 2.368,5.75c1.109,3.05 6.349,12.75 9.171,17.05c6.5,9.85 17.234,21.5 26.455,28.8c22.626,17.8 48.123,26.7 76.342,26.6c28.37,-0.1 53.263,-8.8 75.788,-26.6c12.598,-9.95 25.851,-25.95 31.696,-38.25c0.257,-0.524 0.514,-1.016 0.755,-1.448c0.61,-1.095 1.116,-1.809 1.261,-1.702c0.022,0.011 0.043,0.868 0.064,2.501Zm-235.541,116.299c4.888,-1.3 12.195,-4.65 16.78,-7.7c10.884,-7.15 20.408,-21.75 21.114,-32.3c0.202,-3.4 0.101,-4 -1.209,-6.5c-2.066,-4 -5.089,-5.75 -9.927,-5.75c-6.5,0 -9.474,2.7 -12.144,11.1c-1.663,5.25 -4.586,9.55 -8.768,12.9c-4.334,3.5 -9.02,5.65 -14.261,6.55c-9.877,1.8 -18.846,-0.9 -26.354,-7.85c-3.981,-3.75 -5.845,-6.6 -7.559,-11.7c-1.814,-5.3 -2.318,-6.25 -4.737,-8.4c-7.206,-6.45 -18.695,-1.3 -18.695,8.35c0,4.9 2.872,12.35 7.407,19.3c7.609,11.6 19.3,19.45 33.409,22.55c6.047,1.3 19.098,1.05 24.944,-0.55Z" style="fill:#fff;"/><path id="EyeR" d="M650.304,367.663c48.017,0 87,38.983 87,87c0,48.017 -38.983,87 -87,87c-48.017,0 -87,-38.983 -87,-87c0,-48.017 38.983,-87 87,-87Zm-25.912,60.475c-16.344,0 -29.613,13.269 -29.613,29.613c0,16.344 13.269,29.613 29.613,29.613c16.344,0 29.613,-13.269 29.613,-29.613c0,-16.344 -13.269,-29.613 -29.613,-29.613Z" style="fill:#fff;"/><path id="EyeL" d="M373.961,367.663c-48.017,0 -87,38.983 -87,87c0,48.017 38.983,87 87,87c48.017,0 87,-38.983 87,-87c0,-48.017 -38.983,-87 -87,-87Zm25.912,60.475c16.344,0 29.613,13.269 29.613,29.613c0,16.344 -13.269,29.613 -29.613,29.613c-16.344,0 -29.613,-13.269 -29.613,-29.613c0,-16.344 13.269,-29.613 29.613,-29.613Z" style="fill:#fff;"/><path d="M262.527,400.193c-0.499,-24.148 -0.367,-185.634 0.238,-192.143c1.764,-18.75 11.338,-35.15 26.556,-45.45c7.156,-4.85 14.462,-7.85 23.785,-9.7c2.671,-0.55 39.759,-0.65 199.044,-0.65c186.598,0 195.971,0.05 200.254,0.9c25.145,5.1 43.941,24.15 48.426,49.1c0.705,4 0.857,15.2 1.008,102.9c0.084,50.591 0.028,85.23 -0.17,95.14c-0.039,1.951 -0.083,2.943 -0.133,2.91c-0.128,-0.076 -0.527,-0.717 -1.067,-1.688c-0.526,-0.946 -1.185,-2.205 -1.856,-3.562c-2.57,-5.1 -8.113,-13.5 -13.051,-19.7c-6.148,-7.75 -17.838,-18 -27.564,-24.25c-2.469,-1.6 -4.938,-3.25 -5.392,-3.7c-0.504,-0.45 -1.008,-0.8 -1.159,-0.8l-0.655,0c-0.252,0 -0.907,-0.45 -1.512,-1c-0.605,-0.6 -1.109,-0.9 -1.109,-0.75c0,0.15 -0.655,-0.05 -1.512,-0.5c-4.334,-2.2 -16.679,-6.8 -22.676,-8.4c-10.784,-2.9 -17.637,-3.9 -28.723,-4.2c-20.459,-0.55 -37.793,3.05 -56.69,11.85c-17.385,8.05 -34.467,22.25 -45.352,37.75c-1.361,1.95 -2.62,3.6 -2.772,3.75c-0.454,0.4 -3.023,4.45 -3.023,4.75c0,0.15 -0.806,1.55 -1.764,3.05c-1.965,3 -4.737,8.75 -7.055,14.6c-0.504,1.15 -1.159,2.1 -1.461,2.1c-0.353,0 -2.318,-0.6 -4.384,-1.3c-6.954,-2.4 -11.691,-3.2 -19.753,-3.2c-8.365,0 -14.563,1 -21.719,3.55c-4.838,1.7 -4.686,1.7 -5.341,0.5c-0.252,-0.55 -0.504,-1.25 -0.504,-1.55c0,-1.2 -5.543,-12.8 -8.315,-17.3c-2.57,-4.2 -2.57,-4.2 -8.315,-11.95c-9.171,-12.35 -23.432,-24.35 -38.045,-32.1c-15.571,-8.2 -26.808,-11.7 -44.798,-13.9c-14.361,-1.75 -32.401,-0.35 -45.654,3.6c-19.703,5.85 -33.359,13.25 -49.131,26.75c-9.474,8.1 -20.106,21.6 -25.901,32.9c-0.553,1.074 -1.106,2.096 -1.562,2.913c-0.542,0.97 -0.949,1.651 -1.058,1.787c-0.05,0.058 -0.096,-1.001 -0.138,-3.007Z" style="fill:#fff;"/></g><g><path d="M307.853,922.65c-18.95,-1.95 -38.2,-9.85 -53,-21.8c-8.45,-6.85 -17.95,-17.4 -23.2,-25.75c-6.55,-10.45 -12.25,-27.2 -13.9,-41.15c-0.5,-4.15 -0.65,-70.1 -0.65,-318.95l0,-313.75l1.15,-6.5c2.1,-11.9 4.6,-19.85 9.6,-30.1c5.35,-11.15 10.45,-18.35 18.8,-26.95c16.65,-17 35.55,-26.9 59.7,-31.3l6.25,-1.15l198.25,0c187.4,0 198.55,0.05 204,0.9c24.25,3.75 43.75,13.35 60.35,29.85c18.8,18.6 29,40.75 31.2,67.9c0.35,4.3 0.45,107.05 0.35,317.6c-0.15,289.65 -0.25,311.6 -1,316.35c-1.65,9.75 -4.9,20 -9.35,29.4c-2.05,4.25 -7.5,12.7 -11.05,17.25c-5.1,6.35 -13.65,14.45 -21.1,19.9c-10.3,7.55 -25.3,14.1 -38.95,16.95l-6.7,1.4l-204.5,0.05c-112.5,0 -205.3,-0.05 -206.25,-0.15Zm-43.794,-513.363l-0.006,0.013c-0.75,1.65 -2.2,5.55 -3.25,8.7l-1.9,5.75l-7.15,0.3c-8.55,0.35 -10.85,1.05 -14.6,4.5c-6.45,5.9 -6.75,14.15 -0.75,20.7c3.45,3.75 6.25,4.9 12.45,5.25l5.25,0.25l0.35,4c1.4,16.85 3.95,28.2 9.1,41l0.506,1.25l0,314.111c0,35.592 28.897,64.489 64.489,64.489l367.091,0c35.592,0 64.489,-28.897 64.489,-64.489l0,-315.693l0.525,-1.318c4.8,-11.85 7.7,-25.05 8.5,-38.7l0.3,-4.8l5.3,-0.2c6.35,-0.2 9,-1.2 12.7,-5c5.9,-6.05 5.75,-13.85 -0.4,-20.4c-3.6,-3.85 -6.05,-4.65 -14.85,-4.9l-7.35,-0.2l-1.3,-4.25c-0.7,-2.35 -2.2,-6.45 -3.3,-9.1l-0.125,-0.3l0,-193.266c0,-35.592 -28.897,-64.489 -64.489,-64.489l-367.091,0c-35.592,0 -64.489,28.897 -64.489,64.489l0,192.303Z" style="fill:#0c7b95;"/></g><g><path d="M499.5,627.55c-19,-4.2 -33.85,-17.7 -39.5,-35.9c-1.4,-4.55 -1.4,-10.85 0.05,-13.95c1.9,-4 5.85,-6.15 11.45,-6.2c4.4,0 6.7,0.7 9.05,2.85c2.4,2.15 2.9,3.1 4.7,8.4c1.7,5.1 3.55,7.95 7.5,11.65c11.25,10.55 25.3,11.05 37.3,1.35c4.15,-3.35 7.05,-7.65 8.7,-12.9c1.8,-5.65 3.3,-8.05 6.15,-9.7c2.15,-1.3 2.8,-1.4 7.4,-1.4c4.7,0 5.2,0.1 7.5,1.5c1.85,1.15 2.8,2.2 3.85,4.25c1.35,2.6 1.4,3 1.2,8c-0.25,6 -1.5,9.95 -4.95,16.1c-3.75,6.7 -10.25,13.9 -16,17.7c-4.5,3 -11.8,6.4 -16.65,7.7c-5.8,1.6 -21.55,1.9 -27.75,0.55Z" style="fill:#252223;fill-rule:nonzero;"/><circle cx="399.115" cy="457.606" r="30.5" style="fill:#252223;"/><circle cx="625.06" cy="457.672" r="30.5" style="fill:#252223;"/></g><g><path d="M251.227,456.177l-3.727,-0.177c-2.168,-0.122 -3.92,-0.343 -5.429,-0.737c-2.716,-0.667 -4.641,-1.951 -6.989,-4.363c-3.124,-3.217 -4.378,-6.435 -4.331,-11.315l-0.001,-0.335c0,-5.75 1.25,-8.75 5.05,-12.2c0.438,-0.403 0.856,-0.768 1.266,-1.1c2.298,-2.002 4.59,-2.801 9.145,-3.152c1.211,-0.106 2.591,-0.183 4.188,-0.249l5.118,-0.215c14.21,-52.224 62.001,-90.672 118.7,-90.672c52.202,0 96.852,32.59 114.697,78.517l2.117,-0.73c6.4,-2.25 10.95,-2.95 20.3,-2.95l0.759,0.002l0.759,-0.002c9.35,0 13.9,0.7 20.3,2.95l2.341,0.807c17.825,-45.967 62.496,-78.594 114.727,-78.594c56.704,0 104.497,38.453 118.703,90.683l4.861,0.204c1.598,0.065 2.977,0.143 4.188,0.249c4.555,0.351 6.847,1.15 9.145,3.152c0.411,0.332 0.829,0.697 1.266,1.1c3.8,3.45 5.05,6.45 5.05,12.2l-0.001,0.335c0.048,4.88 -1.207,8.097 -4.331,11.315c-2.348,2.411 -4.273,3.695 -6.989,4.363c-1.51,0.395 -3.262,0.615 -5.429,0.737l-3.473,0.165c-0.806,67.195 -55.607,121.498 -122.991,121.498c-67.886,0 -123,-55.114 -123,-123c0,-2.528 0.076,-5.037 0.227,-7.527c-0.076,-0.062 -2.648,-1.211 -5.013,-2.185c-3.917,-1.402 -5.893,-1.679 -10.341,-1.699c-4.448,0.021 -6.424,0.298 -10.341,1.699c-2.366,0.974 -3.842,1.476 -4.761,2.148c0.152,2.502 0.229,5.024 0.229,7.565c0,67.886 -55.114,123 -123,123c-67.38,0 -122.178,-54.297 -122.991,-121.486Zm398.991,-87.614c-47.52,0 -86.1,38.58 -86.1,86.1c0,47.52 38.58,86.1 86.1,86.1c47.52,0 86.1,-38.58 86.1,-86.1c0,-47.52 -38.58,-86.1 -86.1,-86.1Zm-276,0c-47.52,0 -86.1,38.58 -86.1,86.1c0,47.52 38.58,86.1 86.1,86.1c47.52,0 86.1,-38.58 86.1,-86.1c0,-47.52 -38.58,-86.1 -86.1,-86.1Z" style="fill:#f7c528;"/></g></svg>
        '''
        
        renderer = QSvgRenderer(QByteArray(svg_data))
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        self.setWindowIcon(QIcon(pixmap))

    def init_ui(self):
        """Initialize the user interface"""
        # Central widget with stacked layout for different views
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Create views
        self.flashcard_view = FlashcardView(self)
        self.settings_view = SettingsView(self)
        self.session_complete_view = SessionCompleteView(self)
        
        # Add views to stack
        self.stack.addWidget(self.create_home_view())
        self.stack.addWidget(self.flashcard_view)
        self.stack.addWidget(self.settings_view)
        self.stack.addWidget(self.session_complete_view)
        
        # Show home view
        self.stack.setCurrentIndex(0)
        
    def create_home_view(self):
        """Create the home screen"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        
        # Title
        title = QLabel("Flashcard Practice")
        title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        
        # Subtitle
        subtitle = QLabel("Master any subject with smart spaced repetition")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 40px;")
        
        # Connection status
        self.status_label = QLabel("Not connected to Google Sheets")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #95a5a6; margin-bottom: 20px;")
        
        # NEW: SRS Info label
        self.srs_info_label = QLabel("")
        self.srs_info_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        self.srs_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.srs_info_label.setStyleSheet("""
            background-color: #E0F2FE;
            color: #005F99;
            border: 2px solid #3498db;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
        """)
        self.srs_info_label.setVisible(False)
        
        # Session status label (for resume info)
        self.session_status_label = QLabel("")
        self.session_status_label.setFont(QFont("Arial", 13))
        self.session_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.session_status_label.setStyleSheet("color: #e67e22; margin-bottom: 10px; font-weight: bold;")
        self.session_status_label.setVisible(False)
        
        # Start button
        self.start_button = QPushButton("Start Practice")
        self.start_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.start_button.setMinimumSize(250, 60)
        self.start_button.setStyleSheet(Styles.PRIMARY_BUTTON)
        self.start_button.clicked.connect(self.start_practice)
        self.start_button.setEnabled(False)
        
        # New session button (hidden by default)
        self.new_session_button = QPushButton("Start New Session")
        self.new_session_button.setFont(QFont("Arial", 14))
        self.new_session_button.setMinimumSize(250, 50)
        self.new_session_button.setStyleSheet(Styles.SECONDARY_BUTTON)
        self.new_session_button.clicked.connect(self.start_new_session)
        self.new_session_button.setVisible(False)
        
        # Settings button
        settings_button = QPushButton("⚙ Settings")
        settings_button.setFont(QFont("Arial", 14))
        settings_button.setMinimumSize(250, 50)
        settings_button.setStyleSheet(Styles.SECONDARY_BUTTON)
        settings_button.clicked.connect(self.show_settings)
        
        # Add widgets
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.status_label)
        layout.addWidget(self.srs_info_label)
        layout.addWidget(self.session_status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.new_session_button)
        layout.addWidget(settings_button)
        layout.addStretch()
        
        return widget
        
    def init_services(self):
        """Initialize Google Sheets and flashcard services"""
        QTimer.singleShot(100, self._init_services_async)
        
    def _init_services_async(self):
        """Async initialization of services"""
        # Check if we have saved spreadsheet configuration
        spreadsheet_id = self.config.get('spreadsheet_id', '')
        sheet_gid = self.config.get('sheet_gid', '')
        
        if not spreadsheet_id:
            self.status_label.setText("⚙ Please configure your Google Sheet in Settings")
            self.status_label.setStyleSheet("color: #f39c12; margin-bottom: 20px;")
            return
        
        try:
            self.status_label.setText("Connecting to Google Sheets...")
            self.status_label.setStyleSheet("color: #95a5a6; margin-bottom: 20px;")
            
            # Initialize Google Sheets service with saved config
            self.sheets_service = GoogleSheetsService(spreadsheet_id, sheet_gid if sheet_gid else None)
            
            # Fetch initial data
            words_data = self.sheets_service.fetch_words()
            
            if not words_data:
                raise Exception("No words found in the spreadsheet")
            
            # Initialize flashcard manager
            self.flashcard_manager = FlashcardManager(
                words_data, 
                self.sheets_service,
                self.config
            )
            
            # Update UI
            self.status_label.setText(f"✓ Connected - {len(words_data)} words loaded")
            self.status_label.setStyleSheet("color: #27ae60; margin-bottom: 20px;")
            self.start_button.setEnabled(True)
            
            # Show SRS info
            self.update_srs_info()
            
        except Exception as e:
            self.status_label.setText(f"✗ Connection failed - Please check Settings")
            self.status_label.setStyleSheet("color: #e74c3c; margin-bottom: 20px;")
    
    def update_srs_info(self):
        """Update SRS information on home screen"""
        if not self.flashcard_manager:
            return
        
        due_count = self.flashcard_manager.get_due_cards_count()
        
        if due_count > 0:
            self.srs_info_label.setText(f"📊 {due_count} cards due for review today")
            self.srs_info_label.setVisible(True)
        else:
            self.srs_info_label.setText("🎉 All caught up! No cards due today.")
            self.srs_info_label.setVisible(True)
    
    def update_home_view_connection(self):
        """Update home view connection status"""
        if self.sheets_service and self.sheets_service.is_connected() and self.flashcard_manager:
            word_count = len(self.flashcard_manager.words_data)
            self.status_label.setText(f"✓ Connected - {word_count} words loaded")
            self.status_label.setStyleSheet("color: #27ae60; margin-bottom: 20px;")
            self.start_button.setEnabled(True)
            self.update_srs_info()
        else:
            self.status_label.setText("✗ Not connected - Please configure in Settings")
            self.status_label.setStyleSheet("color: #e74c3c; margin-bottom: 20px;")
            self.start_button.setEnabled(False)
            self.srs_info_label.setVisible(False)
            
    def update_home_view(self):
        """Update home view based on session state"""
        if not self.flashcard_manager:
            return
            
        progress = self.flashcard_manager.get_session_progress()
        
        if progress['is_active'] and progress['remaining'] > 0:
            # Session in progress
            self.session_status_label.setText(
                f"📚 Session in progress: {progress['completed']}/{progress['total']} cards completed"
            )
            self.session_status_label.setVisible(True)
            self.start_button.setText("Resume Practice")
            self.new_session_button.setVisible(True)
        else:
            # No active session
            self.session_status_label.setVisible(False)
            self.start_button.setText("Start Practice")
            self.new_session_button.setVisible(False)
        
        # Update SRS info
        self.update_srs_info()
            
    def start_practice(self):
        """Start or resume practice session"""
        if self.flashcard_manager:
            # Check if there are cards due
            due_count = self.flashcard_manager.get_due_cards_count()
            
            if due_count == 0:
                QMessageBox.information(
                    self,
                    "No Cards Due",
                    "Great work! You have no cards due for review today.\n\nCome back tomorrow for more practice!  🎉"
                )
                return
            
            # Check if there's an active session
            progress = self.flashcard_manager.get_session_progress()
            
            if not progress['is_active'] or progress['remaining'] == 0:
                # Start new session
                self.flashcard_manager.start_new_session(force_new=True)
            # else: resume existing session
            
            self.flashcard_view.load_session(self.flashcard_manager)
            self.stack.setCurrentIndex(1)
        else:
            QMessageBox.warning(
                self,
                "Not Connected",
                "Please configure your Google Sheet in Settings first."
            )
    
    def start_new_session(self):
        """Force start a new session (abandon current one)"""
        if self.flashcard_manager:
            reply = QMessageBox.question(
                self,
                "Start New Session",
                "Are you sure you want to start a new session?\nYour current progress will be saved, but you'll practice a new set of words.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.flashcard_manager.end_session()
                self.flashcard_manager.start_new_session(force_new=True)
                self.flashcard_view.load_session(self.flashcard_manager)
                self.stack.setCurrentIndex(1)
            
    def show_settings(self):
        """Show settings view"""
        self.settings_view.load_settings()
        self.stack.setCurrentIndex(2)
        
    def show_home(self):
        """Return to home view"""
        self.update_home_view()  # Update status before showing
        self.stack.setCurrentIndex(0)
        
    def show_session_complete(self, stats):
        """Show session complete view with statistics"""
        # End the session
        if self.flashcard_manager:
            self.flashcard_manager.end_session()
        
        self.session_complete_view.show_stats(stats)
        self.stack.setCurrentIndex(3)