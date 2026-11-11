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
from pprint import pprint

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config.config_txqp import RANKINGS, RANK_TABLES, FINAL_REPORT_TXT
from config.config import FINAL_REPORTS_DIR, CONTEST_YEAR
from ranking_tables import get_section
from database import get_clubs_section, get_stats_sections
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether, PageBreak, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch

except ImportError:
    print("Error: reportlab is not installed. Please install it with: pip install reportlab")
    sys.exit(1)

# Ensure output directory exists
output_path = Path(FINAL_REPORTS_DIR)
output_path.mkdir(parents=True, exist_ok=True)
img_path = Path('static/images')
# Define output file path
when = datetime.now().strftime('%m-%d-%H-%M')
print(f"Texas QSO Party - Generate Final Report PDF ({CONTEST_YEAR} {when}))")
output_file = (output_path / f"final_report_{CONTEST_YEAR}_{when}.pdf")

# make these "global" since they are being used in two different functions
c = canvas.Canvas("final_report.pdf")
c.setTitle("TXQP Report")

styles = getSampleStyleSheet()

doc = SimpleDocTemplate(
    str(output_file),
    title="TXQP 2026",
    author="TX DX Society",
    pagesize=letter,
    rightMargin=15,
    leftMargin=15,
    topMargin=20,
    bottomMargin=20
)
# Custom styles
title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontName='Times-Bold',
    fontSize=24,
    textColor=colors.HexColor('#8B0000'),
    alignment=1, # Center
    spaceAfter=18
)
subtitle_style = ParagraphStyle(
    'SubtitleStyle',
    parent=styles['Heading2'],
    fontName='Times-Roman',
    fontSize=20,
    textColor=colors.HexColor("#030303"),
    alignment=1, # Center
    spaceBefore=18,
    spaceAfter=18
)
date_style = ParagraphStyle(
    'DateStyle',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=9,
    textColor=colors.HexColor("#000000"),
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
    borderColor=colors.HexColor('#000000'),
    borderPadding=6
)
section_title_style = ParagraphStyle(
    'SectionTitleStyle',
    parent=styles['Heading2'],
    fontName='Times-Bold',
    fontSize=24,
    textColor=colors.HexColor('#8B0000'),
    spaceBefore=14,
    spaceAfter=8
)
table_title_style = ParagraphStyle(
    'TableTitleStyle',
    parent=styles['Heading3'],
    fontName='Helvetica-Bold',
    fontSize=11,
    textColor=colors.HexColor("#000000"),
    spaceBefore=8,
    spaceAfter=4
)
# Define a paragraph style for your table cells (adjust font, size, leading as needed)
cell_style = ParagraphStyle(
    'TableCellStyle',
    fontName='Courier-Bold',
    fontSize=9,
    leading=11,
    textColor=colors.black,
    alignment=2  # right
)
# Headers (wrap headers in Paragraphs as well if they might be long)
header_style = ParagraphStyle(
    'TableHeaderStyle',
    fontName='Courier-Bold',
    fontSize=12,
    leading=14,
    textColor=colors.white,
    alignment=0  # 0=LEFT, 1=CENTER
)

# Base Table Style
more_table_style_cmds = [
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#6899EE")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Changed to TOP so wrapped lines align nicely
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
    ('ALIGN', (0, 0), (0, -1), 'CENTER'), # Rank column centered
    ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ('TOPPADDING', (0, 0), (-1, 0), 6),
    ('FONTNAME', (0, 1), (-1, -1), 'Courier-Bold'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('TOPPADDING', (0, 1), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
]

story = []

def generate_final_report_pdf(s, year: str):
    """
    Generate final report PDF for a year using ReportLab.
    
    Args:
        year: Contest year
    """
    print(f"Texas QSO Party - Generate Final Report PDF ({year} {when}))")
 
  
    _set_up_pdf_document(year)

    for section_config in RANK_TABLES:
        section = get_section(year, section_config)
        _add_section(section)

    # get the section for the club results
    sections = get_clubs_section(s, year)
    for section in sections:
        _add_section(section)

    sections = get_stats_sections(s)
    col_widths = [1 * inch, 5 * inch, 0.5 * inch, 0.5 * inch]
    for section in sections:
        _add_section(section, color=False, col_widths=col_widths)
    
    print(f"finish PDF document")
    _finish_pdf_document()
    
    print('break')

def _set_up_pdf_document(year):
    """Set up the PDF document natively using ReportLab"""
    # Header
    story.extend([Paragraph(f"Texas QSO Party {year}", title_style)])
    story.extend([Paragraph("Final Results", subtitle_style)])
    story.extend([Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", date_style)])

    # logo
    img = Image(f"{img_path}/txqp.png")
    aspect = img.imageHeight / float(img.imageWidth)
    img.drawWidth = 200
    img.drawHeight = 200 * aspect
    story.append(img)
    
    # Intro
    intro_text = FINAL_REPORT_TXT if FINAL_REPORT_TXT else 'Congratulations to all participants!'
    story.extend([Paragraph(intro_text, intro_style)])

def _add_section(section, color = True, col_widths=[]):
    story.extend([Paragraph(section['section_title'], section_title_style)])
    # one table at a time
    for table in section['tables']:
        print('break')
        story.extend([Paragraph(table['title'], table_title_style)])
        print('break')
        
        # Headers
        if len(table['headers']) == 3:
            col_widths = [1 * inch, 1 * inch, 1 * inch]
        num_table_rows = 0
        num_styles_added = 0
        table_rows = []
        table_style_cmds = []
        story.extend([Paragraph(h, header_style) for h in table['headers']])
        # Rows wrapped in Paragraphs so colWidths forces wrapping
        for row in table['rows']:
            formatted_row = [
                Paragraph("N/A" if val == -1 else str(val), cell_style) 
                for val in row
            ]
            table_rows.append(formatted_row)
            num_table_rows += 1
        
        # Alternating row colors and rank highlighting
        for i, row in enumerate(table_rows):
            
            # Default alternating
            if i % 2 == 0:
                bg_color = colors.HexColor('#ffffff')
            else:
                bg_color = colors.HexColor("#bff5d7")
            
            # Rank highlighting
            rank = row[0] # Rank is first column
            is_highlighted = False
            if i > 2 or color:
                if rank == 1:
                    bg_color = colors.HexColor("#B4F0B5")
                elif rank == 2:
                    bg_color = colors.HexColor("#CA9AEFFF")
                elif rank == 3:
                    bg_color = colors.HexColor("#B2C9FA")
            
            table_style_cmds.extend([('BACKGROUND', (0, i), (-1, i), bg_color)])
            # print(f"i = {i}, New cmds:\n{table_style_cmds[:23]}")
            num_styles_added += 1
            
        
        # Create Table (using auto-sizing columns) except for category stats table
        if table['title'] == 'Number of Logs by Category':
            rows_in_table = Table(table_rows, repeatRows=1, colWidths=col_widths)
        else:
            rows_in_table = Table(table_rows, repeatRows=1)
        # print(f"rows in table: {type(table_rows)} {len(table_rows)}")
        # for i, r in enumerate(table_rows):
        #     print(f"index {i}, length of row {len(r)}")

        # nrows = len(table_rows)

        # for command in table_style_cmds:
        #     if command[0] not in {
        #         "BACKGROUND",
        #         "ROWBACKGROUNDS",
        #         "COLBACKGROUNDS",
        #     }:
        #         continue

        #     start_row = 14
        #     end_row = command[2][1]

        #     for label, row in (("start", start_row), ("end", end_row)):
        #         normalized_row = row if row >= 0 else nrows + row

        #         if not 0 <= normalized_row < nrows:
        #             print(f"Table {table['title']!r} has {nrows} rows, but background command has invalid {label} row {row}: {command!r}"
        #             )
        #             print('break')

        foo = table_style_cmds + more_table_style_cmds
        rows_in_table.setStyle(TableStyle(foo))
        story.append(rows_in_table)
        story.append(Spacer(1, 10))
        print('break')

def _finish_pdf_document():
    print(f"length of story list: {len(story)}")
    for index, item in enumerate(story):
        print(f"{index} {type(item).__name__}\n")
    print('break')

    import sys
    import traceback

    try:
        doc.build(story)
    except Exception:
        traceback.print_exc(limit=100, file=sys.stdout)
        raise

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
