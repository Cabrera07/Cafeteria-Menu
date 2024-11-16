###############################################################################
# PDF Preview Dialog
# Displays a preview of a PDF file, allows zooming and printing
###############################################################################

# === Imports ===
# Standard library imports
import os
import tempfile
import shutil

# Third-party imports
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton,
    QFileDialog, QMessageBox, QFrame, QScrollArea, QDialog
)
from PySide6.QtGui import QPageSize
from PySide6.QtCore import Qt, QSize, QRect 
from PySide6.QtGui import QIcon, QPixmap, QImage, QPalette, QColor
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QPainter
import fitz  # PyMuPDF library




###############################################################################
# PDFPreviewDialog Class - Handles PDF preview, zoom, and print
###############################################################################

class PDFPreviewDialog(QDialog):
    def __init__(self, pdf_path, parent=None):
        super().__init__(parent)
        self.pdf_path = pdf_path
        self.current_page = 0
        self.zoom_level = 0.7
        self.labels = []  # To store QLabel references for PDF pages
        
        # Set window properties
        self.setWindowTitle("PDF Preview")
        self.setMinimumSize(900, 1000)
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
            }
            QLabel {
                color: #1a1413;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #1a1413;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 20px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4a3b39;
            }
            QScrollArea {
                border: 8px solid #1a1413;
                border-radius: 5px;
                background-color: white;
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
                background-color: #4a3b39;  
            }
        """)
        
        # Setup UI components and initial PDF load
        self.setup_ui()
        self.load_pdf()



    ###############################################################################
    # UI Setup
    ###############################################################################
    
    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # === Header Section ===
        header_layout = QHBoxLayout()

        # Icon Label
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(":/assets/icons/pdf.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Title Label
        header = QLabel(" Printing Preview")
        header.setStyleSheet("font-size: 24px; margin-bottom: 10px;")
        header.setAlignment(Qt.AlignLeft)

        # Zoom Label
        self.zoom_label = QLabel(f"Zoom: {int(self.zoom_level * 100)}%")
        self.zoom_label.setStyleSheet("font-size: 16px;")

        # Add widgets to header layout
        header_layout.addWidget(icon_label)  
        header_layout.addWidget(header)
        header_layout.addStretch()  
        header_layout.addWidget(self.zoom_label)
        layout.addLayout(header_layout)
        
        
        # Scroll area for PDF content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumSize(800, 600)
        
        # Container for PDF pages
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)
        

        # === Controls section ===
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # Zoom controls
        zoom_out_btn = QPushButton(" Zoom Out")
        zoom_out_btn.setIcon(QIcon(":/assets/icons/zoom-out.png"))
        zoom_out_btn.setIconSize(QSize(35, 35))
        zoom_out_btn.clicked.connect(self.zoom_out)

        zoom_in_btn = QPushButton(" Zoom In")
        zoom_in_btn.setIcon(QIcon(":/assets/icons/zoom-in.png"))
        zoom_in_btn.setIconSize(QSize(35, 35))
        zoom_in_btn.clicked.connect(self.zoom_in)

        # Save button
        save_btn = QPushButton(" Save")
        save_btn.setIcon(QIcon(":/assets/icons/diskette.png"))
        save_btn.setIconSize(QSize(35, 35))
        save_btn.clicked.connect(self.save_pdf)
        
        # Print button
        print_btn = QPushButton(" Print")
        print_btn.setIcon(QIcon(":/assets/icons/paper.png"))
        print_btn.setIconSize(QSize(35, 35))
        print_btn.clicked.connect(self.print_pdf)
        
        # Close button
        close_btn = QPushButton(" Close")
        close_btn.setIcon(QIcon(":/assets/icons/close.png"))
        close_btn.setIconSize(QSize(35, 35))
        close_btn.clicked.connect(self.close)
        
        # Add buttons to controls layout
        controls_layout.addWidget(zoom_out_btn)
        controls_layout.addWidget(zoom_in_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(save_btn)
        controls_layout.addWidget(print_btn)
        controls_layout.addWidget(close_btn)
        
        layout.addLayout(controls_layout)
    


    ###############################################################################
    # PDF Loading and Display
    ###############################################################################

    def load_pdf(self):
        """Load and display the PDF pages with the current zoom level."""
        try:
            # Validate PDF before loading
            if not os.path.exists(self.pdf_path):
                raise Exception("PDF file not found")

            # Open PDF document
            doc = fitz.open(self.pdf_path)
            
            try:
                # Clear previous content
                for i in reversed(range(self.content_layout.count())):
                    self.content_layout.itemAt(i).widget().setParent(None)
                self.labels.clear()
                
                # Calculate zoom matrix
                zoom_matrix = fitz.Matrix(2.0 * self.zoom_level, 2.0 * self.zoom_level)
                
                # Load each page
                for page_num in range(len(doc)):
                    try:
                        page = doc.load_page(page_num)
                        pix = page.get_pixmap(matrix=zoom_matrix)
                        
                        # Convert to QImage
                        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
                        if img.isNull():
                            raise Exception(f"Failed to create image for page {page_num + 1}")
                            
                        pixmap = QPixmap.fromImage(img)
                        
                        # Create label and add to layout
                        label = QLabel()
                        label.setPixmap(pixmap)
                        label.setAlignment(Qt.AlignCenter)
                        self.content_layout.addWidget(label)
                        self.labels.append(label)
                        
                    except Exception as e:
                        raise Exception(f"Error processing page {page_num + 1}: {str(e)}")
                
                # Update zoom level indicator
                self.zoom_label.setText(f"Zoom: {int(self.zoom_level * 100)}%")
                
            finally:
                doc.close()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                            f"Error loading PDF: {str(e)}\n"
                            "Please ensure the file is a valid PDF and try again.")



    ###############################################################################
    # Save Functionality
    ###############################################################################
    
    def save_pdf(self):
        """Save the PDF file in system."""
        try:
            # Default filename set to 'CafeteriaItem.pdf'
            default_filename = "CafeteriaItem.pdf"

            # Open save file dialog with default filename
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save PDF File",
                default_filename,  # Default name for saving
                "PDF Files (*.pdf);;All Files (*)"
            )

            if file_path:
                # Ensure the file has a .pdf extension
                if not file_path.lower().endswith('.pdf'):
                    file_path += '.pdf'
                
                # Copy the file to the specified location
                shutil.copy2(self.pdf_path, file_path)
                
                # Inform the user of successful save
                QMessageBox.information(
                    self,
                    "Success",
                    f"PDF file saved successfully to:\n{file_path}"
                )
                
        except Exception as e:
            # Display error message if saving fails
            QMessageBox.critical(
                self,
                "Save Error",
                f"Error saving PDF file: {str(e)}"
            )



    ###############################################################################
    # Zoom Controls
    ###############################################################################
    
    def zoom_in(self):
        """Increase zoom level and reload PDF."""
        if self.zoom_level < 3.0:  
            self.zoom_level += 0.1
            self.load_pdf()
    
    def zoom_out(self):
        """Decrease zoom level and reload PDF."""
        if self.zoom_level > 0.3:  
            self.zoom_level -= 0.1
            self.load_pdf()
    


    ###############################################################################
    # Print Functionality
    ###############################################################################

    def print_pdf(self):
        """Print the PDF document at full page size by rendering each page directly onto the printable area."""
        try:
            # Validate PDF existence
            if not os.path.exists(self.pdf_path):
                QMessageBox.critical(self, "Error", "PDF file not found")
                return

            # Validate PDF can be opened
            try:
                doc = fitz.open(self.pdf_path)
                doc.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Invalid PDF file: {str(e)}")
                return

            # Set up the printer with high resolution and full page usage
            printer = QPrinter(QPrinter.HighResolution)
            if not printer.isValid():
                QMessageBox.critical(self, "Error", "No valid printer found")
                return

            printer.setPageSize(QPageSize(QPageSize.Letter))
            printer.setFullPage(True)  

            # Zero margins for full-area usage
            margins = printer.pageLayout().margins()
            margins.setLeft(0)
            margins.setRight(0)
            margins.setTop(0)
            margins.setBottom(0)
            printer.setPageMargins(margins)

            # Show print dialog
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                doc = None
                painter = QPainter()
                
                try:
                    doc = fitz.open(self.pdf_path)  
                    
                    # Verify printer device can be opened
                    if not painter.begin(printer):
                        raise Exception("Could not open printer device. Please check printer connection and status.")

                    for page_num in range(len(doc)):
                        # Check printer status before each page
                        if printer.printerState() == QPrinter.Error:
                            raise Exception("Printer is not ready or has encountered an error")

                        if page_num > 0:
                            if not printer.newPage():
                                raise Exception("Failed to create new page for printing")

                        page = doc[page_num]
                        
                        try:
                            # Calculate scaling matrix to fit PDF page into printer's full page area
                            printer_rect = printer.pageRect(QPrinter.DevicePixel)
                            matrix = fitz.Matrix(
                                printer_rect.width() / page.rect.width,
                                printer_rect.height() / page.rect.height
                            )
                            pix = page.get_pixmap(matrix=matrix)

                            # Convert pixmap to QImage and draw it
                            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
                            target_rect = QRect(0, 0, printer_rect.width(), printer_rect.height())
                            
                            if not painter.drawImage(target_rect, img):
                                raise Exception(f"Failed to print page {page_num + 1}")

                        except Exception as e:
                            raise Exception(f"Error rendering page {page_num + 1}: {str(e)}")

                except Exception as e:
                    QMessageBox.critical(self, "Print Error", 
                                    f"Error during printing: {str(e)}\n"
                                    "Please check your printer connection and try again.")
                finally:
                    if painter.isActive():
                        painter.end()
                    if doc:
                        doc.close()

        except Exception as e:
            QMessageBox.critical(self, "Print Error", 
                            f"An unexpected error occurred: {str(e)}\n"
                            "Please try again or contact support if the problem persists.")





