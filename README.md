# Louisiana QSO Party Log Processor

Contest log processing system for the Louisiana QSO Party, hosted by Jefferson Amateur Radio Club.

### Adapted from Texas QSO Party software created by Charles Sanders, NO5W

## Leaderboards and Certificates
The current rules specify awards for the following categories. In 2026, we are not sending out awards or certificates. For everyone - no matter were they placed - the may come to the website 15 days after the contest and see an HTML certificate, which they may print, that shows where they placed in all the relevent categories:

### Leaderboard Categories
TBH

### Clarifications to the Rules
- Users fill out a web form to upload the Cabrillo log file. If anything in the header section of the log file disagrees with what was entered - or is missing -  the log file is rejected immediately and the user is asked to fix the log file or change the responses on the form, and resubmit. A log file may be resubmitted any number of times, with each new upload replacing the previous ones. Fields required on the form and in the Cabrillo log file are: call sign, email, power, mode, and station type. Overlay is an OPTIONAL field, but if included the values on the upload form and in the Cabrillo file must match.

- QSOs that do not match the “CATEGORY-MODE” are ignored and receive no points. For example, Phone QSOs are ignored if the mode is “CW/DIGITAL”. Of course, "MIXED" mode allows any mode in QSOs.

- The operator’s QTH is taken from the QSOs present, and not the "LOCATION" element in the Cabrillo file. Except for someone who has declared himself as a “Rover” all QSOs after the first must have the same QTH as the first. Any that do not meet that requirement are ignored and receive no points.

- QSOs from one non-LA operator to another are ignored and receive no points. But QSOs from one LA operator to another are valid for points and multipliers.

- The "bonus" LA call sign used is N5LCC. One OR MORE QSOs to N5LCC, regardless of band or mode, receive 100 bonus points. Contacting N5LCC multiple times does not increase bonus points. This callsign is not part of the rankings in the contest. Also it may have multiple calling QTH, and may be operating at two different frequencies on the same band as long as the mode is different.

- Warning messages are generated for all these situations so the user knows which QSOs were ignored. The log has been accepted for scoring if there are warning messages, but if the user wants to make corrections and resubmit, the last submission is used for scoring and ranking.


## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- sqlalchemy (database ORM)
- flask (web framework)
- pandas (data analysis)
- python-dateutil (date parsing)

### 2. Create Data Files

Create the county abbreviations file at `data/LA_County_Abbrevs.txt`:
```
ACAD
ALLE
ASCE
...
(all 64 Louisiana counties)
```

### 3. Initialize Database

```bash
python -c "from laqp.models.database import Database; from config.config import DATABASE_URL; db = Database(DATABASE_URL); db.create_tables()"
```

### 4. Create Directory Structure

```bash
python -c "from config.config import ensure_directories; ensure_directories()"
```

## Usage

### Batch Processing (Command Line)

Process all logs in the `logs/incoming/` directory:

```bash
# Full processing pipeline
python scripts/process_all_logs.py

# Validation only
python scripts/process_all_logs.py --validate-only

# Skip database storage
python scripts/process_all_logs.py --skip-db
```

**Important Notes**:
- **Incoming logs are preserved**: Files in `logs/incoming/` are copied (not moved), so they remain there for reference
- **Output directories are cleaned**: On each run, the following directories are emptied before processing:
  - `logs/validated/`
  - `logs/prepared/`
  - `logs/problems/`
  - `logs/reports/`
  - `output/scores/`
  - `output/statistics/`
- This ensures you're always looking at results from the current run, not mixed with previous runs

### Web Application (Future)

```bash
# Start Flask development server
python -m flask --app web.app run

# Production with gunicorn
gunicorn -w 4 web.app:app
```

## Key Differences: LAQP vs TQP

### Categories
- **TQP**: Power (QRP/LOW/HIGH) × Mode (CWO/PHO/DGO/MIX) × Location (DX/NTX/TX-Fixed/TX-Mobile) × Operators (SO/MO)
- **LAQP**: Mode only (Phone/CW-Digital/Mixed) × Location (DX/Non-LA/LA-Fixed/LA-Rover)
  - Power is tracked but doesn't create separate categories
  - Number of operators is ignored (everyone lumped together)
  - Overlays (WIRES/TB-WIRES/POTA) are separate awards, not categories

### Scoring
- **TQP**: 2 pts phone, 3 pts CW/digital
- **LAQP**: 2 pts phone, 4 pts CW/digital

### Multipliers
- **TQP**: Counted once for entire contest
- **LAQP**: Counted per band AND per mode type (CW/Digital vs Phone)
  - Example: Working CADDO county on 40m CW and 40m SSB = 2 multipliers

### Bonuses
- **TQP**: 
  - Mobile tracking: 500 pts per 5 counties worked per mobile
  - County activation: 1000 pts per county with 5+ QSOs
- **LAQP**:
  - N5LCC bonus: 100 pts one-time for working club station
  - Rover activation: 50 pts per county activated (rovers only)

### Contest Period
- **TQP**: Two sessions (Saturday afternoon + Sunday afternoon)
- **LAQP**: Single session (Saturday 1400Z - Sunday 0200Z)

## Development Roadmap

### Phase 1: Core Processing (Current)
- [x] Project structure
- [x] Configuration system
- [x] Database schema
- [x] Log validator
- [ ] Log preparation (adapt from TQP)
- [ ] Scoring engine (adapt from TQP)
- [ ] Statistics generator (adapt from TQP)

### Phase 2: Command Line Tools
- [x] Batch processor
- [ ] Report generator
- [ ] Database utilities
- [ ] Leaderboard generator

### Phase 3: Web Application
- [ ] Flask app setup
- [ ] Log upload interface
- [ ] Real-time validation
- [ ] Score lookup
- [ ] Public results page

### Phase 4: Advanced Features
- [ ] Duplicate detection across logs
- [ ] Log checking (spot mismatches)
- [ ] Certificate generation
- [ ] Email notifications
- [ ] Admin dashboard

## LA Rules Summary

### Scoring
1. **QSO Points**: 2 for phone, 4 for CW/digital
2. **Multipliers**: 
   - Non-LA: LA counties worked (per band/mode)
   - LA: counties + states + provinces + DXCC (per band/mode)
3. **Score**: QSO points × multipliers + bonuses

### Categories (12 total)
- Non-LA: Phone Only, CW/Digital Only, Mixed
- LA Fixed: Phone Only, CW/Digital Only, Mixed  
- LA Rover: Phone Only, CW/Digital Only, Mixed
- (Each category can have 3 power levels: QRP/Low/High)

### Overlays (Separate Awards)
- WIRES: Wire antennas only
- TB-WIRES: Tribander + wires
- POTA: Parks/campgrounds/refuges

## Contact

Louisiana QSO Party
Jefferson Amateur Radio Club
questions@laqp.org

Contest Manager: KJ5BYZ
