#!/usr/bin/env python3
"""
Texas QSO Party - Generate Final Report PDF

Generates PDF final report with tables for a contest year natively using ReportLab.
Saves to data/results/final_report_{year}.pdf

Create the PDF document natively using ReportLab
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config.config_txqp import RANKINGS, RANK_TABLES, FINAL_REPORT_TXT
from config.config import FINAL_REPORTS_DIR, CONTEST_YEAR
from ranking_tables import get_section

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
except ImportError:
    print("Error: reportlab is not installed. Please install it with: pip install reportlab")
    sys.exit(1)

# Ensure output directory exists
output_path = Path(FINAL_REPORTS_DIR)
output_path.mkdir(parents=True, exist_ok=True)
# Define output file path
output_file = (output_path / f"final_report_{CONTEST_YEAR}.pdf")

# make these "global" since they are being used in two different functions
doc = SimpleDocTemplate(
    str(output_file),
    pagesize=letter,
    rightMargin=15,
    leftMargin=15,
    topMargin=20,
    bottomMargin=20
)
styles = getSampleStyleSheet()
# Custom styles
title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontName='Times-Bold',
    fontSize=20,
    textColor=colors.HexColor('#8B0000'),
    alignment=1, # Center
    spaceAfter=6
)
subtitle_style = ParagraphStyle(
    'SubtitleStyle',
    parent=styles['Heading2'],
    fontName='Times-Roman',
    fontSize=14,
    textColor=colors.HexColor('#333333'),
    alignment=1, # Center
    spaceAfter=4
)
date_style = ParagraphStyle(
    'DateStyle',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=9,
    textColor=colors.HexColor('#666666'),
    alignment=1, # Center
    spaceAfter=14
)
intro_style = ParagraphStyle(
    'IntroStyle',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=11,
    spaceAfter=16,
    leftIndent=10,
    rightIndent=10,
    borderWidth=0,
    borderColor=colors.HexColor('#8B0000'),
    borderPadding=6
)
section_title_style = ParagraphStyle(
    'SectionTitleStyle',
    parent=styles['Heading2'],
    fontName='Times-Bold',
    fontSize=18,
    textColor=colors.HexColor('#8B0000'),
    spaceBefore=14,
    spaceAfter=8
)
table_title_style = ParagraphStyle(
    'TableTitleStyle',
    parent=styles['Heading3'],
    fontName='Helvetica-Bold',
    fontSize=11,
    textColor=colors.HexColor('#333333'),
    spaceBefore=8,
    spaceAfter=4
)

story = []

def generate_final_report_pdf(year: str):
    """
    Generate final report PDF for a year using ReportLab.
    
    Args:
        year: Contest year
    """
    print("=" * 60)
    print(f"Texas QSO Party - Generate Final Report PDF ({year})")
    print("=" * 60)
    
    print("Set up PDF...")
    _set_up_pdf_document(year)

    for section_config in RANK_TABLES:
        section = get_section(year, section_config)
        # print(f"doing section with title: {section_config['section_title']}")
        _add_section(section, year)

    print(f"finish PDF document")
    _finish_pdf_document()

    # Summary
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Saved to: {output_file}")
    print()

def _set_up_pdf_document(year):
    """Set up the PDF document natively using ReportLab"""
    # Header
    story.append(Paragraph(f"Texas QSO Party {year}", title_style))
    story.append(Paragraph("Final Results", subtitle_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", date_style))
    
    # Intro
    intro_text = FINAL_REPORT_TXT if FINAL_REPORT_TXT else 'Congratulations to all participants!'
    story.append(Paragraph(intro_text, intro_style))

def _add_section(section, year):
    story.append(PageBreak())
    story.append(Paragraph(section['section_title'], section_title_style))
    
    for table in section['tables']:
        table_elements = []
        table_elements.append(Paragraph(table['title'], table_title_style))
        
        # Prepare table data
        table_data = []
        
        # Headers
        table_data.append(table['headers'])
        
        # Rows
        for row in table['rows']:
            formatted_row = ["N/A" if val == -1 else str(val) for val in row]
            table_data.append(formatted_row)
        
        # Create Table (using auto-sizing columns)
        t = Table(table_data, repeatRows=1)
        
        # Base Table Style
        style_cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'), # Rank column centered
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('FONTNAME', (0, 1), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
        ]
        
        # Alternating row colors and rank highlighting
        for i, row in enumerate(table['rows']):
            row_idx = i + 1 # offset by 1 for header
            
            # Default alternating
            if i % 2 == 0:
                bg_color = colors.HexColor('#ffffff')
            else:
                bg_color = colors.HexColor('#f0f0f0')
            
            # Rank highlighting
            rank = row[0] # Rank is first column
            is_highlighted = False
            if rank == 1:
                bg_color = colors.HexColor('#FFD700')
                is_highlighted = True
            elif rank == 2:
                bg_color = colors.HexColor('#C0C0C0')
                is_highlighted = True
            elif rank == 3:
                bg_color = colors.HexColor('#CD7F32')
                is_highlighted = True
            
            style_cmds.append(('BACKGROUND', (0, row_idx), (-1, row_idx), bg_color))
            if is_highlighted:
                style_cmds.append(('FONTNAME', (0, row_idx), (-1, row_idx), 'Courier-Bold'))
        
        t.setStyle(TableStyle(style_cmds))
        table_elements.append(t)
        table_elements.append(Spacer(1, 10))
        
        story.append(KeepTogether(table_elements))
        
    story.append(PageBreak())

def _finish_pdf_document():
    doc.build(story)

def main(year):
    generate_final_report_pdf(year)

if __name__ == "__main__":
    from config.config import CONTEST_YEAR
    
    # Get year from environment or command line
    if len(sys.argv) > 1:
        year = sys.argv[1]
    else:
        year = CONTEST_YEAR
    main(year)
