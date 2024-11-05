###################################################################################
# Main Application Entry Point
# Initializes the QApplication and launches the main window for the Cafeteria Menu
###################################################################################

# === Imports ===
import sys
from PySide6.QtWidgets import QApplication
from ui_main import MainWindow  # Import the main window UI

# === Application Initialization ===
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())