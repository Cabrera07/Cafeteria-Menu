###############################################################################
# Café Menu Manager
# Main window implementation for a café menu CRUD system with Qt interface
###############################################################################

# === Imports ===
# Standard library imports
from pathlib import Path
from decimal import Decimal
from typing import Optional, List
import os
import decimal
import tempfile

# Third-party imports
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton,
    QFileDialog, QMessageBox, QFrame
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap

# Local imports
import resources_rc
from ui_preview import PDFPreviewDialog
from database import DatabaseManager, MenuItem
from pdf_generator import MenuItemPdfGenerator



###############################################################################
# MainWindow Class - Core Logic and UI
###############################################################################

class MainWindow(QMainWindow):
    """Main window for the Cafe Menu CRUD application."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Café Menu Manager")
        self.setMinimumSize(1400, 1000)

        # === Database Manager and State Variables ===
        config_path = str(Path(__file__).resolve().parent.parent / 'db' / 'config.json')
        self.db = DatabaseManager(config_path)
        self.current_image: Optional[bytes] = None
        self.current_image_name: Optional[str] = None
        self.current_items: List[MenuItem] = []
        self.current_index: int = -1

        # Setup UI components and initial data loading
        self.setup_ui()
        self.setup_connections()
        self.load_categories()
        self.load_items()



    ###############################################################################
    # UI Setup
    ###############################################################################

    def setup_ui(self):
        """Define the UI layout and components."""

        # === Style Definition ===
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                color: #1a1413;
                font-size: 20px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit {
                background-color: #FFFFFF;
                border: 4px solid #1a1413;
                border-radius: 5px;
                padding: 5px;
                color: #1a1413;
                font-size: 18px;
            }
            #titleLabel {
                font-size: 40px;
                color: #1a1413;
                font-weight: bold;
            }      
                                 
            /* Button Style */
            QPushButton {
                background-color: #1a1413;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a3b39;
            }
                           
            /* Message Style */           
            QMessageBox {
                background-color: #1a1413;  
            }
            QMessageBox QLabel {
                color: #FFFFFF;  
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #4a3b39; 
                color: white;
                min-width: 75px;
                padding: 5px;
            }
            QMessageBox QPushButton:hover {
                background-color: #967259;  
            }
                           
            /* Combobox Style */
            QComboBox {
                background-color: #FFFFFF;
                border: 4px solid #1a1413;
                border-radius: 5px;
                padding: 5px;
                color: #1a1413;
                font-size: 18px;
            }
            QComboBox::placeholder {
                color: #808080;  
            }
            QComboBox::drop-down {
                border: none;
            }
           QComboBox::down-arrow {
                image: url(:/assets/icons/down-arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 4px solid #1a1413;
                color: #1a1413;
                selection-background-color: #1a1413;
                selection-color: white;
            }       
        """)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(15)  
        layout.setContentsMargins(20, 20, 20, 20) 
        


        # === Header Section ===
        header_widget = QWidget()
        header_widget.setFixedHeight(80)  
        header = QHBoxLayout(header_widget)
        header.setSpacing(10)
        header.setContentsMargins(0, 0, 0, 10)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(":/assets/images/cup-of-drink.png")
        logo_label.setPixmap(logo_pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))  
        header.addWidget(logo_label) 
        
        # Title
        title_label = QLabel("  Cafeteria Menu Manager")
        title_label.setObjectName("titleLabel")
        header.addWidget(title_label)
        header.addStretch()
        layout.addWidget(header_widget)
        


        # === Search Section ===
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 10, 0, 10) 
        search_icon = QPushButton(QIcon(":/assets/icons/magnifier.png"), "")
        search_icon.setFixedSize(60, 60)
        search_icon.setIconSize(QSize(35, 35))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search menu items...")
        self.search_input.setFixedHeight(60)  
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        


        # === Form Layout for Menu Item Details ===
        form_layout = QHBoxLayout()
        form_layout.setSpacing(35) 
        

        # == Left Side: Image Selection ==
        image_layout = QVBoxLayout()
        image_layout.setContentsMargins(25, 0, 25, 0) 
        self.image_label = QLabel()
        self.image_label.setFixedSize(400, 400)
        self.image_label.setStyleSheet("border: 6px dashed #1a1413; border-radius: 10px;")
        self.image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.image_label)
        
        self.select_image_btn = QPushButton("   Select Image")
        self.select_image_btn.setIcon(QIcon(":/assets/icons/upload.png"))
        self.select_image_btn.setIconSize(QSize(35, 35))
        image_layout.addWidget(self.select_image_btn)
        form_layout.addLayout(image_layout)
        


        # == Right Side: Form Fields for Item Details ==
        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(50)  
        
        # ID Field (read-only)
        id_layout = QHBoxLayout()
        id_label = QLabel("ID:")
        id_label.setFixedWidth(115)  
        self.id_input = QLineEdit()
        self.id_input.setFixedHeight(50)  
        self.id_input.setReadOnly(True)
        self.id_input.setPlaceholderText("Auto-generated ID")
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_input)
        fields_layout.addLayout(id_layout)

        # Name Field
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setFixedWidth(115)
        self.name_input = QLineEdit()
        self.name_input.setFixedHeight(50)
        self.name_input.setPlaceholderText("Enter menu item name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        fields_layout.addLayout(name_layout)

        # Category Field
        category_layout = QHBoxLayout()
        category_label = QLabel("Category:")
        category_label.setFixedWidth(115)
        self.category_combo = QComboBox()
        self.category_combo.setFixedHeight(50)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        fields_layout.addLayout(category_layout)

        # Price Field
        price_layout = QHBoxLayout()
        price_label = QLabel("Price:")
        price_label.setFixedWidth(115)
        self.price_input = QLineEdit()
        self.price_input.setFixedHeight(50)
        self.price_input.setPlaceholderText("Enter price (e.g., 9.99)")
        price_layout.addWidget(price_label)
        price_layout.addWidget(self.price_input)
        fields_layout.addLayout(price_layout)

        # Description Field
        description_layout = QHBoxLayout()
        description_label = QLabel("Description:")
        description_label.setFixedWidth(115)
        self.description_input = QTextEdit()
        self.description_input.setFixedHeight(100)
        self.description_input.setPlaceholderText("Enter item description")  
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_input)
        fields_layout.addLayout(description_layout)

        form_layout.addLayout(fields_layout)
        layout.addLayout(form_layout)
        


        # == Buttons Layout ==
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Previous 
        self.prev_btn = QPushButton(QIcon(":/assets/icons/arrow.png"), " Previous")
        self.prev_btn.setIconSize(QSize(35, 35))
        
        # Next 
        self.next_btn = QPushButton("Next ")
        self.next_btn.setIcon(QIcon(":/assets/icons/right-arrow.png"))
        self.next_btn.setIconSize(QSize(35, 35))
        self.next_btn.setLayoutDirection(Qt.RightToLeft)

        # New 
        self.new_btn = QPushButton(" Insert")
        self.new_btn.setIcon(QIcon(":/assets/icons/add.png"))
        self.new_btn.setIconSize(QSize(35, 35))

        # Save
        self.save_btn = QPushButton(QIcon(":/assets/icons/text-box.png"), "  Save Edit")
        self.save_btn.setIconSize(QSize(35, 35))

        # Delete 
        self.delete_btn = QPushButton(" Delete")
        self.delete_btn.setIcon(QIcon(":/assets/icons/bin.png"))
        self.delete_btn.setIconSize(QSize(35, 35))
        
        # Rfresh
        self.refresh_btn = QPushButton(" Refresh")
        self.refresh_btn.setIcon(QIcon(":/assets/icons/refresh-page-option.png"))
        self.refresh_btn.setIconSize(QSize(35, 35))
        
        # Print 
        self.print_btn = QPushButton(QIcon(":/assets/icons/paper.png"), " Print")
        self.print_btn.setIconSize(QSize(35, 35))
        
        # Clear 
        self.clear_btn = QPushButton(" Clear")
        self.clear_btn.setIcon(QIcon(":/assets/icons/clean.png"))
        self.clear_btn.setIconSize(QSize(35, 35))

        # Add buttons to layout
        buttons = [
            self.prev_btn,
            self.next_btn,
            self.new_btn,
            self.save_btn,
            self.delete_btn,
            self.print_btn,
            self.clear_btn,
            self.refresh_btn 
        ]
        
        for button in buttons:
            buttons_layout.addWidget(button)
        
        layout.addLayout(buttons_layout)



    ###############################################################################
    # Setup and Initialization
    ###############################################################################

    def setup_connections(self):
        """Set up event handlers for UI elements"""
        # Button connections
        self.prev_btn.clicked.connect(self.show_previous_item)
        self.next_btn.clicked.connect(self.show_next_item)
        self.new_btn.clicked.connect(self.insert_item)  
        self.save_btn.clicked.connect(self.update_item) 
        self.delete_btn.clicked.connect(self.delete_item)
        self.print_btn.clicked.connect(self.print_item)
        self.clear_btn.clicked.connect(self.clear_fields)
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        # Search connection
        self.search_input.textChanged.connect(self.search_items)
        
        # Image selection
        self.select_image_btn.clicked.connect(self.select_image)



    ###############################################################################
    # Load and Display Functions
    ###############################################################################

    def load_categories(self):
        """Load categories into combo box"""
        try:
            categories = self.db.get_categories()
            self.category_combo.clear()
            self.category_combo.addItem("Select a category", None)  
            for category_id, category_name in categories:
                self.category_combo.addItem(category_name, category_id)
            self.category_combo.setCurrentIndex(0)
        except Exception as e:
            self.show_error("Error loading categories", str(e))

    def load_items(self):
        """Load all menu items"""
        try:
            self.current_items = self.db.get_all_menu_items()
            if self.current_items:
                self.current_index = 0
                self.display_current_item()
            else:
                self.clear_fields()
            self.update_navigation_buttons()
        except Exception as e:
            self.show_error("Error loading items", str(e))

    def display_current_item(self):
        """Display the current item in the form"""
        if 0 <= self.current_index < len(self.current_items):
            item = self.current_items[self.current_index]
            
            # Set form fields
            self.id_input.setText(str(item.id))
            self.name_input.setText(item.name)
            self.description_input.setText(item.description)
            self.price_input.setText(str(item.price))
            
            # Set category
            index = self.category_combo.findText(item.category_name)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
            
            # Display image
            if item.image:
                self.current_image = item.image
                self.current_image_name = item.image_name
                self.display_image(item.image)
            else:
                self.clear_image()
                
            # Enable/disable appropriate buttons
            self.new_btn.setEnabled(False)
            self.save_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)

    def display_image(self, image_data: bytes):
        """Display image data in the image label"""
        try:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        except Exception as e:
            self.show_error("Error displaying image", str(e))
    
    def refresh_data(self):
        """Refresh data from the database and update the UI."""
        try:
            # Force close the connection to clear internal state
            if self.db.connection:
                self.db.connection.close()
            self.db.connect()  

            self.load_categories()
            self.current_items = self.db.get_all_menu_items()

            if self.current_items:
                self.current_index = 0
                self.display_current_item()
            else:
                self.current_index = -1
                self.clear_fields()

            self.update_navigation_buttons()
            QMessageBox.information(self, "Success", "Data refreshed successfully")

        except Exception as e:
            self.show_error("Error refreshing data", str(e))



    ###############################################################################
    # Image and Field Management
    ###############################################################################

    def clear_image(self):
        """Clear the image display"""
        self.image_label.clear()
        self.image_label.setText("No Image")
        self.current_image = None
        self.current_image_name = None

    def select_image(self):
        """Handle image selection"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_name:
            try:
                with open(file_name, 'rb') as file:
                    self.current_image = file.read()
                    self.current_image_name = os.path.basename(file_name)
                    self.display_image(self.current_image)
            except Exception as e:
                self.show_error("Error loading image", str(e))



    ###############################################################################
    # Validation and Data Handling
    ###############################################################################

    def validate_form(self) -> bool:
        """Validate form inputs"""
        if not self.name_input.text().strip():
            self.show_error("Validation Error", "Name is required")
            self.name_input.setFocus()
            return False
            
        if not self.description_input.toPlainText().strip():
            self.show_error("Validation Error", "Description is required")
            self.description_input.setFocus()
            return False
            
        try:
            price = Decimal(self.price_input.text())
            if price <= 0:
                raise ValueError()
        except (ValueError, decimal.InvalidOperation):
            self.show_error("Validation Error", "Price must be a positive number")
            self.price_input.setFocus()
            return False
            
        if self.category_combo.currentIndex() <= 0:  
            self.show_error("Validation Error", "Category must be selected")
            self.category_combo.setFocus()
            return False
            
        if not self.current_image:
            self.show_error("Validation Error", "An image is required")
            return False
            
        return True

    def get_form_data(self) -> MenuItem:
        """Get form data as MenuItem object"""
        return MenuItem(
            id=int(self.id_input.text()) if self.id_input.text() else None,
            name=self.name_input.text().strip(),
            description=self.description_input.toPlainText().strip(),
            price=float(self.price_input.text()),
            category_id=self.category_combo.currentData(),
            image=self.current_image,
            image_name=self.current_image_name,
            category_name=self.category_combo.currentText()
        )



    ###############################################################################
    # CRUD Operations
    ###############################################################################
    
    def delete_item(self):
        """Delete current menu item"""
        if not self.id_input.text():
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this item?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_menu_item(int(self.id_input.text()))
                QMessageBox.information(self, "Success", "Item deleted successfully")
                self.load_items()
            except Exception as e:
                self.show_error("Error deleting item", str(e))

    def search_items(self):
        """Handle search functionality"""
        search_text = self.search_input.text().strip()
        try:
            if search_text:
                self.current_items = self.db.search_menu_items(search_text)
                if not self.current_items:
                    QMessageBox.information(self, "Search Result", 
                        "No exact matches found. Showing similar items if available.")
            else:
                self.current_items = self.db.get_all_menu_items()
            
            self.current_index = 0 if self.current_items else -1
            if self.current_items:
                self.display_current_item()
            else:
                self.clear_fields()
            self.update_navigation_buttons()
        except Exception as e:
            self.show_error("Error searching items", str(e))

    def insert_item(self):
        """Handle insertion of a new menu item"""
        if not self.validate_form():
            return
            
        try:
            item = self.get_form_data()
            if item.id:  
                self.show_error("Error", "Cannot insert: This is an existing item. Use update instead.")
                return
                
            new_id = self.db.create_menu_item(item)
            QMessageBox.information(self, "Success", "Item created successfully")
            self.id_input.setText(str(new_id))
            self.load_items()
        except ValueError as ve:
            self.show_error("Validation Error", str(ve))
        except Exception as e:
            self.show_error("Error creating item", str(e))

    def update_item(self):
        """Handle updating an existing menu item"""
        if not self.validate_form():
            return
            
        if not self.id_input.text():
            self.show_error("Error", "Cannot update: No item selected. Use insert for new items.")
            return
            
        try:
            item = self.get_form_data()
            if self.db.update_menu_item(item):
                QMessageBox.information(self, "Success", "Item updated successfully")
                self.load_items()
            else:
                QMessageBox.information(self, "No Changes", "No changes detected in the item")
        except Exception as e:
            self.show_error("Error updating item", str(e))

    

    ###############################################################################
    # Utility Methods
    ###############################################################################

    def show_previous_item(self):
        """Display previous item"""
        if self.current_index > 0:
            self.current_index -= 1
            self.display_current_item()
            self.update_navigation_buttons()

    def show_next_item(self):
        """Display next item"""
        if self.current_index < len(self.current_items) - 1:
            self.current_index += 1
            self.display_current_item()
            self.update_navigation_buttons()

    def update_navigation_buttons(self):
        """Update navigation button states"""
        self.prev_btn.setEnabled(self.current_index > 0)
        self.next_btn.setEnabled(self.current_index < len(self.current_items) - 1)
        self.delete_btn.setEnabled(bool(self.id_input.text()))

    def clear_fields(self):
        """Clear all form fields including search"""
        self.id_input.clear()
        self.name_input.clear()
        self.description_input.clear()
        self.price_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.search_input.clear()  
        self.clear_image()
        self.current_image = None
        self.current_image_name = None
        
        # Reset placeholders
        self.id_input.setPlaceholderText("Auto-generated ID")
        self.name_input.setPlaceholderText("Enter item name")
        self.description_input.setPlaceholderText("Enter item description")
        self.price_input.setPlaceholderText("Enter price (e.g., 9.99)")
        self.category_combo.setCurrentIndex(0)
        self.new_btn.setEnabled(True)
        self.save_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

    def show_error(self, title: str, message: str):
        """Display error message"""
        QMessageBox.critical(self, title, message)

    def print_item(self):
        """Print current item to PDF with preview"""
        if not self.id_input.text():
            self.show_error("Error", "No item selected to print")
            return
            
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                pdf_path = tmp_file.name
            
            # Generate PDF report
            current_item = self.get_form_data()
            report_generator = MenuItemPdfGenerator()
            report_generator.generate_report(current_item, pdf_path)
            
            # Show PDF preview dialog
            preview_dialog = PDFPreviewDialog(pdf_path, self)
            preview_dialog.exec_()
            
            # Clean up temporary file
            try:
                os.unlink(pdf_path)
            except:
                pass  
                
        except Exception as e:
            self.show_error("Error generating PDF", str(e))    

    def closeEvent(self, event):
        """Handle application closure"""
        self.db.close()
        super().closeEvent(event)