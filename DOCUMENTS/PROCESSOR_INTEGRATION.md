# Louisiana QSO Party - Unified Log Processor Integration

Brownell Notes
Funtional FLow:
process_single_log - creates UnifiedLogProcessor instance
process_batch_logs - does all the log files in the incoming directory
process_log_details (in UnifiedLogProcessor instance; creates result object)
*** ambiguous DX????
    validate_and_parse - stores parsed QSOs - creates error and warning messages
    prepare_qsos - creates prepared object
    score_qsos



This update refactors your validation, preparation, and scoring modules into a single unified processor that:

1. ✅ Works in-memory (no intermediate files)
2. ✅ Uses consistent naming (strings, not integers)
3. ✅ Returns standardized result dictionary
4. ✅ Works for both web uploads and batch processing

## What's Changed

### Before (3 separate phases):
```
Validate → temp file → Prepare → temp file → Score → result
```

### After (1 unified process):
```
Process → result (all in memory)
```

## Files Included

1. **processor.py** - Unified log processor combining all three phases
2. **app.py** - Updated Flask app using the unified processor
3. **templates/upload.html** - HTML with results display
4. **static/css/upload.css** - Stylesheet
5. **static/js/upload.js** - JavaScript for results rendering

## Standardized Result Dictionary

The processor returns a consistent result dict with:

```python
{
    # Station Info
    'callsign': 'K5ABC',
    'name': 'John Smith',
    'category': 'nl_ph_lo',  # Short category name
    'overlay': None,  # 'WIRES', 'TB-WIRES', 'POTA', or None
    
    # Category Details (strings, not integers!)
    'location_type': 'NON-LA',  # 'DX', 'NON-LA', 'LA-FIXED', 'LA-ROVER'
    'mode_category': 'MIXED',  # 'PHONE', 'CW-DIGITAL', 'MIXED'
    'power_level': 'LOW',  # 'QRP', 'LOW', 'HIGH'
    'is_rover': False,
    
    # Scores
    'final_score': 1250,
    'qso_points': 625,
    'total_qsos': 350,
    'valid_qsos': 313,
    'total_multipliers': 5,
    'claimed_score': 1250,
    
    # Multipliers (sets)
    'parishes_worked': {'ORL', 'JEF', 'STB'},
    'parishes_worked_multiplier': 3,
    'states_worked': {'TX', 'MS'},
    'states_worked_multiplier': 2,
    'provinces_worked': set(),
    'provinces_multiplier': 0,
    'dx_worked': set(),
    'dx_worked_multiplier': 0,
    'parishes_activated': set(),  # For rovers
    
    # Bonuses
    'rover_bonus_points': 0,
    'worked_n5lcc': True,
    'num_n5lcc_contacts': 3,
    
    # Statistics (dicts)
    'qsos_by_band': {'160': 0, '80': 45, '40': 123, ...},
    'qsos_by_mode': {'Phone': 313, 'CW/Digital': 0},
    'qsos_by_hour': {0: 28, 1: 35, 2: 42, ...},
    'bands_worked': ['80', '40', '20'],
    'multipliers_by_band_mode': {
        '40-Phone': {'ORL', 'JEF', 'STB'},
        '20-Phone': {'ORL', 'TAN'}
    },
    
    # Validation Status
    'is_valid': True,
    'errors': [],
    'warnings': [],
    'has_valid_power': True,
    'has_valid_operator': True,
    'has_email': True,
}
```

## Installation

### 1. Copy Files

Place these files in your project:

```
your-project/
├── processor.py          # NEW: Unified processor
├── app.py               # UPDATED: Uses processor
├── templates/
│   └── upload.html      # UPDATED: Results display
├── static/
│   ├── css/
│   │   └── upload.css   # Styling
│   └── js/
│       └── upload.js    # Results rendering
└── config/
    └── config.py        # Your existing config
```

### 2. Required Data Files

Ensure you have:
- `data/LA_Parish_Abbrevs.txt` - All 64 LA parishes
- `data/WVE_Abbrevs.txt` - US states + Canadian provinces

### 3. Dependencies

```bash
pip install Flask werkzeug
```

## Usage

### For Web Upload (Single Log)

The Flask app in `app.py` already uses the unified processor:

```python
from processor import process_single_log

# In your upload route
result = process_single_log(
    log_path,
    email=form_email,
    mode=form_mode,
    power=form_power,
    station=form_station,
    overlay=form_overlay
)

if result['is_valid']:
    # Success - display results
    display_result = format_result_for_display(result)
    return jsonify({'success': True, 'result': display_result})
else:
    # Failed - show errors
    return jsonify({'success': False, 'errors': result['errors']})
```

### For Batch Processing (Multiple Logs)

```python
from processor import process_batch_logs
from pathlib import Path

# Process all logs in a directory
results = process_batch_logs(Path('logs/incoming'))

for result in results:
    if result['is_valid']:
        print(f"{result['callsign']}: {result['final_score']} points")
    else:
        print(f"{result['callsign']}: ERRORS - {result['errors']}")
```

### Custom Processing

```python
from processor import UnifiedLogProcessor
from pathlib import Path

# Create processor with your data files
processor = UnifiedLogProcessor(
    parish_file=Path('data/LA_Parish_Abbrevs.txt'),
    state_province_file=Path('data/WVE_Abbrevs.txt')
)

# Process a single log
result = processor.process_log(Path('log.cbr'))
```

## Key Features

### 1. In-Memory Processing

No intermediate files are created. Everything happens in memory:

- Validation parses and stores QSO lines
- Preparation expands multi-parish QSOs in memory
- Scoring processes the prepared QSOs directly

### 2. Consistent Naming

**Location Types (strings):**
- `'DX'` - DX station
- `'NON-LA'` - US/VE outside Louisiana  
- `'LA-FIXED'` - Louisiana fixed/portable
- `'LA-ROVER'` - Louisiana mobile/rover

**Mode Categories (strings):**
- `'PHONE'` - Phone only
- `'CW-DIGITAL'` - CW/Digital only
- `'MIXED'` - Both

**Power Levels (strings):**
- `'QRP'` - 5W or less
- `'LOW'` - 150W or less
- `'HIGH'` - Over 150W

**Overlays (strings or None):**
- `None` - No overlay
- `'WIRES'` - Wire antennas
- `'TB-WIRES'` - Tribander + wires
- `'POTA'` - Parks activation

### 3. Comprehensive Error Handling

```python
result = process_single_log(log_path)

# Check validity
if not result['is_valid']:
    print("Validation failed:")
    for error in result['errors']:
        print(f"  ERROR: {error}")
    for warning in result['warnings']:
        print(f"  WARNING: {warning}")
    return

# Process valid log
print(f"Callsign: {result['callsign']}")
print(f"Score: {result['final_score']}")
```

### 4. Works for Both Use Cases

**Web Upload:**
```python
# Single log with form validation
result = process_single_log(
    log_path,
    email='user@example.com',
    mode='mixed',
    power='low'
)
```

**Batch Processing:**
```python
# Multiple logs without form data
for log_file in Path('logs/incoming').glob('*.log'):
    result = process_single_log(log_file)
    # Process result...
```

## Migration from Old Code

### If You're Using Separate Modules

**Old approach:**
```python
# Three separate steps
from laqp.core.validator import validate_log
from laqp.core.preparation import prepare_log
from laqp.core.scoring import score_log

# Step 1
validation_result = validate_log(input_path)
if not validation_result.is_valid:
    # Handle errors...

# Step 2
prep_result = prepare_log(input_path, temp_path)

# Step 3
score_result = score_log(temp_path)
```

**New approach:**
```python
# Single step
from processor import process_single_log

result = process_single_log(input_path)

if not result['is_valid']:
    # Handle errors in result['errors']
else:
    # Use result['final_score'], etc.
```

### If You Want to Keep Old Modules

You can keep your existing modules and just use the processor for the web app:

1. Keep `validator.py`, `preparation.py`, `scoring.py` for batch processing
2. Use `processor.py` only for the web upload functionality
3. Eventually migrate batch processing to use the processor

## Testing

### Test with Sample Log

```bash
# Start Flask app
python app.py

# Visit http://localhost:5000
# Upload a test log file
```

### Verify Results

The web interface will display:
- Station information
- Score summary
- QSO statistics  
- Multipliers worked
- Bonuses applied
- Detailed breakdowns

### Check for Errors

If processing fails, check:
1. Are data files present? (`LA_Parish_Abbrevs.txt`, `WVE_Abbrevs.txt`)
2. Are they in the correct location? (check `config/config.py`)
3. Is the log format valid Cabrillo?
4. Check Flask console for error messages

## Troubleshooting

### "Module not found: processor"

Make sure `processor.py` is in the same directory as `app.py`:

```bash
your-project/
├── processor.py    # ← Must be here
├── app.py
└── ...
```

### "File not found: LA_Parish_Abbrevs.txt"

Update paths in `config/config.py`:

```python
COUNTIES_FILE = 'data/LA_Parish_Abbrevs.txt'
WVE_ABBREVS_FILE = 'data/WVE_Abbrevs.txt'
```

### "is_valid is always False"

Check `result['errors']` for details:

```python
if not result['is_valid']:
    print("Errors:")
    for error in result['errors']:
        print(f"  - {error}")
```

### Results Not Displaying

1. Check browser console for JavaScript errors
2. Verify Flask is returning JSON properly
3. Check that all result dict fields are present

## Next Steps

1. ✅ Copy processor.py and updated app.py to your project
2. ✅ Ensure data files are in place
3. ✅ Test with sample log
4. ⬜ Migrate batch processing script to use processor
5. ⬜ Deploy to production

## Benefits Summary

✅ **Simpler** - One function call instead of three  
✅ **Faster** - No file I/O between phases  
✅ **Cleaner** - No temp files to manage  
✅ **Consistent** - Same naming everywhere  
✅ **Flexible** - Works for web and batch  
✅ **Maintainable** - Single source of truth  

---

**Questions?** Check the inline documentation in `processor.py` or contact the development team.
