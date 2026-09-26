#!/usr/bin/env python3
"""
Louisiana QSO Party - Generate Final Report HTML

Generates HTML final report with leaderboards for a contest year.
Saves to data/results/final_report_{year}.html
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from leaderboards import generate_leaderboards
from config.config import FINAL_REPORTS_DIR, FINAL_REPORT_TXT, FINAL_REPORTS_DIR


def generate_final_report_html(year: str, output_dir: str = FINAL_REPORTS_DIR):
    """
    Generate final report HTML for a year.
    
    Args:
        year: Contest year
        output_dir: Directory to save HTML file
    """
    print("=" * 60)
    print(f"Louisiana QSO Party - Generate Final Report HTML ({year})")
    print("=" * 60)
    print()
    
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate leaderboards (don't save rankings again)
    print("Generating leaderboards...")
    sections = generate_leaderboards(year, LEADERBOARDS, RANKINGS, save_rankings=False)
    
    # Generate HTML
    print("Creating HTML report...")
    html = _create_html_document(year, sections)
    
    # Save to file
    output_file = output_path / f"final_report_{year}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Summary
    total_tables = sum(len(section['tables']) for section in sections)
    total_entries = sum(
        len(table['rows']) 
        for section in sections 
        for table in section['tables']
    )
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Sections: {len(sections)}")
    print(f"Tables: {total_tables}")
    print(f"Total entries: {total_entries}")
    print(f"Saved to: {output_file}")
    print()


def _create_html_document(year: str, sections: list) -> str:
    """Create complete HTML document"""
    
    html_parts = []
    
    # Document header
    html_parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Louisiana QSO Party {year} - Final Results</title>
    <style>
{_get_css()}
    </style>
</head>
<body>
    <div class="container">
        <header class="report-header">
            <h1>Louisiana QSO Party {year}</h1>
            <h2>Final Results</h2>
            <p class="generated-date">Generated: {datetime.now().strftime('%B %d, %Y')}</p>
        </header>
        
        <div class="report-intro">
            {FINAL_REPORT_TXT if FINAL_REPORT_TXT else '<p>Congratulations to all participants!</p>'}
        </div>
""")
    
    # Generate HTML for each section
    for section in sections:
        html_parts.append(_generate_section_html(section))
    
    # Document footer
    html_parts.append("""
        <footer class="report-footer">
            <p>&copy; 2026 Jefferson Amateur Radio Club</p>
            <p>Louisiana QSO Party</p>
        </footer>
    </div>
</body>
</html>
""")
    
    return ''.join(html_parts)


def _generate_section_html(section: dict) -> str:
    """Generate HTML for a section"""
    html_parts = []
    
    # Section header
    html_parts.append(f"""
        <div class="section">
            <h2 class="section-title">{section['section_title']}</h2>
""")
    
    # Generate tables
    for table in section['tables']:
        html_parts.append(_generate_table_html(table))
    
    html_parts.append("        </div>\n")
    
    return ''.join(html_parts)


def _generate_table_html(table: dict) -> str:
    """Generate HTML for a leaderboard table (Excel-like with gridlines)"""
    html_parts = []
    
    # Table title
    html_parts.append(f"""
            <div class="table-container">
                <h3 class="table-title">{table['title']}</h3>
                <table class="leaderboard-table">
                    <thead>
                        <tr>
""")
    
    # Table headers
    for header in table['headers']:
        html_parts.append(f"                            <th>{header}</th>\n")
    
    html_parts.append("""                        </tr>
                    </thead>
                    <tbody>
""")
    
    # Table rows
    for row in table['rows']:
        html_parts.append("                        <tr>\n")
        for i, value in enumerate(row):
            if value == -1:
                value = "N/A"  # Empty cell for -1
            # First column (Rank) centered, rest left-aligned
            cell_class = "rank-cell" if i == 0 else "data-cell"
            html_parts.append(f'                            <td class="{cell_class}">{value}</td>\n')
        html_parts.append("                        </tr>\n")
    
    html_parts.append("""                    </tbody>
                </table>
            </div>
""")
    
    return ''.join(html_parts)


def _get_css() -> str:
    """Return CSS for Excel-like table styling"""
    return """
/* Louisiana QSO Party Final Report CSS */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Courier New', Courier, monospace;
    background-color: #f5f5f5;
    padding: 20px;
    line-height: 1.4;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: #fff;
    padding: 40px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.report-header {
    text-align: center;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 3px solid #8B0000;
}

.report-header h1 {
    font-family: Georgia, serif;
    font-size: 2.5rem;
    color: #8B0000;
    margin-bottom: 10px;
}

.report-header h2 {
    font-family: Georgia, serif;
    font-size: 1.8rem;
    color: #333;
    margin-bottom: 10px;
}

.generated-date {
    font-family: Arial, sans-serif;
    font-size: 0.9rem;
    color: #666;
    font-style: italic;
}

.report-intro {
    font-family: Georgia, serif;
    font-size: 1.1rem;
    margin: 30px 0;
    padding: 20px;
    background: #f9f9f9;
    border-left: 4px solid #8B0000;
}

.section {
    margin: 40px 0;
    page-break-inside: avoid;
}

.section-title {
    font-family: Georgia, serif;
    font-size: 1.8rem;
    color: #8B0000;
    margin-bottom: 30px;
    padding-bottom: 10px;
    border-bottom: 2px solid #8B0000;
}

.table-container {
    margin: 30px 0;
    page-break-inside: avoid;
}

.table-title {
    font-family: Arial, sans-serif;
    font-size: 1.2rem;
    color: #333;
    margin-bottom: 10px;
    font-weight: bold;
}

/* Excel-like table styling */
.leaderboard-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.95rem;
    margin-bottom: 30px;
    border: 2px solid #000;
}

.leaderboard-table thead {
    background-color: #4472C4;
    color: #fff;
}

.leaderboard-table th {
    padding: 10px 8px;
    text-align: left;
    font-weight: bold;
    border: 1px solid #000;
    border-right: 1px solid #fff;
}

.leaderboard-table th:last-child {
    border-right: 1px solid #000;
}

.leaderboard-table tbody tr:nth-child(even) {
    background-color: #f0f0f0;
}

.leaderboard-table tbody tr:nth-child(odd) {
    background-color: #fff;
}

.leaderboard-table tbody tr:hover {
    background-color: #e8f0ff;
}

.leaderboard-table td {
    padding: 8px;
    border: 1px solid #000;
}

.leaderboard-table td.rank-cell {
    text-align: center;
    font-weight: bold;
    background-color: #f9f9f9;
    width: 60px;
}

.leaderboard-table td.data-cell {
    text-align: left;
}

/* Rank highlighting */
.leaderboard-table tbody tr:nth-child(1) {
    background-color: #FFD700 !important;
    font-weight: bold;
}

.leaderboard-table tbody tr:nth-child(2) {
    background-color: #C0C0C0 !important;
}

.leaderboard-table tbody tr:nth-child(3) {
    background-color: #CD7F32 !important;
}

.report-footer {
    margin-top: 60px;
    padding-top: 20px;
    border-top: 2px solid #ddd;
    text-align: center;
    font-family: Georgia, serif;
    color: #666;
}

/* Print styles */
@media print {

    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }

    .no-print { display: none; }

    body {
        background: #fff;
        padding: 0;
    }

    .container {
        box-shadow: none;
        padding: 20px;
    }

    .section {
        page-break-before: auto;
    }

    .table-container {
        page-break-inside: avoid;
    }

    .leaderboard-table tbody tr:hover {
        background-color: transparent;
    }
}
"""


if __name__ == "__main__":
    import sys
    from config.config import CONTEST_YEAR, FINAL_REPORTS_DIR
    
    # Get year from environment or command line
    if len(sys.argv) > 1:
        year = sys.argv[1]
    else:
        year = CONTEST_YEAR
    
    generate_final_report_html(year, FINAL_REPORTS_DIR)
