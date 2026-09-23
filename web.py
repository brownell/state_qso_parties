#!/usr/bin/env python3
"""
Louisiana QSO Party Log Upload Application
Web interface for contestants to submit and validate Cabrillo log files
"""

from flask import Flask, json, render_template, request, jsonify
import os
from datetime import datetime
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

# Import the unified processor and database
from processor import process_single_log
from database import save_result
from config.config import SECRET_KEY, CONTEST_YEAR, BATCH_INPUT_DIR, ALLOWED_LOG_EXTENSIONS, RANKINGS

app = Flask(__name__)

# Ensure upload directory exists
os.makedirs(BATCH_INPUT_DIR, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_LOG_EXTENSIONS


def format_set_as_list(s):
    """Convert set to sorted list for display"""
    if not s:
        return []
    return sorted(list(s))


def format_result_for_display(result):
    """
    Convert the result dictionary to a format suitable for HTML display
    Handles sets, dicts, and other complex type
    """
    display_result = {}
    
    # Copy simple values
    simple_fields = [
        'callsign', 'exchange', 'overlay', 'location_type', 'mode_category',
        'power_level', 'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
        'total_multipliers', 'counties_worked_multiplier', 'states_worked_multiplier',
        'provinces_worked_multiplier', 'dx_worked_multiplier', 'mobile_bonus_points',
        'worked_n5lcc', 'num_n5lcc_contacts', 'name', 'club', 'claimed_score', 'year'
    ]
    
    for field in simple_fields:
        display_result[field] = result.get(field, 'N/A')
    
    # Convert sets to sorted lists
    display_result['counties_worked'] = format_set_as_list(result.get('counties_worked', set()))
    display_result['states_worked'] = format_set_as_list(result.get('states_worked', set()))
    display_result['provinces_worked'] = format_set_as_list(result.get('provinces_worked', set()))
    display_result['dx_worked'] = format_set_as_list(result.get('dx_worked', set()))
    display_result['counties_activated'] = format_set_as_list(result.get('counties_activated', set()))
    display_result['bands_worked'] = format_set_as_list(result.get('bands_worked', set()))
    
    # Format QSOs by band
    qsos_by_band = result.get('qsos_by_band', {})
    display_result['qsos_by_band'] = [
        {'band': band, 'count': count}
        for band, count in sorted(qsos_by_band.items(), key=lambda x: x[0])
    ]
    
    # Format QSOs by mode
    qsos_by_mode = result.get('qsos_by_mode', {})
    display_result['qsos_by_mode'] = [
        {'mode': mode, 'count': count}
        for mode, count in qsos_by_mode.items()
    ]
    

    # Format QSOs by hour
    try:
        temp = result.get('qsos_by_hour', {})
        display_result['qsos_by_hour'] = {}
        for key in temp:
            display_result['qsos_by_hour'][key] =  temp[key]
    except Exception as e:
        print(f"Error formatting qsos_by_hour for display: {e}")
        display_result['qsos_by_hour'] = []
    
    ## errors and warnings
    display_result['errors'] = result['errors']
    display_result['warnings'] = result['warnings']

    return display_result


@app.route('/')
def home():
    """Render the home page"""
    return render_template('home.html')

@app.route('/abbreviations')
def abbreviations():
    """Render the LA county abbreviations page (placeholder)"""
    return render_template('abbreviations.html')

@app.route('/activate')
def activate():
    """Render the county activation page (placeholder)"""
    return render_template('activate.html')

@app.route('/map')
def map():
    """ county map """
    return render_template('map.html')

# @app.route('/operations')
# def operations():
#     """  operations """
#     return render_template('operations.html')


@app.route('/results')
def results():
    """Render the results lookup page"""
    # Get available years from query params or config
    years = request.args.get('years', None)
    
    try:
        from config.config import CONTEST_YEARS
    except ImportError:
        # Fallback if CONTEST_YEARS not defined
        CONTEST_YEARS = ['2026', '2025', '2024']
    return render_template('results_lookup.html', available_years=years.split(',') if years else CONTEST_YEARS)


@app.route('/api/individual_results', methods=['POST'])
def api_individual_results():
    """
    Get individual results for a callsign and year.
    Returns result data and formatted rankings.
    """
    try:
        data = request.get_json()
        year = data.get('year', '').strip()
        if len(year) > 4:
            year = year[:4]
        callsign = data.get('callsign', '').strip().upper()
        
        if not year or not callsign:
            return jsonify({
                'success': False,
                'error': 'Year and callsign are required'
            }), 400
        
        # Get result from database
        from database import get_result
        result = get_result(year, callsign)
        
        if not result:
            return jsonify({
                'success': False,
                'error': f'No results found for {callsign} in {year}'
            }), 404
        
        rankings_display = {}
        sorted_rankings = dict(sorted(result.get('rankings', {}).items(), key=lambda item: item[1]))
        for code, rank in sorted_rankings.items():
            if code in RANKINGS:
                # Format as "Louisiana - Fixed QRP Power #2"
                rankings_display[RANKINGS[code]] = rank
        print(f"Rankings for {callsign} in {year}: {rankings_display}")

        # Format result for JSON (convert sets to lists)
        json_result = format_result_for_display(result)
        app.json.sort_keys = False
        return jsonify({
            'success': True,
            'result': json_result,
            'rankings_display': rankings_display
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/final_report/<year>')
def api_final_report(year):
    """
    Get final contest report HTML for a year.
    """
    temp_year = year
    if len(year) > 4:
        temp_year = year[:4]
    try:
        # Path to final report HTML
        try:
            from config.config import FINAL_REPORTS_DIR
        except ImportError:
            FINAL_REPORTS_DIR = 'data/final_reports'
        
        report_file = os.path.join(FINAL_REPORTS_DIR, f'final_report_{temp_year}.html')
        print(f'**********  report_file: {report_file}')
        
        if not os.path.exists(report_file):
            return jsonify({
                'success': False,
                'error': f'Final report for {year} not yet published'
            }), 404
        
        # Read HTML file
        with open(report_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract just the body content (skip html/head tags if present)
        import re
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
        if body_match:
            html_content = body_match.group(1)
        
        return jsonify({
            'success': True,
            'html': html_content
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/rules')
def rules():
    """Render the contest rules page (placeholder)"""
    return render_template('rules.html')

@app.route('/upload')
def upload():
    """Render the log upload page with user upload form"""
    return render_template('upload.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


@app.route('/process', methods=['POST'])
def upload_log(contest_year=CONTEST_YEAR):
    """
    Handle log file upload and validation
    Returns JSON response with validation results and formatted data
    """

    try:
        # Get form data
        form_data = {
            'year': request.form.get('year', '').strip(),
            'callsign': request.form.get('callsign', '').strip().upper(),
            'email': request.form.get('email', '').strip().lower(),
            'mode': request.form.get('mode', '').strip().upper(),
            'power': request.form.get('power', '').strip().upper(),
            'station_type': request.form.get('station_type', '').strip().upper(),
            'overlay': request.form.get('overlay', '').strip().upper()
        }
        
        # Validate required fields
        if not form_data['email'] and not form_data['callsign']:
            return jsonify({
                'success': False,
                'error': 'Callsign and Email address are required'
            }), 400
        
        # Get log content (either from file or pasted text)
        log_content = None
        
        if 'logfile' in request.files:
            file = request.files['logfile']
            if file:
                if file.filename and allowed_file(file.filename):
                    log_content = file.read().decode('utf-8', errors='ignore')
        
        if not log_content:
            log_text = request.form.get('log_text', '').strip()
            if log_text:
                log_content = log_text
            else:
                return jsonify({
                    'success': False,
                    'error': 'No log file provided. Please upload a file or paste log content.'
                }), 400
            
        ## Write this to data/batch_input/<year> as {callsign}.log
        log_file = f"{BATCH_INPUT_DIR}/year/{form_data['callsign']}.log"
        with open(log_file, 'w') as f:
            f.write(log_content)
        
        try:
            # Process the log file (validate, prepare, score)
            ## this function is ONLY called from the web interface
            result = process_single_log(
                contest_year,
                Path(log_file),
                form_data
            )

            ## if there were errors, delete the saved log file (don't keep invalid logs in batch input) and tell user
            if len(result.get('errors', [])) > 0:
                try:
                    os.remove(log_file)
                except FileNotFoundError:
                    result[errors].append("Log file not found for deletion after processing errors.")
                except PermissionError:
                    result[errors].append("Permission error when trying to delete log file after processing errors.")
                except OSError as e:
                    result[errors].append(f"OS error when trying to delete log file after processing errors: {str(e)}")
                print(f"⚠ There were errors in log for {result.get('callsign', 'unknown callsign')}")
                return jsonify({
                    'success': False,
                    'error': '<div>ERRORS FOUND: Could not process log file.<br>Please review the errors and fix log file and/or change form responses and resubmit.<br>List of Errors:</div>',
                    'errors': result.get('errors', [])
                    }), 400
            
            # Initialize empty rankings dict
            
            # Check if processing succeeded
            if result.get('is_valid', True) and not result.get('errors'):
                
                # Save result to database (will overwrite if exists)
                try:
                    if save_result(result):
                        print(f"✓ Saved result to database: {result['callsign']} ({result['year']})")
                    else:
                        print(f"⚠ Failed to save result to database: {result['callsign']}")
                except Exception as e:
                    print(f"⚠ Database save error: {e}")
                
                # Format the result for display (HTML rendered in browser, not saved)
                display_result = format_result_for_display(result)
                
                return jsonify({
                    'success': True,
                    'message': 'Log file processed successfully!',
                    'result': display_result
                })
            else:
                # Processing failed - return errors
                errors = result.get('errors', ['Unknown processing error'])
                return jsonify({
                    'success': False,
                    'error': 'Log processing failed',
                    'errors': errors
                }), 400
        finally:
            pass
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    import os, sys
    from datetime import datetime
    from config.config import CONTEST_YEAR
    
    # Get year from environment or command line
    if len(sys.argv) > 1:
        year = sys.argv[1]
    else:
        year = CONTEST_YEAR
    app.json.sort_keys = False
    app.run(debug=True, host='0.0.0.0', port=5000)
