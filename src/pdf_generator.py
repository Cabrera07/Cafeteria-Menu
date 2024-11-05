###############################################################################
# PDF Report Generator
# Generates a PDF report for a menu item using ReportLab
###############################################################################

# === Imports ===
# Standard library imports
import os
import io
from datetime import datetime
from pathlib import Path

# Third-party imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, Frame
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Local imports
from database import MenuItem



###############################################################################
# MenuItemPdfGenerator Class - Generates PDF reports for menu items
###############################################################################

class MenuItemPdfGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        

    
    ###############################################################################
    # Setup Custom Styles
    ###############################################################################

    def _setup_custom_styles(self):
        """Setup custom styles for the PDF report"""

        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=1  
        ))
        
        # Header style for report title
        self.styles.add(ParagraphStyle(
            name='Header',
            parent=self.styles['Heading1'],
            fontSize=25,
            textColor=colors.HexColor('#1a1413'),
            alignment=1,
            spaceAfter=20
        ))
        
        # Heading style for section headers
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#1a1413')
        ))
        
        # Normal text style for paragraphs
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=12,
            leading=16
        ))


    ###############################################################################
    # Header Table with Logo
    ###############################################################################

    def create_header_table(self, logo_path):
        """Create a header table with logo and title and full-width underline"""

        # Load logo image if it exists, otherwise show placeholder text
        if os.path.exists(logo_path):
            logo = Image(logo_path)
            logo.drawHeight = 1 * inch
            logo.drawWidth = 1 * inch
        else:
            # Placeholder if logo not found
            logo = Paragraph("Logo not found", self.styles['CustomNormal'])

        header_title = Paragraph("Cafeteria Menu", self.styles['Header'])
        

        # Main header table with logo and title
        header_data = [[logo, header_title]]
        header_table = Table(header_data, colWidths=[1.5*inch, 5*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ffffff')),
        ]))
        

        # Decorative line below the header
        line_table = Table([['']], colWidths=[7*inch])  
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0,0), (-1,0), 4, colors.HexColor('#1a1413')),
            ('TOPPADDING', (0,0), (-1,0), 0),
            ('BOTTOMPADDING', (0,0), (-1,0), 0),
        ]))
        

        # Combine header and line in a container table
        container_data = [[header_table], [line_table]]
        container_table = Table(container_data)
        container_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        
        return container_table



    ###############################################################################
    # Generate PDF Report
    ###############################################################################

    def generate_report(self, menu_item: MenuItem, output_path: str):
        """Generate a PDF report for a specific menu item."""

        # Define the PDF document settings
        doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=60,  
        leftMargin=60,   
        topMargin=60,    
        bottomMargin=60  
        )

        # List to hold the elements of the PDF document
        elements = []


        # Add header with logo and title
        logo_path = str(Path(__file__).parent.parent / 'assets' / 'images' / 'cup-of-drink.png')
        header_table = self.create_header_table(logo_path)
        elements.append(header_table)
        elements.append(Spacer(1, 30))


        # Add title for menu item details
        title = Paragraph(f"Menu Item Details - {menu_item.name}", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 10))


        # Add item image if it exists
        if menu_item.image:
            img_stream = io.BytesIO(menu_item.image)
            img = Image(img_stream)
            img.drawHeight = 2.1 * inch
            img.drawWidth = 2.1 * inch
            
            # Table to frame the image
            image_table = Table([[img]], colWidths=[2.2*inch])
            image_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, -1), 4, colors.HexColor('#1a1413')),  
                ('PADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(image_table)
            elements.append(Spacer(1, 20))


        # Table for item details (ID, Name, Category, Price)
        data = [
            ['Field', 'Value'],
            ['ID', str(menu_item.id)],
            ['Name', menu_item.name],
            ['Category', menu_item.category_name],
            ['Price', f"${menu_item.price:.2f}"],
        ]
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1413')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1a1413')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#1a1413')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 12)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # Description Section
        elements.append(Paragraph("Description", self.styles['CustomHeading']))
        elements.append(Paragraph(menu_item.description, self.styles['CustomNormal']))



        ###############################################################################
        # Footer with Page Number
        ###############################################################################

        def add_page_number(canvas, doc):
            """Add page number and line to footer on each page."""
            canvas.saveState()
            # Draw a line above the footer
            canvas.setStrokeColor(colors.HexColor('#1a1413'))
            canvas.setLineWidth(4)
            canvas.line(
                doc.leftMargin, 
                doc.bottomMargin + 30, 
                doc.pagesize[0] - doc.rightMargin, 
                doc.bottomMargin + 30
            )
            
            # Page number centered at the bottom
            canvas.setFont('Helvetica', 16)
            page_number_text = f"Page {doc.page}"
            canvas.drawString(
                doc.pagesize[0]/2 - 20,
                doc.bottomMargin + 10,
                page_number_text
            )
            
        # Build the PDF with footer function
        doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)