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
    leading=26,
    textColor=colors.HexColor('#8B0000'),
    spaceBefore=14,
    spaceAfter=8
)
table_title_style = ParagraphStyle(
    'TableTitleStyle',
    parent=styles['Heading3'],
    fontName='Helvetica-Bold',
    fontSize=16,
    textColor=colors.white,
)
# Headers (wrap headers in Paragraphs as well if they might be long)
table_header_style = ParagraphStyle(
    'TableHeaderStyle',
    fontName='Courier-Bold',
    fontSize=14,
    textColor=colors.white,
)
# Define a paragraph style for your table cells (adjust font, size, leading as needed)
table_cell_style = ParagraphStyle(
    'TableCellStyle',
    fontName='Courier-Bold',
    fontSize=12,
    leading=13,
    textColor=colors.black,
    alignment=2  # right
)

# Base Table Style
more_table_style_cmds = [
    # Grid, padding
    ('GRID', (0, 0), (-1, -1), 1, colors.black),

    # Table Title: Span row 0 across all columns
    ('SPAN', (0, 0), (-1, 0)),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('VALIGN', (0, 0), (-1, 0), 'TOP'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#024A35")),
    ('LEADING', (0, 0), (-1, 0), 18),
    ('TOPPADDING', (0, 0), (-1, 0), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),

    # Table Header styling
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Changed to TOP so wrapped lines align nicely
    ('BACKGROUND', (0, 1), (-1, 1), colors.navy),
    ('TOPPADDING', (0, 1), (-1, 1), 6),
    ('BOTTOMPADDING', (0, 1), (-1, 1), 6),

    # Table Cells of datas (rows 2 through end)
    # Added as the table cells are created
    ('ALIGN', (0, 1), (0, -1), 'CENTER'),
    ('VALIGN', (0, 1), (0, -1), 'TOP'),  # Changed to TOP so wrapped lines align nicely
    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ('VALIGN', (1, 1), (-1, -1), 'TOP'),  # Changed to TOP so wrapped lines align nicely
    ('BACKGROUND', (0, 2), (-1, -1), colors.white),
    ('TOPPADDING', (0, 2), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 2), (-1, -1), 4),
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
        _add_section(section, True, False)

    # get the section for the club results
    sections = get_clubs_section(s, year)
    for section in sections:
        _add_section(section, True)

    sections = get_stats_sections(s, year)
    for section in sections:
        _add_section(section, False)
    
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

def _add_section(section, color, col_widths=True):
    story.extend([Paragraph(section['section_title'], section_title_style)])
    # one table at a time
    for table in section['tables']:
        if len(table['rows']) ==0: continue
        if col_widths:
            col_widths = table['col_widths']
        table_style_cmds = []
        add_columns = [''] * (len(table['headers']) - 1)
        temp = [Paragraph(table['title'], table_title_style)]
        table_rows = [temp + add_columns]
        # Headers

        table_rows.append([Paragraph(h, table_header_style) for h in table['headers']])
        # Rows wrapped in Paragraphs so colWidths forces wrapping
        # the first row is table title, second row is table headers
        # data starts in the third row i.e. [2]
        for row in table['rows']:
            formatted_row = [
                Paragraph("N/A" if val == -1 else str(val), table_cell_style) 
                for val in row
            ]
            table_rows.append(formatted_row)
        
        # Alternating row colors and rank highlighting
        for i, row in enumerate(table_rows):
            if i in [0,1]: continue
            # Default alternating
            if i % 2 == 0:
                bg_color = colors.HexColor('#ffffff')
            else:
                bg_color = colors.HexColor("#bff5d7")
            
            # Rank highlighting
            if color:
                if i == 3:
                    bg_color = colors.HexColor("#B4F0B5")
                elif i == 4:
                    bg_color = colors.HexColor("#CA9AEFFF")
                elif i == 5:
                    bg_color = colors.HexColor("#B2C9FA")
            if i > (len(table_rows) - 1):
                print('break')
            table_style_cmds.extend([('BACKGROUND', (0, i), (-1, i), bg_color)])
            # print(f"i = {i}, New cmds:\n{table_style_cmds[:23]}")
            
        
        # Create Table (using auto-sizing columns) except for category stats table
        if col_widths:
            rows_in_table = Table(table_rows, repeatRows=1, colWidths=col_widths)
        else:
            rows_in_table = Table(table_rows, repeatRows=1)

        # print(f"rows in table: {type(table_rows)} {len(table_rows)}")
        # for i, r in enumerate(table_rows):
        #     print(f"index {i}, length of row {len(r)}")

        nrows = len(table_rows)

        for command in table_style_cmds:
            if command[0] not in {
                "BACKGROUND",
                "ROWBACKGROUNDS",
                "COLBACKGROUNDS",
            }:
                continue

            start_row = 0
            end_row = command[2][1]

            for label, row in (("start", start_row), ("end", end_row)):
                normalized_row = row if row >= 0 else nrows + row

                if not 0 <= normalized_row < nrows:
                    print(f"Table {table['title']!r} has {nrows} rows, but background command has invalid {label} row {row}: {command!r}"
                    )
                    print('break')
       
        rows_in_table.setStyle(TableStyle(more_table_style_cmds + table_style_cmds))
        story.extend([rows_in_table])
        story.append(Spacer(1, 10))

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
