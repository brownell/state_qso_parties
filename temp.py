
from pprint import pprint
import sys
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime, timezone
from unittest import result
from cabrillo.parser import parse_log_file
from cabrillo.qso import frequency_to_band_m
from utilities import generate_index_key, get_dxcc, writefile
from share import SHARED as s
from config.config import DATABASE_FILE, DB_DROP
from config.config_txqp import RANKINGS

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import (
    CONTEST_YEAR, BATCH_INPUT_DIR, HQ_FIELDS
)
SCRIPT_DIR = Path(__file__).resolve().parent

dir_path = (SCRIPT_DIR / BATCH_INPUT_DIR / CONTEST_YEAR).resolve()
foo['check']['scored_mode'] = 

{"total_logs": 413, "rejected_logs": 0, "dx_logs": 10, "us_logs": 256, "cdn_logs": 2, "tx_mobile_logs": 18, "tx_fixed_logs": 107, "unclassed_logs": 0, "total_qsos": 52779, "valid_qsos": 0, "qsos_with_tx": 47580, "qsos_with_us": 51858, "qsos_with_canada": 2110, "qsos_with_dx": 3592, "duplicate_qsos": 971, "nils": 3438, "busteds": 134, "other_invalid_qsos": 305, "uniques": 18998, "year": "2026", "counties_worked": "[\"ANDE\", \"ANDR\", \"ANGE\", \"ARAN\", \"ARCH\", \"ARMS\", \"ATAS\", \"AUST\", \"BAIL\", \"BAND\", \"BAST\", \"BAYL\", \"BEE\", \"BELL\", \"BEXA\", \"BLAN\", \"BORD\", \"BOSQ\", \"BOWI\", \"BREW\", \"BRIS\", \"BROO\", \"BROW\", \"BURL\", \"BURN\", \"BZIA\", \"BZOS\", \"CALD\", \"CALH\", \"CALL\", \"CAMP\", \"CARS\", \"CASS\", \"CHAM\", \"CHER\", \"CHIL\", \"CLAY\", \"CMRN\", \"COKE\", \"COLN\", \"COLO\", \"COLW\", \"COMA\", \"COML\", \"COOK\", \"CORY\", \"CRAN\", \"CROC\", \"CULB\", \"DALM\", \"DALS\", \"DAWS\", \"DELT\", \"DENT\", \"DEWI\", \"DONL\", \"DUVA\", \"EAST\", \"ECTO\", \"ELLI\", \"EPAS\", \"FANN\", \"FAYE\", \"FBEN\", \"FISH\", \"FOAR\", \"FRAN\", \"FREE\", \"GALV\", \"GILL\", \"GLAS\", \"GOLI\", \"GONZ\", \"GRAY\", \"GREG\", \"GRIM\", \"GRSN\", \"GUAD\", \"HALL\", \"HAMI\", \"HANS\", \"HARR\", \"HART\", \"HASK\", \"HAYS\", \"HDMN\", \"HEMP\", \"HEND\", \"HIDA\", \"HILL\", \"HOCK\", \"HOOD\", \"HOPK\", \"HOUS\", \"HOWA\", \"HRDN\", \"HRSN\", \"HUNT\", \"JACK\", \"JDAV\", \"JEFF\", \"JHOG\", \"JKSN\", \"JOHN\", \"JONE\", \"JWEL\", \"KARN\", \"KAUF\", \"KENY\", \"KERR\", \"KING\", \"KINN\", \"KLEB\", \"KNOX\", \"LAMA\", \"LAMB\", \"LAMP\", \"LAVA\", \"LEE\", \"LEON\", \"LIBE\", \"LIPS\", \"LIVO\", \"LLAN\", \"LSAL\", \"LUBB\", \"MADI\", \"MARI\", \"MART\", \"MASO\", \"MEDI\", \"MGMY\", \"MIDL\", \"MILA\", \"MILL\", \"MITC\", \"MLEN\", \"MMUL\", \"MONT\", \"MOOR\", \"MORR\", \"MOTL\", \"NACO\", \"NAVA\", \"NUEC\", \"OCHI\", \"ORAN\", \"PANO\", \"PARK\", \"PARM\", \"PECO\", \"POLK\", \"POTT\", \"PPIN\", \"RAIN\", \"RAND\", \"RBSN\", \"REAG\", \"REAL\", \"REFU\", \"ROBE\", \"ROCK\", \"RRIV\", \"RUNN\", \"RUSK\", \"SABI\", \"SAUG\", \"SCUR\", \"SHAC\", \"SHMN\", \"SJAC\", \"SMIT\", \"SOME\", \"SPAT\", \"SSAB\", \"STAR\", \"STEP\", \"STER\", \"SWIS\", \"TARR\", \"TAYL\", \"TERY\", \"TGRE\", \"THRO\", \"TITU\", \"TRAV\", \"TRIN\", \"UPSH\", \"UPTO\", \"UVAL\", \"VICT\", \"VZAN\", \"WALK\", \"WALL\", \"WARD\", \"WASH\", \"WEBB\", \"WHAR\", \"WHEE\", \"WICH\", \"WILB\", \"WILY\", \"WINK\", \"WISE\", \"WLSN\", \"WMSN\", \"WOOD\", \"YOUN\", \"ZAPA\", \"ZAVA\"]", "states_worked": "[\"AK\", \"AL\", \"AR\", \"AZ\", \"CA\", \"CO\", \"CT\", \"DE\", \"FL\", \"GA\", \"HI\", \"IA\", \"ID\", \"IL\", \"IN\", \"KS\", \"KY\", \"LA\", \"MA\", \"MD\", \"ME\", \"MI\", \"MN\", \"MO\", \"MS\", \"MT\", \"NC\", \"ND\", \"NE\", \"NH\", \"NJ\", \"NM\", \"NV\", \"NY\", \"OH\", \"OK\", \"OR\", \"PA\", \"RI\", \"SC\", \"SD\", \"TN\", \"UT\", \"VA\", \"VT\", \"WA\", \"WI\", \"WV\", \"WY\"]", "provinces_worked": "[\"AB\", \"BC\", \"MB\", \"NB\", \"NL\", \"NS\", \"NX5M\", \"ON\", \"PE\", \"QC\", \"SK\", \"VE4\", \"VE9\"]", "dx_worked": "[\"Aland Islands\", \"American Samoa\", \"Anguilla\", \"Argentina\", \"Asiatic Russia\", \"Asiatic Turkey\", \"Australia\", \"Austria\", \"Bahamas\", \"Barbados\", \"Belarus\", \"Belgium\", \"Brazil\", \"Bulgaria\", \"Canary Islands\", \"Ceuta & Melilla\", \"Chile\", \"Colombia\", \"Costa Rica\", \"Crete\", \"Croatia\", \"Cuba\", \"Czech Republic\", \"Denmark\", \"Dominican Republic\", \"Ecuador\", \"England\", \"Estonia\", \"European Russia\", \"European Turkey\", \"Fed. Rep. of Germany\", \"Finland\", \"France\", \"Georgia\", \"Greece\", \"Guam\", \"Guantanamo Bay\", \"Honduras\", \"Hungary\", \"Iceland\", \"India\", \"Ireland\", \"Israel\", \"Italy\", \"Japan\", \"Kaliningrad\", \"Kenya\", \"Latvia\", \"Lithuania\", \"Luxembourg\", \"Martinique\", \"Mexico\", \"Moldova\", \"Netherlands\", \"Norfolk Island\", \"Norway\", \"Oman\", \"Panama\", \"Peru\", \"Philippines\", \"Poland\", \"Portugal\", \"Puerto Rico\", \"Qatar\", \"Romania\", \"Sardinia\", \"Saudi Arabia\", \"Scotland\", \"Serbia\", \"Seychelles\", \"Slovak Republic\", \"Slovenia\", \"South Africa\", \"Spain\", \"St. Helena\", \"St. Lucia\", \"Sweden\", \"Switzerland\", \"Trinidad & Tobago\", \"US Virgin Islands\", \"Ukraine\", \"Uruguay\", \"Wales\"]", "counties_activated": "[]", "rejected_logs_filenames": "[]", "qsos_by_hour": "[4263, 3794, 2817, 2540, 2783, 2493, 3422, 2448, 2758, 3192, 2615, 2690, 3304, 2599, 1872, 1704, 2019, 2395]", "nil_calls": "[[\"AA0FO\", \"K5EC\"], [\"AA0FO\", \"K5EC\"], [\"AA0FO\", \"K5EC\"], [\"AA0FO\", \"K5EC\"], [\"AA0FO\", \"WA5DTK\"], [\"AA0FO\", \"WA5DTK\"], [\"AA3R\", \"N5T\"], [\"AA3R\", \"N5T\"], [\"AA3R\", \"N5NU\"], [\"AA3R\", \"N5NU\"], [\"AA3R\", \"K5K\"], [\"AA3R\", \"K5K\"], [\"AA3R\", \"K5K\"], [\"AA3R\", \"K5K\"], [\"AA3R\", \"W5GCX\"], [\"AA3R\", \"W5GCX\"], [\"AA3R\", \"W5AL\"], [\"AA3R\", \"W5AL\"], [\"AA3R\", \"N5XZ\"], [\"AA3R\", \"N5XZ\"], [\"AA3R\", \"N5VBL\"], [\"AA3R\", \"N5VBL\"], [\"AA3R\", \"WB5BKL\"], [\"AA3R\", \"WB5BKL\"], [\"AA3R\", \"K5TIA\"], [\"AA3R\", \"K5TIA\"], [\"AA3R\", \"W5ACQ\"], [\"AA3R\", \"W5ACQ\"], [\"AA3R\", \"KK5TY\"], [\"AA3R\", \"KK5TY\"], [\"AA3R\", \"WA5DTK\"], [\"AA3R\", \"WA5DTK\"], [\"AA3R\", \"K5EC\"], [\"AA3R\", \"K5EC\"], [\"AA3R\", \"K5EC\"], [\"AA3R\", \"K5EC\"], [\"AA3R\", \"WA5DTK\"], [\"AA3R\", \"WA5DTK\"], [\"AA3R\", \"W5ACQ\"], [\"AA3R\", \"W5ACQ\"], [\"AA3R\", \"WA5DTK\"], [\"AA3R\", \"WA5DTK\"], [\"AA3R\", \"KI5NCJ\"], [\"AA3R\", \"KI5NCJ\"], [\"AA3R\", \"AD4EB\"], [\"AA3R\", \"AD4EB\"], [\"AA3R\", \"W5ACQ\"], [\"AA3R\", \"W5ACQ\"], [\"AA3R\", \"N5JJ\"], [\"AA3R\", \"N5JJ\"], [\"AA3R\", \"WB5BKL\"], [\"AA3R\", \"WB5BKL\"], [\"AA3R\", \"KD5ZZU\"], [\"AA3R\", \"KD5ZZU\"], [\"AA3R\", \"K5T\"], [\"AA3R\", \"K5T\"], [\"AA3R\", \"W5ESE\"], [\"AA3R\", \"W5ESE\"], [\"AA5AH\", \"W0UC\"], [\"AA5AH\", \"W0UC\"], [\"AA5JF\", \"K5TIA\"], [\"AA5JF\", \"K5TIA\"], [\"AA5JF\", \"K5K\"], [\"AA5JF\", \"K5K\"], [\"AA5UN\", \"N5TJ\"], [\"AA5UN\", \"N5TJ\"], [\"AA5UN\", \"N1LN\"], [\"AA5UN\", \"N1LN\"], [\"AA6MU\", \"W5LXS\"], [\"AA6MU\", \"W5LXS\"], [\"AA6MU\", \"AD4EB\"], [\"AA6MU\", \"AD4EB\"], [\"AA6MU\", \"N5RZ\"], [\"AA6MU\", \"N5RZ\"], [\"AA6MU\", \"KG5OWB\"], [\"AA6MU\", \"KG5OWB\"], [\"AA7V\", \"AD4EB\"], [\"AA7V\", \"AD4EB\"], [\"AA7V\", \"KG5OWB\"], [\"AA7V\", \"KG5OWB\"], [\"AA7V\", \"WA5LFD\"], [\"AA7V\", \"WA5LFD\"], [\"AC6ZM\", \"AD4EB\"], [\"AC6ZM\", \"AD4EB\"], [\"AC7DD\", \"W5ACQ\"], [\"AC7DD\", \"W5ACQ\"], [\"AC7DD\", \"N5XZ\"], [\"AC7DD\", \"N5XZ\"], [\"AD4EB\", \"WB5BKL\"], [\"AD4EB\", \"WB5BKL\"], [\"AD4EB\", \"N0TT\"], [\"AD4EB\", \"N0TT\"], [\"AD4EB\", \"N0TT\"], [\"AD4EB\", \"N0TT\"], [\"AD4EB\", \"W5JK\"], [\"AD4EB\", \"W5JK\"], [\"AD4EB\", \"W5JK\"], [\"AD4EB\", \"W5JK\"], [\"AD4EB\", \"NX5M\"], [\"AD4EB\", \"NX5M\"], [\"AD4EB\", \"NX5M\"], [\"AD4EB\", \"NX5M\"], [\"AD4EB\", \"N0TT\"], [\"AD4EB\", \"N0TT\"], [\"AD4EB\", \"N5XZ\"], [\"AD4EB\", \"N5XZ\"], [\"AD4EB\", \"N5EP\"], [\"AD4EB\", \"N5EP\"], [\"AD4EB\", \"K0WRY\"], [\"AD4EB\", \"K0WRY\"], [\"AD4EB\", \"N3KN\"], [\"AD4EB\", \"N3KN\"], [\"AD4EB\", \"K2QB\"], [\"AD4EB\", \"K2QB\"], [\"AD4EB\", \"K5YX\"], [\"AD4EB\", \"K5YX\"], [\"AD4EB\", \"N9MS\"], [\"AD4EB\", \"N9MS\"], [\"AD4EB\", \"N9MS\"], [\"AD4EB\", \"N9MS\"], [\"AD4EB\", \"KV8Q\"], [\"AD4EB\", \"KV8Q\"], [\"AD4EB\", \"VA6RCN\"], [\"AD4EB\", \"VA6RCN\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"VE3YT\"], [\"AD4EB\", \"VE3YT\"], [\"AD4EB\", \"DL5AXX\"], [\"AD4EB\", \"DL5AXX\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"K3TW\"], [\"AD4EB\", \"K3TW\"], [\"AD4EB\", \"NU5DE\"], [\"AD4EB\", \"NU5DE\"], [\"AD4EB\", \"N5YA\"], [\"AD4EB\", \"N5YA\"], [\"AD4EB\", \"N5YA\"], [\"AD4EB\", \"N5YA\"], [\"AD4EB\", \"N4AO\"], [\"AD4EB\", \"N4AO\"], [\"AD4EB\", \"N7EPD\"], [\"AD4EB\", \"N7EPD\"], [\"AD4EB\", \"W4YE\"], [\"AD4EB\", \"W4YE\"], [\"AD4EB\", \"VE3SIF\"], [\"AD4EB\", \"VE3SIF\"], [\"AD4EB\", \"K0ZR\"], [\"AD4EB\", \"K0ZR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"KG5IEE\"], [\"AD4EB\", \"KG5IEE\"], [\"AD4EB\", \"VE3SIF\"], [\"AD4EB\", \"VE3SIF\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"VE3YT\"], [\"AD4EB\", \"VE3YT\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"N8II\"], [\"AD4EB\", \"N8II\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"K6KQV\"], [\"AD4EB\", \"K6KQV\"], [\"AD4EB\", \"AJ4F\"], [\"AD4EB\", \"AJ4F\"], [\"AD4EB\", \"W5GCX\"], [\"AD4EB\", \"W5GCX\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"N5EP\"], [\"AD4EB\", \"N5EP\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"WA5DTK\"], [\"AD4EB\", \"WA5DTK\"], [\"AD4EB\", \"W5LXS\"], [\"AD4EB\", \"W5LXS\"], [\"AD4EB\", \"KY4L\"], [\"AD4EB\", \"KY4L\"], [\"AD4EB\", \"K5TIA\"], [\"AD4EB\", \"K5TIA\"], [\"AD4EB\", \"K8MV\"], [\"AD4EB\", \"K8MV\"], [\"AD4EB\", \"W9QL\"], [\"AD4EB\", \"W9QL\"], [\"AD4EB\", \"WB5BKL\"], [\"AD4EB\", \"WB5BKL\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"N2MF\"], [\"AD4EB\", \"N2MF\"], [\"AD4EB\", \"N2MF\"], [\"AD4EB\", \"N2MF\"], [\"AD4EB\", \"N2MF\"], [\"AD4EB\", \"N2MF\"], [\"AD4EB\", \"K3TW\"], [\"AD4EB\", \"K3TW\"], [\"AD4EB\", \"NX5M\"], [\"AD4EB\", \"NX5M\"], [\"AD4EB\", \"AF5CC\"], [\"AD4EB\", \"AF5CC\"], [\"AD4EB\", \"AF5CC\"], [\"AD4EB\", \"AF5CC\"], [\"AD4EB\", \"AA7V\"], [\"AD4EB\", \"AA7V\"], [\"AD4EB\", \"WA2JQK\"], [\"AD4EB\", \"WA2JQK\"], [\"AD4EB\", \"N9GXA\"], [\"AD4EB\", \"N9GXA\"], [\"AD4EB\", \"KG5VK\"], [\"AD4EB\", \"KG5VK\"], [\"AD4EB\", \"WA5LFD\"], [\"AD4EB\", \"WA5LFD\"], [\"AD4EB\", \"WA5DTK\"], [\"AD4EB\", \"WA5DTK\"], [\"AD4EB\", \"KG5OWB\"], [\"AD4EB\", \"KG5OWB\"], [\"AD4EB\", \"K5IZO\"], [\"AD4EB\", \"K5IZO\"], [\"AD4EB\", \"N6DW\"], [\"AD4EB\", \"N6DW\"], [\"AD4EB\", \"K4NMR\"], [\"AD4EB\", \"K4NMR\"], [\"AD4EB\", \"DL5AXX\"], [\"AD4EB\", \"DL5AXX\"], [\"AD4EB\", \"N2MF\"], [\"AD4EB\", \"N2MF\"], [\"AD4EB\", \"K0PC\"], [\"AD4EB\", \"K0PC\"], [\"AD4EB\", \"KU8E\"], [\"AD4EB\", \"KU8E\"], [\"AD4EB\", \"KE0TT\"], [\"AD4EB\", \"KE0TT\"], [\"AD4EB\", \"K4BAI\"], [\"AD4EB\", \"K4BAI\"], [\"AD4EB\", \"N7EPD\"], [\"AD4EB\", \"N7EPD\"], [\"AD4EB\", \"N5JJ\"], [\"AD4EB\", \"N5JJ\"], [\"AD4EB\", \"K4ZGB\"], [\"AD4EB\", \"K4ZGB\"], [\"AD4EB\", \"N2MF\"], [\"AD4EB\", \"N2MF\"], [\"AD4EB\", \"N7EPD\"], [\"AD4EB\", \"N7EPD\"], [\"AD4EB\", \"N5XZ\"], [\"AD4EB\", \"N5XZ\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"NE8P\"], [\"AD4EB\", \"NE8P\"], [\"AD4EB\", \"W9QL\"], [\"AD4EB\", \"W9QL\"], [\"AD4EB\", \"W1QK\"], [\"AD4EB\", \"W1QK\"], [\"AD4EB\", \"N5JJ\"], [\"AD4EB\", \"N5JJ\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"KA0PQW\"], [\"AD4EB\", \"WA2QAU\"], [\"AD4EB\", \"WA2QAU\"], [\"AD4EB\", \"N4AO\"], [\"AD4EB\", \"N4AO\"], [\"AD4EB\", \"N4AO\"], [\"AD4EB\", \"N4AO\"], [\"AD4EB\", \"N4AO\"], [\"AD4EB\", \"N4AO\"], [\"AD4EB\", \"N6TQ\"], [\"AD4EB\", \"N6TQ\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"F8PDR\"], [\"AD4EB\", \"WA5DTK\"], [\"AD4EB\", \"WA5DTK\"], [\"AD4EB\", \"W5ACQ\"], [\"AD4EB\", \"W5ACQ\"], [\"AD4EB\", \"K2YG\"], [\"AD4EB\", \"K2YG\"], [\"AD4EB\", \"K2YG\"], [\"AD4EB\", \"K2YG\"], [\"AD4EB\", \"K2YG\"], [\"AD4EB\", \"K2YG\"], [\"AD4EB\", \"OM2VL\"], [\"AD4EB\", \"OM2VL\"], [\"AD4EB\", \"AA6MU\"], [\"AD4EB\", \"AA6MU\"], [\"AD4EB\", \"WU8T\"], [\"AD4EB\", \"WU8T\"], [\"AD4EB\", \"WU8T\"], [\"AD4EB\", \"WU8T\"], [\"AD4EB\", \"K5TIA\"], [\"AD4EB\", \"K5TIA\"], [\"AF5CC\", \"K5QHD\"], [\"AF5CC\", \"K5QHD\"], [\"AF5CC\", \"W5JK\"], [\"AF5CC\", \"W5JK\"], [\"AF5CC\", \"K5K\"], [\"AF5CC\", \"K5K\"], [\"AG5T\", \"N5NA\"], [\"AG5T\", \"N5NA\"], [\"AI4DB\", \"KI5GNH\"], [\"AI4DB\", \"KI5GNH\"], [\"AI6O\", \"N5JJ\"], [\"AI6O\", \"N5JJ\"], [\"AI6O\", \"N5XZ\"], [\"AI6O\", \"N5XZ\"], [\"AJ4F\", \"F8PDR\"], [\"AJ4F\", \"F8PDR\"], [\"AJ4F\", \"K0PC\"], [\"AJ4F\", \"K0PC\"], [\"AJ4F\", \"N0YL\"], [\"AJ4F\", \"N0YL\"], [\"AJ4F\", \"K1ORY\"], [\"AJ4F\", \"K1ORY\"], [\"AJ4F\", \"AA6MU\"], [\"AJ4F\", \"AA6MU\"], [\"AJ4F\", \"F8PDR\"], [\"AJ4F\", \"F8PDR\"], [\"AJ4LN\", \"K5K\"], [\"AJ4LN\", \"K5K\"], [\"AJ4LN\", \"K5K\"], [\"AJ4LN\", \"K5K\"], [\"DL3DXX\", \"K5WA\"], [\"DL3DXX\", \"K5WA\"], [\"DL3DXX\", \"K5WA\"], [\"DL3DXX\", \"K5WA\"], [\"DL3DXX\", \"W5ESE\"], [\"DL3DXX\", \"W5ESE\"], [\"DL3DXX\", \"WA5DCT\"], [\"DL3DXX\", \"WA5DCT\"], [\"DL3DXX\", \"KG5VK\"], [\"DL3DXX\", \"KG5VK\"], [\"DL3DXX\", \"K5WA\"], [\"DL3DXX\", \"K5WA\"], [\"DL3DXX\", \"K5K\"], [\"DL3DXX\", \"K5K\"], [\"DL3DXX\", \"KG5OWB\"], [\"DL3DXX\", \"KG5OWB\"], [\"DL3DXX\", \"AD4EB\"], [\"DL3DXX\", \"AD4EB\"], [\"DL3GA\", \"K5WA\"], [\"DL3GA\", \"K5WA\"], [\"DL3GA\", \"WA5DCT\"], [\"DL3GA\", \"WA5DCT\"], [\"DL5AXX\", \"K5WA\"], [\"DL5AXX\", \"K5WA\"], [\"DL5AXX\", \"W5LXS\"], [\"DL5AXX\", \"W5LXS\"], [\"DL5AXX\", \"K5WA\"], [\"DL5AXX\", \"K5WA\"], [\"DL5AXX\", \"WA5LFD\"], [\"DL5AXX\", \"WA5LFD\"], [\"DL5AXX\", \"AD4EB\"], [\"DL5AXX\", \"AD4EB\"], [\"F6JXR\", \"K5WA\"], [\"F6JXR\", \"K5WA\"], [\"F8PDR\", \"W5JK\"], [\"F8PDR\", \"W5JK\"], [\"F8PDR\", \"W5NC\"], [\"F8PDR\", \"W5NC\"], [\"F8PDR\", \"NX5M\"], [\"F8PDR\", \"NX5M\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"K5OT\"], [\"F8PDR\", \"K5OT\"], [\"F8PDR\", \"W5ACQ\"], [\"F8PDR\", \"W5ACQ\"], [\"F8PDR\", \"N5KW\"], [\"F8PDR\", \"N5KW\"], [\"F8PDR\", \"N5KW\"], [\"F8PDR\", \"N5KW\"], [\"F8PDR\", \"AJ4F\"], [\"F8PDR\", \"AJ4F\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"K5WA\"], [\"F8PDR\", \"K5WA\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"K5T\"], [\"F8PDR\", \"K5T\"], [\"F8PDR\", \"K5T\"], [\"F8PDR\", \"K5T\"], [\"F8PDR\", \"N5NA\"], [\"F8PDR\", \"N5NA\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"N5NU\"], [\"F8PDR\", \"N5NU\"], [\"F8PDR\", \"W0VX\"], [\"F8PDR\", \"W0VX\"], [\"F8PDR\", \"W5AL\"], [\"F8PDR\", \"W5AL\"], [\"F8PDR\", \"KT3X\"], [\"F8PDR\", \"KT3X\"], [\"F8PDR\", \"KT3X\"], [\"F8PDR\", \"KT3X\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"N5T\"], [\"F8PDR\", \"N5T\"], [\"F8PDR\", \"N5T\"], [\"F8PDR\", \"N5T\"], [\"F8PDR\", \"N5DN\"], [\"F8PDR\", \"N5DN\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"N5XZ\"], [\"F8PDR\", \"N5XZ\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"N5NA\"], [\"F8PDR\", \"N5NA\"], [\"F8PDR\", \"N5TJ\"], [\"F8PDR\", \"N5TJ\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"NM5M\"], [\"F8PDR\", \"NM5M\"], [\"F8PDR\", \"N5XZ\"], [\"F8PDR\", \"N5XZ\"], [\"F8PDR\", \"NX5M\"], [\"F8PDR\", \"NX5M\"], [\"F8PDR\", \"WA8ZBT\"], [\"F8PDR\", \"WA8ZBT\"], [\"F8PDR\", \"W5KU\"], [\"F8PDR\", \"W5KU\"], [\"F8PDR\", \"N5RZ\"], [\"F8PDR\", \"N5RZ\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"K5CM\"], [\"F8PDR\", \"KT3X\"], [\"F8PDR\", \"KT3X\"], [\"F8PDR\", \"KT3X\"], [\"F8PDR\", \"KT3X\"], [\"F8PDR\", \"K5T\"], [\"F8PDR\", \"K5T\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"AD4EB\"], [\"F8PDR\", \"W5JK\"], [\"F8PDR\", \"W5JK\"], [\"F8PDR\", \"KK5TY\"], [\"F8PDR\", \"KK5TY\"], [\"F8PDR\", \"AJ4F\"], [\"F8PDR\", \"AJ4F\"], [\"F8PDR\", \"NX5M\"], [\"F8PDR\", \"NX5M\"], [\"K0AD\", \"N5WBL\"], [\"K0AD\", \"N5WBL\"], [\"K0AD\", \"WA5LFD\"], [\"K0AD\", \"WA5LFD\"], [\"K0MPH\", \"K5ECT\"], [\"K0MPH\", \"K5ECT\"], [\"K0MPH\", \"K5CM\"], [\"K0MPH\", \"K5CM\"], [\"K0MPH\", \"K5CM\"], [\"K0MPH\", \"K5CM\"], [\"K0PC\", \"AD4EB\"], [\"K0PC\", \"AD4EB\"], [\"K0RC\", \"N5T\"], [\"K0RC\", \"N5T\"], [\"K0RJK\", \"W5NC\"], [\"K0RJK\", \"W5NC\"], [\"K0SV\", \"N5YA\"], [\"K0SV\", \"N5YA\"], [\"K0TQ\", \"AD4EB\"], [\"K0TQ\", \"AD4EB\"], [\"K0TRL\", \"N5NU\"], [\"K0TRL\", \"N5NU\"], [\"K0TRL\", \"K5WA\"], [\"K0TRL\", \"K5WA\"], [\"K0TRL\", \"K5EC\"], [\"K0TRL\", \"K5EC\"], [\"K0TRL\", \"K5EC\"], [\"K0TRL\", \"K5EC\"], [\"K0YY\", \"WA5DCT\"], [\"K0YY\", \"WA5DCT\"], [\"K0YY\", \"WA5DTK\"], [\"K0YY\", \"WA5DTK\"], [\"K0YY\", \"K5EC\"], [\"K0YY\", \"K5EC\"], [\"K0YY\", \"K5EC\"], [\"K0YY\", \"K5EC\"], [\"K0YY\", \"WA5JMZ\"], [\"K0YY\", \"WA5JMZ\"], [\"K0YY\", \"N5SLY\"], [\"K0YY\", \"N5SLY\"], [\"K0YY\", \"KG5IEE\"], [\"K0YY\", \"KG5IEE\"], [\"K0YY\", \"K5IZO\"], [\"K0YY\", \"K5IZO\"], [\"K1BZ\", \"N5RZ\"], [\"K1BZ\", \"N5RZ\"], [\"K1BZ\", \"KD5ZZU\"], [\"K1BZ\", \"KD5ZZU\"], [\"K1DW\", \"K5OT\"], [\"K1DW\", \"K5OT\"], [\"K1ORY\", \"N5XZ\"], [\"K1ORY\", \"N5XZ\"], [\"K1ORY\", \"N7EPD\"], [\"K1ORY\", \"N7EPD\"], [\"K1ORY\", \"K5K\"], [\"K1ORY\", \"K5K\"], [\"K1ORY\", \"KK5TY\"], [\"K1ORY\", \"KK5TY\"], [\"K1ORY\", \"N5TJ\"], [\"K1ORY\", \"N5TJ\"], [\"K1ORY\", \"K5TIA\"], [\"K1ORY\", \"K5TIA\"], [\"K1ORY\", \"KG5IEE\"], [\"K1ORY\", \"KG5IEE\"], [\"K1ORY\", \"NX5M\"], [\"K1ORY\", \"NX5M\"], [\"K1ORY\", \"W0VX\"], [\"K1ORY\", \"W0VX\"], [\"K1ORY\", \"W5KU\"], [\"K1ORY\", \"W5KU\"], [\"K1ORY\", \"N5NU\"], [\"K1ORY\", \"N5NU\"], [\"K1ORY\", \"AJ4F\"], [\"K1ORY\", \"AJ4F\"], [\"K1ORY\", \"N5RZ\"], [\"K1ORY\", \"N5RZ\"], [\"K1ORY\", \"W5ACQ\"], [\"K1ORY\", \"W5ACQ\"], [\"K1SP\", \"K2SG\"], [\"K1SP\", \"K2SG\"], [\"K1SP\", \"KI4MZC\"], [\"K1SP\", \"KI4MZC\"], [\"K2AL\", \"K5CM\"], [\"K2AL\", \"K5CM\"], [\"K2HT\", \"KT3X\"], [\"K2HT\", \"KT3X\"], [\"K2KAR\", \"W5LXS\"], [\"K2KAR\", \"W5LXS\"], [\"K2QB\", \"N5XZ\"], [\"K2QB\", \"N5XZ\"], [\"K2QB\", \"N5NA\"], [\"K2QB\", \"N5NA\"], [\"K2QB\", \"AD4EB\"], [\"K2QB\", \"AD4EB\"], [\"K2QB\", \"NM5M\"], [\"K2QB\", \"NM5M\"], [\"K2WJ\", \"K5ECT\"], [\"K2WJ\", \"K5ECT\"], [\"K2WJ\", \"K5QHD\"], [\"K2WJ\", \"K5QHD\"], [\"K2WJ\", \"W5GCX\"], [\"K2WJ\", \"W5GCX\"], [\"K2YG\", \"N5NA\"], [\"K2YG\", \"N5NA\"], [\"K2YG\", \"KG5IEE\"], [\"K2YG\", \"KG5IEE\"], [\"K2ZR\", \"N5YA\"], [\"K2ZR\", \"N5YA\"], [\"K2ZR\", \"KD5ZZU\"], [\"K2ZR\", \"KD5ZZU\"], [\"K3IE\", \"N5XZ\"], [\"K3IE\", \"N5XZ\"], [\"K3IE\", \"N5KW\"], [\"K3IE\", \"N5KW\"], [\"K3IE\", \"AD4EB\"], [\"K3IE\", \"AD4EB\"], [\"K3IE\", \"K5TIA\"], [\"K3IE\", \"K5TIA\"], [\"K3PA\", \"KK5TY\"], [\"K3PA\", \"KK5TY\"], [\"K3QP\", \"W5NC\"], [\"K3QP\", \"W5NC\"], [\"K3QP\", \"WA5DTK\"], [\"K3QP\", \"WA5DTK\"], [\"K3TD\", \"NU5DE\"], [\"K3TD\", \"NU5DE\"], [\"K3TD\", \"W5LIC\"], [\"K3TD\", \"W5LIC\"], [\"K3TD\", \"NU5M\"], [\"K3TD\", \"NU5M\"], [\"K3TD\", \"KF5VDX\"], [\"K3TD\", \"KF5VDX\"], [\"K3TD\", \"KI5GNH\"], [\"K3TD\", \"KI5GNH\"], [\"K3TW\", \"N5TTT\"], [\"K3TW\", \"N5TTT\"], [\"K3YDX\", \"W5NC\"], [\"K3YDX\", \"W5NC\"], [\"K3YDX\", \"W5ACQ\"], [\"K3YDX\", \"W5ACQ\"], [\"K3YDX\", \"NM5M\"], [\"K3YDX\", \"NM5M\"], [\"K3YDX\", \"AD4EB\"], [\"K3YDX\", \"AD4EB\"], [\"K4BAI\", \"WA5DTK\"], [\"K4BAI\", \"WA5DTK\"], [\"K4BAI\", \"AD4EB\"], [\"K4BAI\", \"AD4EB\"], [\"K4RO\", \"AD4EB\"], [\"K4RO\", \"AD4EB\"], [\"K4RO\", \"AD4EB\"], [\"K4RO\", \"AD4EB\"], [\"K4ZGB\", \"AD4EB\"], [\"K4ZGB\", \"AD4EB\"], [\"K4ZGB\", \"AD4EB\"], [\"K4ZGB\", \"AD4EB\"], [\"K4ZGB\", \"AD4EB\"], [\"K4ZGB\", \"AD4EB\"], [\"K5B\", \"K5EC\"], [\"K5B\", \"K5EC\"], [\"K5B\", \"K5EC\"], [\"K5B\", \"K5EC\"], [\"K5B\", \"WA5JMZ\"], [\"K5B\", \"WA5JMZ\"], [\"K5B\", \"WA5DTK\"], [\"K5B\", \"WA5DTK\"], [\"K5B\", \"WA5DTK\"], [\"K5B\", \"WA5DTK\"], [\"K5B\", \"OM2VL\"], [\"K5B\", \"OM2VL\"], [\"K5B\", \"OM2VL\"], [\"K5B\", \"OM2VL\"], [\"K5B\", \"W6AFA\"], [\"K5B\", \"W6AFA\"], [\"K5B\", \"K5K\"], [\"K5B\", \"K5K\"], [\"K5CM\", \"NX5M\"], [\"K5CM\", \"NX5M\"], [\"K5CM\", \"K5IZO\"], [\"K5CM\", \"K5IZO\"], [\"K5CM\", \"K5IZO\"], [\"K5CM\", \"K5IZO\"], [\"K5CM\", \"KN6VTC\"], [\"K5CM\", \"KN6VTC\"], [\"K5CM\", \"KN6VTC\"], [\"K5CM\", \"KN6VTC\"], [\"K5CM\", \"W6AFA\"], [\"K5CM\", \"W6AFA\"], [\"K5CM\", \"W6AFA\"], [\"K5CM\", \"W6AFA\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"N7EPD\"], [\"K5CM\", \"N7EPD\"], [\"K5CM\", \"N7EPD\"], [\"K5CM\", \"N7EPD\"], [\"K5CM\", \"KU8E\"], [\"K5CM\", \"KU8E\"], [\"K5CM\", \"KU8E\"], [\"K5CM\", \"KU8E\"], [\"K5CM\", \"KB4DE\"], [\"K5CM\", \"KB4DE\"], [\"K5CM\", \"KB4DE\"], [\"K5CM\", \"KB4DE\"], [\"K5CM\", \"K5YX\"], [\"K5CM\", \"K5YX\"], [\"K5CM\", \"K5YX\"], [\"K5CM\", \"K5YX\"], [\"K5CM\", \"K2AL\"], [\"K5CM\", \"K2AL\"], [\"K5CM\", \"W7GF\"], [\"K5CM\", \"W7GF\"], [\"K5CM\", \"WA2JQK\"], [\"K5CM\", \"WA2JQK\"], [\"K5CM\", \"WA2JQK\"], [\"K5CM\", \"WA2JQK\"], [\"K5CM\", \"AA3R\"], [\"K5CM\", \"AA3R\"], [\"K5CM\", \"K9OZ\"], [\"K5CM\", \"K9OZ\"], [\"K5CM\", \"N5VBP\"], [\"K5CM\", \"N5VBP\"], [\"K5CM\", \"VA3FN\"], [\"K5CM\", \"VA3FN\"], [\"K5CM\", \"VA3FN\"], [\"K5CM\", \"VA3FN\"], [\"K5CM\", \"VA3FN\"], [\"K5CM\", \"VA3FN\"], [\"K5CM\", \"SP6JOE\"], [\"K5CM\", \"SP6JOE\"], [\"K5CM\", \"N9GXA\"], [\"K5CM\", \"N9GXA\"], [\"K5CM\", \"N9GXA\"], [\"K5CM\", \"N9GXA\"], [\"K5CM\", \"NU5M\"], [\"K5CM\", \"NU5M\"], [\"K5CM\", \"N9GXA\"], [\"K5CM\", \"N9GXA\"], [\"K5CM\", \"WU8T\"], [\"K5CM\", \"WU8T\"], [\"K5CM\", \"KC0INP\"], [\"K5CM\", \"KC0INP\"], [\"K5CM\", \"KC0INP\"], [\"K5CM\", \"KC0INP\"], [\"K5CM\", \"WA5DTK\"], [\"K5CM\", \"WA5DTK\"], [\"K5CM\", \"W4YE\"], [\"K5CM\", \"W4YE\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"NA4C\"], [\"K5CM\", \"NA4C\"], [\"K5CM\", \"NX5M\"], [\"K5CM\", \"NX5M\"], [\"K5CM\", \"W5NC\"], [\"K5CM\", \"W5NC\"], [\"K5CM\", \"W5NC\"], [\"K5CM\", \"W5NC\"], [\"K5CM\", \"K5IZO\"], [\"K5CM\", \"K5IZO\"], [\"K5CM\", \"K5IZO\"], [\"K5CM\", \"K5IZO\"], [\"K5CM\", \"N5XZ\"], [\"K5CM\", \"N5XZ\"], [\"K5CM\", \"KN6VTC\"], [\"K5CM\", \"KN6VTC\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"F8PDR\"], [\"K5CM\", \"WA2JQK\"], [\"K5CM\", \"WA2JQK\"], [\"K5CM\", \"KG9X\"], [\"K5CM\", \"KG9X\"], [\"K5CM\", \"W3US\"], [\"K5CM\", \"W3US\"], [\"K5CM\", \"KF8I\"], [\"K5CM\", \"KF8I\"], [\"K5CM\", \"W4CHI\"], [\"K5CM\", \"W4CHI\"], [\"K5CM\", \"N9GXA\"], [\"K5CM\", \"N9GXA\"], [\"K5CM\", \"N7EPD\"], [\"K5CM\", \"N7EPD\"], [\"K5CM\", \"N7EPD\"], [\"K5CM\", \"N7EPD\"], [\"K5CM\", \"WB8ASI\"], [\"K5CM\", \"WB8ASI\"], [\"K5CM\", \"WN7Y\"], [\"K5CM\", \"WN7Y\"], [\"K5CM\", \"KA2KQP\"], [\"K5CM\", \"KA2KQP\"], [\"K5CM\", \"N7AME\"], [\"K5CM\", \"N7AME\"], [\"K5CM\", \"N7AME\"], [\"K5CM\", \"N7AME\"], [\"K5CM\", \"WX5LOK\"], [\"K5CM\", \"WX5LOK\"], [\"K5CM\", \"NC4FG\"], [\"K5CM\", \"NC4FG\"], [\"K5CM\", \"N7EPD\"], [\"K5CM\", \"N7EPD\"], [\"K5CM\", \"N7EPD\"], [\"K5CM\", \"N7EPD\"], [\"K5EC\", \"N5ECY\"], [\"K5EC\", \"N5ECY\"], [\"K5EC\", \"N5ECY\"], [\"K5EC\", \"N5ECY\"], [\"K5EC\", \"N5ECY\"], [\"K5EC\", \"N5ECY\"], [\"K5EC\", \"N5ECY\"], [\"K5EC\", \"N5ECY\"], [\"K5EC\", \"AA0FO\"], [\"K5EC\", \"AA0FO\"], [\"K5EC\", \"AA0FO\"], [\"K5EC\", \"AA0FO\"], [\"K5EC\", \"NE5B\"], [\"K5EC\", \"NE5B\"], [\"K5EC\", \"WA5CKF\"], [\"K5EC\", \"WA5CKF\"], [\"K5EC\", \"WA5CKF\"], [\"K5EC\", \"WA5CKF\"], [\"K5EC\", \"WA5CKF\"], [\"K5EC\", \"WA5CKF\"], [\"K5EC\", \"WA5CKF\"], [\"K5EC\", \"WA5CKF\"], [\"K5EC\", \"WJ9O\"], [\"K5EC\", \"WJ9O\"], [\"K5EC\", \"WJ9O\"], [\"K5EC\", \"WJ9O\"], [\"K5EC\", \"WJ9O\"], [\"K5EC\", \"WJ9O\"], [\"K5EC\", \"WJ9O\"], [\"K5EC\", \"WJ9O\"], [\"K5EC\", \"WA8ZBT\"], [\"K5EC\", \"WA8ZBT\"], [\"K5EC\", \"K0YY\"], [\"K5EC\", \"K0YY\"], [\"K5EC\", \"K0YY\"], [\"K5EC\", \"K0YY\"], [\"K5EC\", \"K0TRL\"], [\"K5EC\", \"K0TRL\"], [\"K5EC\", \"K0TRL\"], [\"K5EC\", \"K0TRL\"], [\"K5EC\", \"K9OZ\"], [\"K5EC\", \"K9OZ\"], [\"K5EC\", \"K9OZ\"], [\"K5EC\", \"K9OZ\"], [\"K5EC\", \"K9OZ\"], [\"K5EC\", \"K9OZ\"], [\"K5EC\", \"K9OZ\"], [\"K5EC\", \"K9OZ\"], [\"K5EC\", \"WA5DCT\"], [\"K5EC\", \"WA5DCT\"], [\"K5EC\", \"K5B\"], [\"K5EC\", \"K5B\"], [\"K5EC\", \"K5B\"], [\"K5EC\", \"K5B\"], [\"K5EC\", \"KK5TY\"], [\"K5EC\", \"KK5TY\"], [\"K5EC\", \"N5SLY\"], [\"K5EC\", \"N5SLY\"], [\"K5EC\", \"K5QHD\"], [\"K5EC\", \"K5QHD\"], [\"K5EC\", \"K5QHD\"], [\"K5EC\", \"K5QHD\"], [\"K5EC\", \"K5QHD\"], [\"K5EC\", \"K5QHD\"], [\"K5EC\", \"K5QHD\"], [\"K5EC\", \"K5QHD\"], [\"K5EC\", \"KJ5IEL\"], [\"K5EC\", \"KJ5IEL\"], [\"K5EC\", \"W8PI\"], [\"K5EC\", \"W8PI\"], [\"K5EC\", \"N5JDT\"], [\"K5EC\", \"N5JDT\"], [\"K5EC\", \"KK4JOE\"], [\"K5EC\", \"KK4JOE\"], [\"K5EC\", \"KK4JOE\"], [\"K5EC\", \"KK4JOE\"], [\"K5EC\", \"KK4JOE\"], [\"K5EC\", \"KK4JOE\"], [\"K5EC\", \"KK4JOE\"], [\"K5EC\", \"KK4JOE\"], [\"K5EC\", \"AA3R\"], [\"K5EC\", \"AA3R\"], [\"K5EC\", \"AA0AW\"], [\"K5EC\", \"AA0AW\"], [\"K5EC\", \"K8MV\"], [\"K5EC\", \"K8MV\"], [\"K5EC\", \"K8MV\"], [\"K5EC\", \"K8MV\"], [\"K5EC\", \"K8MV\"], [\"K5EC\", \"K8MV\"], [\"K5EC\", \"NQ9N\"], [\"K5EC\", \"NQ9N\"], [\"K5EC\", \"NQ9N\"], [\"K5EC\", \"NQ9N\"], [\"K5EC\", \"NQ9N\"], [\"K5EC\", \"NQ9N\"], [\"K5EC\", \"WA6KHK\"], [\"K5EC\", \"WA6KHK\"], [\"K5EC\", \"WA6KHK\"], [\"K5EC\", \"WA6KHK\"], [\"K5EC\", \"W4CHI\"], [\"K5EC\", \"W4CHI\"], [\"K5EC\", \"W4CHI\"], [\"K5EC\", \"W4CHI\"], [\"K5EC\", \"N5WRX\"], [\"K5EC\", \"N5WRX\"], [\"K5ECT\", \"K9ECT\"], [\"K5ECT\", \"K9ECT\"], [\"K5ECT\", \"W6AFA\"], [\"K5ECT\", \"W6AFA\"], [\"K5ECT\", \"WA4JA\"], [\"K5ECT\", \"WA4JA\"], [\"K5ECT\", \"KA3EHL\"], [\"K5ECT\", \"KA3EHL\"], [\"K5ECT\", \"WB9HFK\"], [\"K5ECT\", \"WB9HFK\"], [\"K5GAL\", \"KI5NCJ\"], [\"K5GAL\", \"KI5NCJ\"], [\"K5GAL\", \"W5LIC\"], [\"K5GAL\", \"W5LIC\"], [\"K5IZO\", \"N5AW\"], [\"K5IZO\", \"N5AW\"], [\"K5IZO\", \"KG5OWB\"], [\"K5IZO\", \"KG5OWB\"], [\"K5IZO\", \"W5GCX\"], [\"K5IZO\", \"W5GCX\"], [\"K5IZO\", \"K0YY\"], [\"K5IZO\", \"K0YY\"], [\"K5K\", \"AA3R\"], [\"K5K\", \"AA3R\"], [\"K5K\", \"AA3R\"], [\"K5K\", \"AA3R\"], [\"K5K\", \"N6OKU\"], [\"K5K\", \"N6OKU\"], [\"K5K\", \"N6OKU\"], [\"K5K\", \"N6OKU\"], [\"K5K\", \"K1ORY\"], [\"K5K\", \"K1ORY\"], [\"K5K\", \"K1ORY\"], [\"K5K\", \"K1ORY\"], [\"K5K\", \"N5WBL\"], [\"K5K\", \"N5WBL\"], [\"K5K\", \"N5WBL\"], [\"K5K\", \"N5WBL\"], [\"K5K\", \"N5VBL\"], [\"K5K\", \"N5VBL\"], [\"K5K\", \"KB4CG\"], [\"K5K\", \"KB4CG\"], [\"K5K\", \"KB4CG\"], [\"K5K\", \"KB4CG\"], [\"K5K\", \"KC4EEL\"], [\"K5K\", \"KC4EEL\"], [\"K5K\", \"KC4EEL\"], [\"K5K\", \"KC4EEL\"], [\"K5K\", \"KC3M\"], [\"K5K\", \"KC3M\"], [\"K5K\", \"KC3M\"], [\"K5K\", \"KC3M\"], [\"K5K\", \"N6DW\"], [\"K5K\", \"N6DW\"], [\"K5K\", \"KC4EEL\"], [\"K5K\", \"KC4EEL\"], [\"K5K\", \"KC4EEL\"], [\"K5K\", \"KC4EEL\"], [\"K5K\", \"N5WCT\"], [\"K5K\", \"N5WCT\"], [\"K5K\", \"AF5CC\"], [\"K5K\", \"AF5CC\"], [\"K5K\", \"N0IIL\"], [\"K5K\", \"N0IIL\"], [\"K5K\", \"K5B\"], [\"K5K\", \"K5B\"], [\"K5LGX\", \"VE9CF\"], [\"K5LGX\", \"VE9CF\"], [\"K5MAY\", \"KI5NCJ\"], [\"K5MAY\", \"KI5NCJ\"], [\"K5MAY\", \"N5JJ\"], [\"K5MAY\", \"N5JJ\"], [\"K5OT\", \"K1DW\"], [\"K5OT\", \"K1DW\"], [\"K5OT\", \"KR7D\"], [\"K5OT\", \"KR7D\"], [\"K5OT\", \"N8DNA\"], [\"K5OT\", \"N8DNA\"], [\"K5OT\", \"F8PDR\"], [\"K5OT\", \"F8PDR\"], [\"K5OT\", \"AF5CC\"], [\"K5OT\", \"AF5CC\"], [\"K5OT\", \"N6DW\"], [\"K5OT\", \"N6DW\"], [\"K5QHD\", \"N5IT\"], [\"K5QHD\", \"N5IT\"], [\"K5QHD\", \"NE5B\"], [\"K5QHD\", \"NE5B\"], [\"K5QHD\", \"KS4X\"], [\"K5QHD\", \"KS4X\"], [\"K5QHD\", \"NX5M\"], [\"K5QHD\", \"NX5M\"], [\"K5QHD\", \"WA4GMW\"], [\"K5QHD\", \"WA4GMW\"], [\"K5QHD\", \"AJ4HP\"], [\"K5QHD\", \"AJ4HP\"], [\"K5QHD\", \"WO4O\"], [\"K5QHD\", \"WO4O\"], [\"K5QHD\", \"WB9HFK\"], [\"K5QHD\", \"WB9HFK\"], [\"K5QHD\", \"NE8P\"], [\"K5QHD\", \"NE8P\"], [\"K5QHD\", \"NU5M\"], [\"K5QHD\", \"NU5M\"], [\"K5QHD\", \"WA5DCT\"], [\"K5QHD\", \"WA5DCT\"], [\"K5QHD\", \"NV4T\"], [\"K5QHD\", \"NV4T\"], [\"K5QHD\", \"N5WCT\"], [\"K5QHD\", \"N5WCT\"], [\"K5QHD\", \"WA5JMZ\"], [\"K5QHD\", \"WA5JMZ\"], [\"K5QHD\", \"KF5VDX\"], [\"K5QHD\", \"KF5VDX\"], [\"K5QHD\", \"N5YA\"], [\"K5QHD\", \"N5YA\"], [\"K5QHD\", \"K5EC\"], [\"K5QHD\", \"K5EC\"], [\"K5QHD\", \"K5EC\"], [\"K5QHD\", \"K5EC\"], [\"K5QHD\", \"K5EC\"], [\"K5QHD\", \"K5EC\"], [\"K5QHD\", \"K5EC\"], [\"K5QHD\", \"K5EC\"], [\"K5QHD\", \"KK5TY\"], [\"K5QHD\", \"KK5TY\"], [\"K5QHD\", \"NU5DE\"], [\"K5QHD\", \"NU5DE\"], [\"K5QHD\", \"W5LIC\"], [\"K5QHD\", \"W5LIC\"], [\"K5QHD\", \"K2WJ\"], [\"K5QHD\", \"K2WJ\"], [\"K5QQ\", \"W5ESE\"], [\"K5QQ\", \"W5ESE\"], [\"K5QQ\", \"K5IZO\"], [\"K5QQ\", \"K5IZO\"], [\"K5QQ\", \"AD4EB\"], [\"K5QQ\", \"AD4EB\"], [\"K5QQ\", \"KG5VK\"], [\"K5QQ\", \"KG5VK\"], [\"K5RJM\", \"N5WRX\"], [\"K5RJM\", \"N5WRX\"], [\"K5T\", \"WA5DTK\"], [\"K5T\", \"WA5DTK\"], [\"K5T\", \"WA5DTK\"], [\"K5T\", \"WA5DTK\"], [\"K5T\", \"W5AL\"], [\"K5T\", \"W5AL\"], [\"K5T\", \"N5NA\"], [\"K5T\", \"N5NA\"], [\"K5T\", \"KB0NES\"], [\"K5T\", \"KB0NES\"], [\"K5T\", \"KB0NES\"], [\"K5T\", \"KB0NES\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"K5IZO\"], [\"K5T\", \"K5IZO\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"W4YE\"], [\"K5T\", \"W4YE\"], [\"K5T\", \"W4YE\"], [\"K5T\", \"W4YE\"], [\"K5T\", \"W5JK\"], [\"K5T\", \"W5JK\"], [\"K5T\", \"W5JK\"], [\"K5T\", \"W5JK\"], [\"K5T\", \"F8PDR\"], [\"K5T\", \"F8PDR\"], [\"K5T\", \"F8PDR\"], [\"K5T\", \"F8PDR\"], [\"K5T\", \"N5YA\"], [\"K5T\", \"N5YA\"], [\"K5T\", \"N5JJ\"], [\"K5T\", \"N5JJ\"], [\"K5T\", \"N5JJ\"], [\"K5T\", \"N5JJ\"], [\"K5T\", \"N6DW\"], [\"K5T\", \"N6DW\"], [\"K5T\", \"N9GXA\"], [\"K5T\", \"N9GXA\"], [\"K5T\", \"WA5LFD\"], [\"K5T\", \"WA5LFD\"], [\"K5T\", \"NA4J\"], [\"K5T\", \"NA4J\"], [\"K5T\", \"K5TIA\"], [\"K5T\", \"K5TIA\"], [\"K5T\", \"K5TIA\"], [\"K5T\", \"K5TIA\"], [\"K5T\", \"WA5DTK\"], [\"K5T\", \"WA5DTK\"], [\"K5T\", \"K5K\"], [\"K5T\", \"K5K\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"NX5M\"], [\"K5T\", \"NX5M\"], [\"K5T\", \"KG5VK\"], [\"K5T\", \"KG5VK\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"ND0C\"], [\"K5T\", \"AA3R\"], [\"K5T\", \"AA3R\"], [\"K5T\", \"F8PDR\"], [\"K5T\", \"F8PDR\"], [\"K5TIA\", \"KI4MZC\"], [\"K5TIA\", \"KI4MZC\"], [\"K5TIA\", \"NX5M\"], [\"K5TIA\", \"NX5M\"], [\"K5TIA\", \"KJ9C\"], [\"K5TIA\", \"KJ9C\"], [\"K5TIA\", \"W5GCX\"], [\"K5TIA\", \"W5GCX\"], [\"K5TIA\", \"K1ORY\"], [\"K5TIA\", \"K1ORY\"], [\"K5TIA\", \"K5T\"], [\"K5TIA\", \"K5T\"], [\"K5TIA\", \"K5T\"], [\"K5TIA\", \"K5T\"], [\"K5TU\", \"K8MV\"], [\"K5TU\", \"K8MV\"], [\"K5UBE\", \"N5IT\"], [\"K5UBE\", \"N5IT\"], [\"K5UBE\", \"KF5VDX\"], [\"K5UBE\", \"KF5VDX\"], [\"K5WA\", \"DL3DXX\"], [\"K5WA\", \"DL3DXX\"], [\"K5WA\", \"OM2VL\"], [\"K5WA\", \"OM2VL\"], [\"K5WA\", \"DL3DXX\"], [\"K5WA\", \"DL3DXX\"], [\"K5WA\", \"OM2VL\"], [\"K5WA\", \"OM2VL\"], [\"K5WA\", \"DL5AXX\"], [\"K5WA\", \"DL5AXX\"], [\"K5WA\", \"SP6JOE\"], [\"K5WA\", \"SP6JOE\"], [\"K5WA\", \"VE3DQN\"], [\"K5WA\", \"VE3DQN\"], [\"K5WA\", \"F8PDR\"], [\"K5WA\", \"F8PDR\"], [\"K5WA\", \"DL3GA\"], [\"K5WA\", \"DL3GA\"], [\"K5WA\", \"SP6JOE\"], [\"K5WA\", \"SP6JOE\"], [\"K5WA\", \"DL5AXX\"], [\"K5WA\", \"DL5AXX\"], [\"K5WA\", \"NX5M\"], [\"K5WA\", \"NX5M\"], [\"K5WA\", \"W5GCX\"], [\"K5WA\", \"W5GCX\"], [\"K5WA\", \"F6JXR\"], [\"K5WA\", \"F6JXR\"], [\"K5WA\", \"DL3DXX\"], [\"K5WA\", \"DL3DXX\"], [\"K5WA\", \"OM2VL\"], [\"K5WA\", \"OM2VL\"], [\"K5WA\", \"N5DTT\"], [\"K5WA\", \"N5DTT\"], [\"K5WW\", \"NX5M\"], [\"K5WW\", \"NX5M\"], [\"K5YX\", \"AD4EB\"], [\"K5YX\", \"AD4EB\"], [\"K5YX\", \"KE5OBS\"], [\"K5YX\", \"KE5OBS\"], [\"K5YX\", \"K0PC\"], [\"K5YX\", \"K0PC\"], [\"K5YX\", \"KJ5IEL\"], [\"K5YX\", \"KJ5IEL\"], [\"K5ZD\", \"W5JK\"], [\"K5ZD\", \"W5JK\"], [\"K7GM\", \"K5TIA\"], [\"K7GM\", \"K5TIA\"], [\"K8MFO\", \"WB5BKL\"], [\"K8MFO\", \"WB5BKL\"], [\"K8MV\", \"W5LXS\"], [\"K8MV\", \"W5LXS\"], [\"K8MV\", \"AD4EB\"], [\"K8MV\", \"AD4EB\"], [\"K8MV\", \"KJ5IEL\"], [\"K8MV\", \"KJ5IEL\"], [\"K8MV\", \"NU5DE\"], [\"K8MV\", \"NU5DE\"], [\"K8MV\", \"N5YA\"], [\"K8MV\", \"N5YA\"], [\"K8MV\", \"K5TU\"], [\"K8MV\", \"K5TU\"], [\"K8MV\", \"W5JK\"], [\"K8MV\", \"W5JK\"], [\"K8MV\", \"W5HI\"], [\"K8MV\", \"W5HI\"], [\"K8MV\", \"KT3X\"], [\"K8MV\", \"KT3X\"], [\"K9CW\", \"K5K\"], [\"K9CW\", \"K5K\"], [\"K9ECT\", \"K5ECT\"], [\"K9ECT\", \"K5ECT\"], [\"K9JK\", \"AD4EB\"], [\"K9JK\", \"AD4EB\"], [\"K9OZ\", \"K5WA\"], [\"K9OZ\", \"K5WA\"], [\"K9OZ\", \"K5EC\"], [\"K9OZ\", \"K5EC\"], [\"K9OZ\", \"K5EC\"], [\"K9OZ\", \"K5EC\"], [\"K9OZ\", \"K5EC\"], [\"K9OZ\", \"K5EC\"], [\"K9OZ\", \"K5CM\"], [\"K9OZ\", \"K5CM\"], [\"KA0PQW\", \"N5AW\"], [\"KA0PQW\", \"N5AW\"], [\"KA0PQW\", \"W5NC\"], [\"KA0PQW\", \"W5NC\"], [\"KA0PQW\", \"AD4EB\"], [\"KA0PQW\", \"AD4EB\"], [\"KA0PQW\", \"AD4EB\"], [\"KA0PQW\", \"AD4EB\"], [\"KA0PQW\", \"AD4EB\"], [\"KA0PQW\", \"AD4EB\"], [\"KA0PQW\", \"KG5OWB\"], [\"KA0PQW\", \"KG5OWB\"], [\"KA0PQW\", \"AD4EB\"], [\"KA0PQW\", \"AD4EB\"], [\"KA2KQP\", \"N5XZ\"], [\"KA2KQP\", \"N5XZ\"], [\"KA2KQP\", \"K5K\"], [\"KA2KQP\", \"K5K\"], [\"KA2KQP\", \"K5K\"], [\"KA2KQP\", \"K5K\"], [\"KA2KQP\", \"W5AL\"], [\"KA2KQP\", \"W5AL\"], [\"KA2KQP\", \"N5YA\"], [\"KA2KQP\", \"N5YA\"], [\"KA2KQP\", \"KK5TY\"], [\"KA2KQP\", \"KK5TY\"], [\"KA2KQP\", \"K5CM\"], [\"KA2KQP\", \"K5CM\"], [\"KA3EHL\", \"K5ECT\"], [\"KA3EHL\", \"K5ECT\"], [\"KA6BIM\", \"KG5VK\"], [\"KA6BIM\", \"KG5VK\"], [\"KA6BIM\", \"KT3X\"], [\"KA6BIM\", \"KT3X\"], [\"KA6BIM\", \"KT3X\"], [\"KA6BIM\", \"KT3X\"], [\"KA6BIM\", \"KT3X\"], [\"KA6BIM\", \"KT3X\"], [\"KB0NES\", \"K5T\"], [\"KB0NES\", \"K5T\"], [\"KB0NES\", \"K5T\"], [\"KB0NES\", \"K5T\"], [\"KB0NES\", \"K5B\"], [\"KB0NES\", \"K5B\"], [\"KB0NES\", \"K5B\"], [\"KB0NES\", \"K5B\"], [\"KB4CG\", \"N5KW\"], [\"KB4CG\", \"N5KW\"], [\"KB4CG\", \"WA5DCT\"], [\"KB4CG\", \"WA5DCT\"], [\"KB4DE\", \"K5TIA\"], [\"KB4DE\", \"K5TIA\"], [\"KB4DE\", \"N5XZ\"], [\"KB4DE\", \"N5XZ\"], [\"KB5A\", \"NZ5X\"], [\"KB5A\", \"NZ5X\"], [\"KB9LGS\", \"KC6UCN\"], [\"KB9LGS\", \"KC6UCN\"], [\"KC0INP\", \"WA5DCT\"], [\"KC0INP\", \"WA5DCT\"], [\"KC3M\", \"KK5TY\"], [\"KC3M\", \"KK5TY\"], [\"KC3M\", \"KT3X\"], [\"KC3M\", \"KT3X\"], [\"KC3M\", \"KT3X\"], [\"KC3M\", \"KT3X\"], [\"KC3M\", \"K5K\"], [\"KC3M\", \"K5K\"], [\"KC3M\", \"K5K\"], [\"KC3M\", \"K5K\"], [\"KC4EEL\", \"VA4JS\"], [\"KC4EEL\", \"VA4JS\"], [\"KC4EEL\", \"VA4JS\"], [\"KC4EEL\", \"VA4JS\"], [\"KC4EEL\", \"K4IEW\"], [\"KC4EEL\", \"K4IEW\"], [\"KC6UCN\", \"VA4JS\"], [\"KC6UCN\", \"VA4JS\"], [\"KC6UCN\", \"VE9CF\"], [\"KC6UCN\", \"VE9CF\"], [\"KC6UCN\", \"NX5M\"], [\"KC6UCN\", \"NX5M\"], [\"KC7V\", \"AD4EB\"], [\"KC7V\", \"AD4EB\"], [\"KD4S\", \"K5T\"], [\"KD4S\", \"K5T\"], [\"KD4S\", \"K5T\"], [\"KD4S\", \"K5T\"], [\"KD5ZZU\", \"NR0P\"], [\"KD5ZZU\", \"NR0P\"], [\"KD5ZZU\", \"KA0PQW\"], [\"KD5ZZU\", \"KA0PQW\"], [\"KD5ZZU\", \"N5XZ\"], [\"KD5ZZU\", \"N5XZ\"], [\"KD5ZZU\", \"K2ZR\"], [\"KD5ZZU\", \"K2ZR\"], [\"KD5ZZU\", \"NU5DE\"], [\"KD5ZZU\", \"NU5DE\"], [\"KD5ZZU\", \"K1BZ\"], [\"KD5ZZU\", \"K1BZ\"], [\"KD5ZZU\", \"AA3R\"], [\"KD5ZZU\", \"AA3R\"], [\"KD5ZZU\", \"WU8T\"], [\"KD5ZZU\", \"WU8T\"], [\"KD9NZB\", \"AD4EB\"], [\"KD9NZB\", \"AD4EB\"], [\"KD9NZB\", \"AD4EB\"], [\"KD9NZB\", \"AD4EB\"], [\"KD9NZB\", \"K5WA\"], [\"KD9NZB\", \"K5WA\"], [\"KD9NZB\", \"AJ4F\"], [\"KD9NZB\", \"AJ4F\"], [\"KD9NZB\", \"K5T\"], [\"KD9NZB\", \"K5T\"], [\"KD9NZB\", \"K5K\"], [\"KD9NZB\", \"K5K\"], [\"KE0TT\", \"W5AL\"], [\"KE0TT\", \"W5AL\"], [\"KE0TT\", \"AD4EB\"], [\"KE0TT\", \"AD4EB\"], [\"KE3LA\", \"KK5TY\"], [\"KE3LA\", \"KK5TY\"], [\"KE3V\", \"W5LXS\"], [\"KE3V\", \"W5LXS\"], [\"KE4Q\", \"AD4EB\"], [\"KE4Q\", \"AD4EB\"], [\"KE4Q\", \"AD4EB\"], [\"KE4Q\", \"AD4EB\"], [\"KE4Q\", \"KG5VK\"], [\"KE4Q\", \"KG5VK\"], [\"KE5OBS\", \"WA5CKF\"], [\"KE5OBS\", \"WA5CKF\"], [\"KE5OBS\", \"WA5CKF\"], [\"KE5OBS\", \"WA5CKF\"], [\"KE5OBS\", \"K0TRL\"], [\"KE5OBS\", \"K0TRL\"], [\"KE5OBS\", \"W5NC\"], [\"KE5OBS\", \"W5NC\"], [\"KE5OBS\", \"N5WCT\"], [\"KE5OBS\", \"N5WCT\"], [\"KE5OBS\", \"KC4EEL\"], [\"KE5OBS\", \"KC4EEL\"], [\"KE5OBS\", \"KC4EEL\"], [\"KE5OBS\", \"KC4EEL\"], [\"KE5OBS\", \"OM2VL\"], [\"KE5OBS\", \"OM2VL\"], [\"KE5OBS\", \"OM2VL\"], [\"KE5OBS\", \"OM2VL\"], [\"KE5OBS\", \"KI5NCJ\"], [\"KE5OBS\", \"KI5NCJ\"], [\"KF5RUW\", \"K5RJM\"], [\"KF5RUW\", \"K5RJM\"], [\"KF5VDX\", \"K5QHD\"], [\"KF5VDX\", \"K5QHD\"], [\"KF5VDX\", \"KB3UJT\"], [\"KF5VDX\", \"KB3UJT\"], [\"KF5VDX\", \"K3TD\"], [\"KF5VDX\", \"K3TD\"], [\"KF5VDX\", \"K5UBE\"], [\"KF5VDX\", \"K5UBE\"], [\"KF5YUB\", \"VE9CF\"], [\"KF5YUB\", \"VE9CF\"], [\"KF5YUB\", \"KZ3P\"], [\"KF5YUB\", \"KZ3P\"], [\"KF5YUB\", \"VE7SCC\"], [\"KF5YUB\", \"VE7SCC\"], [\"KF5YUB\", \"VE3YT\"], [\"KF5YUB\", \"VE3YT\"], [\"KF8I\", \"K5CM\"], [\"KF8I\", \"K5CM\"], [\"KG5IEE\", \"K0YY\"], [\"KG5IEE\", \"K0YY\"], [\"KG5IEE\", \"AD4EB\"], [\"KG5IEE\", \"AD4EB\"], [\"KG5IEE\", \"N5VBP\"], [\"KG5IEE\", \"N5VBP\"], [\"KG5IEE\", \"W5GCX\"], [\"KG5IEE\", \"W5GCX\"], [\"KG5IEE\", \"K1ORY\"], [\"KG5IEE\", \"K1ORY\"], [\"KG5IEE\", \"AG5T\"], [\"KG5IEE\", \"AG5T\"], [\"KG5LJZ\", \"W5LIC\"], [\"KG5LJZ\", \"W5LIC\"], [\"KG5LJZ\", \"KN6VTC\"], [\"KG5LJZ\", \"KN6VTC\"], [\"KG5LJZ\", \"ND0C\"], [\"KG5LJZ\", \"ND0C\"], [\"KG5LJZ\", \"NE8P\"], [\"KG5LJZ\", \"NE8P\"], [\"KG5LJZ\", \"NQ9N\"], [\"KG5LJZ\", \"NQ9N\"], [\"KG5OWB\", \"W5ACQ\"], [\"KG5OWB\", \"W5ACQ\"], [\"KG5OWB\", \"N5TJ\"], [\"KG5OWB\", \"N5TJ\"], [\"KG5OWB\", \"W5NC\"], [\"KG5OWB\", \"W5NC\"], [\"KG5OWB\", \"AD4EB\"], [\"KG5OWB\", \"AD4EB\"], [\"KG5OWB\", \"W5GCX\"], [\"KG5OWB\", \"W5GCX\"], [\"KG5OWB\", \"VE2FK\"], [\"KG5OWB\", \"VE2FK\"], [\"KG5OWB\", \"N6AR\"], [\"KG5OWB\", \"N6AR\"], [\"KG5OWB\", \"SP6JOE\"], [\"KG5OWB\", \"SP6JOE\"], [\"KG5OWB\", \"KA0PQW\"], [\"KG5OWB\", \"KA0PQW\"], [\"KG5SQJ\", \"WJ9O\"], [\"KG5SQJ\", \"WJ9O\"], [\"KG5SQJ\", \"KJ5MA\"], [\"KG5SQJ\", \"KJ5MA\"], [\"KG5SQJ\", \"N5SLY\"], [\"KG5SQJ\", \"N5SLY\"], [\"KG5SQJ\", \"N5DTT\"], [\"KG5SQJ\", \"N5DTT\"], [\"KG5SQJ\", \"K5QHD\"], [\"KG5SQJ\", \"K5QHD\"], [\"KG5SQJ\", \"K5GAL\"], [\"KG5SQJ\", \"K5GAL\"], [\"KG5SQJ\", \"NZ5X\"], [\"KG5SQJ\", \"NZ5X\"], [\"KG5SQJ\", \"K5MAY\"], [\"KG5SQJ\", \"K5MAY\"], [\"KG5SQJ\", \"WA8ZBT\"], [\"KG5SQJ\", \"WA8ZBT\"], [\"KG5SQJ\", \"NC5T\"], [\"KG5SQJ\", \"NC5T\"], [\"KG5SQJ\", \"NE5B\"], [\"KG5SQJ\", \"NE5B\"], [\"KG5SQJ\", \"NU5DE\"], [\"KG5SQJ\", \"NU5DE\"], [\"KG5SQJ\", \"N5WRX\"], [\"KG5SQJ\", \"N5WRX\"], [\"KG5SQJ\", \"N5ECY\"], [\"KG5SQJ\", \"N5ECY\"], [\"KG5SQJ\", \"NW5Q\"], [\"KG5SQJ\", \"NW5Q\"], [\"KG5SQJ\", \"WA5CKF\"], [\"KG5SQJ\", \"WA5CKF\"], [\"KG5SQJ\", \"W5LIC\"], [\"KG5SQJ\", \"W5LIC\"], [\"KG5SQJ\", \"WA5DTK\"], [\"KG5SQJ\", \"WA5DTK\"], [\"KG5SQJ\", \"AI5OL\"], [\"KG5SQJ\", \"AI5OL\"], [\"KG5SQJ\", \"K5YX\"], [\"KG5SQJ\", \"K5YX\"], [\"KG5SQJ\", \"N5IT\"], [\"KG5SQJ\", \"N5IT\"], [\"KG5SQJ\", \"KF5RUW\"], [\"KG5SQJ\", \"KF5RUW\"], [\"KG5SQJ\", \"K5K\"], [\"KG5SQJ\", \"K5K\"], [\"KG5SQJ\", \"K5K\"], [\"KG5SQJ\", \"K5K\"], [\"KG5SQJ\", \"N0YL\"], [\"KG5SQJ\", \"N0YL\"], [\"KG5SQJ\", \"KE5OBS\"], [\"KG5SQJ\", \"KE5OBS\"], [\"KG5SQJ\", \"KE5OBS\"], [\"KG5SQJ\", \"KE5OBS\"], [\"KG5SQJ\", \"NU5M\"], [\"KG5SQJ\", \"NU5M\"], [\"KG5SQJ\", \"K2WJ\"], [\"KG5SQJ\", \"K2WJ\"], [\"KG5SQJ\", \"W5JCC\"], [\"KG5SQJ\", \"W5JCC\"], [\"KG5SQJ\", \"N5DN\"], [\"KG5SQJ\", \"N5DN\"], [\"KG5SQJ\", \"K5HRB\"], [\"KG5SQJ\", \"K5HRB\"], [\"KG5SQJ\", \"K5B\"], [\"KG5SQJ\", \"K5B\"], [\"KG5SQJ\", \"K5B\"], [\"KG5SQJ\", \"K5B\"], [\"KG5SQJ\", \"KF5VDX\"], [\"KG5SQJ\", \"KF5VDX\"], [\"KG5SQJ\", \"W5GCX\"], [\"KG5SQJ\", \"W5GCX\"], [\"KG5SQJ\", \"KB9LGS\"], [\"KG5SQJ\", \"KB9LGS\"], [\"KG5SQJ\", \"N5VBP\"], [\"KG5SQJ\", \"N5VBP\"], [\"KG5SQJ\", \"NX5M\"], [\"KG5SQJ\", \"NX5M\"], [\"KG5SQJ\", \"W5HI\"], [\"KG5SQJ\", \"W5HI\"], [\"KG5SQJ\", \"N5J\"], [\"KG5SQJ\", \"N5J\"], [\"KG5SQJ\", \"K5ECT\"], [\"KG5SQJ\", \"K5ECT\"], [\"KG5SQJ\", \"N5WCT\"], [\"KG5SQJ\", \"N5WCT\"], [\"KG5SQJ\", \"WW5L\"], [\"KG5SQJ\", \"WW5L\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"KM5Z\"], [\"KG5SQJ\", \"KM5Z\"], [\"KG5SQJ\", \"W5ESE\"], [\"KG5SQJ\", \"W5ESE\"], [\"KG5SQJ\", \"W5NC\"], [\"KG5SQJ\", \"W5NC\"], [\"KG5SQJ\", \"N5WBL\"], [\"KG5SQJ\", \"N5WBL\"], [\"KG5SQJ\", \"NR0P\"], [\"KG5SQJ\", \"NR0P\"], [\"KG5SQJ\", \"W5LO\"], [\"KG5SQJ\", \"W5LO\"], [\"KG5SQJ\", \"AG5T\"], [\"KG5SQJ\", \"AG5T\"], [\"KG5SQJ\", \"KB5A\"], [\"KG5SQJ\", \"KB5A\"], [\"KG5SQJ\", \"KJ5BUE\"], [\"KG5SQJ\", \"KJ5BUE\"], [\"KG5SQJ\", \"AF5CC\"], [\"KG5SQJ\", \"AF5CC\"], [\"KG5SQJ\", \"N5YA\"], [\"KG5SQJ\", \"N5YA\"], [\"KG5SQJ\", \"KJ5KMB\"], [\"KG5SQJ\", \"KJ5KMB\"], [\"KG5SQJ\", \"N5SLY\"], [\"KG5SQJ\", \"N5SLY\"], [\"KG5SQJ\", \"WA5JMZ\"], [\"KG5SQJ\", \"WA5JMZ\"], [\"KG5SQJ\", \"K0YY\"], [\"KG5SQJ\", \"K0YY\"], [\"KG5SQJ\", \"N0LMQ\"], [\"KG5SQJ\", \"N0LMQ\"], [\"KG5SQJ\", \"KI5NCJ\"], [\"KG5SQJ\", \"KI5NCJ\"], [\"KG5SQJ\", \"K4BAI\"], [\"KG5SQJ\", \"K4BAI\"], [\"KG5SQJ\", \"K3TD\"], [\"KG5SQJ\", \"K3TD\"], [\"KG5SQJ\", \"VA4JS\"], [\"KG5SQJ\", \"VA4JS\"], [\"KG5SQJ\", \"N7IR\"], [\"KG5SQJ\", \"N7IR\"], [\"KG5SQJ\", \"K9JK\"], [\"KG5SQJ\", \"K9JK\"], [\"KG5SQJ\", \"K4MMW\"], [\"KG5SQJ\", \"K4MMW\"], [\"KG5SQJ\", \"W6ECK\"], [\"KG5SQJ\", \"W6ECK\"], [\"KG5SQJ\", \"AJ4LN\"], [\"KG5SQJ\", \"AJ4LN\"], [\"KG5SQJ\", \"WO4O\"], [\"KG5SQJ\", \"WO4O\"], [\"KG5SQJ\", \"NE8P\"], [\"KG5SQJ\", \"NE8P\"], [\"KG5SQJ\", \"AA3R\"], [\"KG5SQJ\", \"AA3R\"], [\"KG5SQJ\", \"WA2JQK\"], [\"KG5SQJ\", \"WA2JQK\"], [\"KG5SQJ\", \"ND0C\"], [\"KG5SQJ\", \"ND0C\"], [\"KG5SQJ\", \"NC4FG\"], [\"KG5SQJ\", \"NC4FG\"], [\"KG5SQJ\", \"K1HG\"], [\"KG5SQJ\", \"K1HG\"], [\"KG5SQJ\", \"AI5OL\"], [\"KG5SQJ\", \"AI5OL\"], [\"KG5SQJ\", \"KC0INP\"], [\"KG5SQJ\", \"KC0INP\"], [\"KG5SQJ\", \"N8II\"], [\"KG5SQJ\", \"N8II\"], [\"KG5SQJ\", \"W0UC\"], [\"KG5SQJ\", \"W0UC\"], [\"KG5SQJ\", \"W6AFA\"], [\"KG5SQJ\", \"W6AFA\"], [\"KG5SQJ\", \"KD9KEQ\"], [\"KG5SQJ\", \"KD9KEQ\"], [\"KG5SQJ\", \"KC1QEM\"], [\"KG5SQJ\", \"KC1QEM\"], [\"KG5SQJ\", \"KB9LGS\"], [\"KG5SQJ\", \"KB9LGS\"], [\"KG5SQJ\", \"KZ3P\"], [\"KG5SQJ\", \"KZ3P\"], [\"KG5SQJ\", \"K5ZD\"], [\"KG5SQJ\", \"K5ZD\"], [\"KG5SQJ\", \"NV4T\"], [\"KG5SQJ\", \"NV4T\"], [\"KG5SQJ\", \"WA6KHK\"], [\"KG5SQJ\", \"WA6KHK\"], [\"KG5SQJ\", \"WX5LOK\"], [\"KG5SQJ\", \"WX5LOK\"], [\"KG5SQJ\", \"N1LN\"], [\"KG5SQJ\", \"N1LN\"], [\"KG5SQJ\", \"W2TB\"], [\"KG5SQJ\", \"W2TB\"], [\"KG5SQJ\", \"WA2QAU\"], [\"KG5SQJ\", \"WA2QAU\"], [\"KG5SQJ\", \"W8PI\"], [\"KG5SQJ\", \"W8PI\"], [\"KG5SQJ\", \"KA6BIM\"], [\"KG5SQJ\", \"KA6BIM\"], [\"KG5SQJ\", \"KJ9B\"], [\"KG5SQJ\", \"KJ9B\"], [\"KG5SQJ\", \"K3YDX\"], [\"KG5SQJ\", \"K3YDX\"], [\"KG5SQJ\", \"KF8I\"], [\"KG5SQJ\", \"KF8I\"], [\"KG5SQJ\", \"KN6VTC\"], [\"KG5SQJ\", \"KN6VTC\"], [\"KG5SQJ\", \"W0PI\"], [\"KG5SQJ\", \"W0PI\"], [\"KG5SQJ\", \"AA0AW\"], [\"KG5SQJ\", \"AA0AW\"], [\"KG5SQJ\", \"VE3YT\"], [\"KG5SQJ\", \"VE3YT\"], [\"KG5SQJ\", \"OM2VL\"], [\"KG5SQJ\", \"OM2VL\"], [\"KG5SQJ\", \"K2SG\"], [\"KG5SQJ\", \"K2SG\"], [\"KG5SQJ\", \"WA1SAY\"], [\"KG5SQJ\", \"WA1SAY\"], [\"KG5SQJ\", \"N1ADX\"], [\"KG5SQJ\", \"N1ADX\"], [\"KG5SQJ\", \"K3TW\"], [\"KG5SQJ\", \"K3TW\"], [\"KG5SQJ\", \"KB0XY\"], [\"KG5SQJ\", \"KB0XY\"], [\"KG5SQJ\", \"W0PMO\"], [\"KG5SQJ\", \"W0PMO\"], [\"KG5SQJ\", \"KN6VTC\"], [\"KG5SQJ\", \"KN6VTC\"], [\"KG5SQJ\", \"N6TQ\"], [\"KG5SQJ\", \"N6TQ\"], [\"KG5SQJ\", \"N1ADX\"], [\"KG5SQJ\", \"N1ADX\"], [\"KG5SQJ\", \"K0SV\"], [\"KG5SQJ\", \"K0SV\"], [\"KG5SQJ\", \"N6AR\"], [\"KG5SQJ\", \"N6AR\"], [\"KG5SQJ\", \"N9TXN\"], [\"KG5SQJ\", \"N9TXN\"], [\"KG5SQJ\", \"K2TNO\"], [\"KG5SQJ\", \"K2TNO\"], [\"KG5SQJ\", \"WN7Y\"], [\"KG5SQJ\", \"WN7Y\"], [\"KG5SQJ\", \"KN4ETD\"], [\"KG5SQJ\", \"KN4ETD\"], [\"KG5SQJ\", \"NT6X\"], [\"KG5SQJ\", \"NT6X\"], [\"KG5SQJ\", \"W4CHI\"], [\"KG5SQJ\", \"W4CHI\"], [\"KG5SQJ\", \"N5DN\"], [\"KG5SQJ\", \"N5DN\"], [\"KG5SQJ\", \"K8MV\"], [\"KG5SQJ\", \"K8MV\"], [\"KG5SQJ\", \"KB0NES\"], [\"KG5SQJ\", \"KB0NES\"], [\"KG5SQJ\", \"VE9CZ\"], [\"KG5SQJ\", \"VE9CZ\"], [\"KG5SQJ\", \"KK4WX\"], [\"KG5SQJ\", \"KK4WX\"], [\"KG5SQJ\", \"K2KAR\"], [\"KG5SQJ\", \"K2KAR\"], [\"KG5SQJ\", \"VE2GT\"], [\"KG5SQJ\", \"VE2GT\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"K5EC\"], [\"KG5SQJ\", \"K5WW\"], [\"KG5SQJ\", \"K5WW\"], [\"KG5SQJ\", \"VE9CF\"], [\"KG5SQJ\", \"VE9CF\"], [\"KG5VK\", \"NX5M\"], [\"KG5VK\", \"NX5M\"], [\"KG5VK\", \"KE4Q\"], [\"KG5VK\", \"KE4Q\"], [\"KG5VK\", \"N2MF\"], [\"KG5VK\", \"N2MF\"], [\"KG5VK\", \"KA6BIM\"], [\"KG5VK\", \"KA6BIM\"], [\"KG5VK\", \"WU8T\"], [\"KG5VK\", \"WU8T\"], [\"KG5VK\", \"W5GCX\"], [\"KG5VK\", \"W5GCX\"], [\"KG5VK\", \"AJ4F\"], [\"KG5VK\", \"AJ4F\"], [\"KG5VK\", \"N7EPD\"], [\"KG5VK\", \"N7EPD\"], [\"KG5VK\", \"VE2FK\"], [\"KG5VK\", \"VE2FK\"], [\"KI4MZC\", \"K5T\"], [\"KI4MZC\", \"K5T\"], [\"KI4MZC\", \"K5TIA\"], [\"KI4MZC\", \"K5TIA\"], [\"KI4MZC\", \"K1SP\"], [\"KI4MZC\", \"K1SP\"], [\"KI5GNH\", \"K0AD\"], [\"KI5GNH\", \"K0AD\"], [\"KI5GNH\", \"KB0XY\"], [\"KI5GNH\", \"KB0XY\"], [\"KI5GNH\", \"WV4P\"], [\"KI5GNH\", \"WV4P\"], [\"KI5GNH\", \"AI4DB\"], [\"KI5GNH\", \"AI4DB\"], [\"KI5GNH\", \"WA5DSS\"], [\"KI5GNH\", \"WA5DSS\"], [\"KI5GNH\", \"K3TD\"], [\"KI5GNH\", \"K3TD\"], [\"KI5GNH\", \"W0UC\"], [\"KI5GNH\", \"W0UC\"], [\"KI5NCJ\", \"WJ9O\"], [\"KI5NCJ\", \"WJ9O\"], [\"KI5NCJ\", \"K5MAY\"], [\"KI5NCJ\", \"K5MAY\"], [\"KI5NCJ\", \"K5GAL\"], [\"KI5NCJ\", \"K5GAL\"], [\"KI5NCJ\", \"AA3R\"], [\"KI5NCJ\", \"AA3R\"], [\"KI5NCJ\", \"WA5DTK\"], [\"KI5NCJ\", \"WA5DTK\"], [\"KI5NCJ\", \"N5SLY\"], [\"KI5NCJ\", \"N5SLY\"], [\"KI5NCJ\", \"N5WRX\"], [\"KI5NCJ\", \"N5WRX\"], [\"KI5NCJ\", \"WA5DSS\"], [\"KI5NCJ\", \"WA5DSS\"], [\"KJ5IEL\", \"K5EC\"], [\"KJ5IEL\", \"K5EC\"], [\"KJ5IEL\", \"OM2VL\"], [\"KJ5IEL\", \"OM2VL\"], [\"KJ5IEL\", \"KJ9C\"], [\"KJ5IEL\", \"KJ9C\"], [\"KJ5IEL\", \"WA5DTK\"], [\"KJ5IEL\", \"WA5DTK\"], [\"KJ5IEL\", \"KN6VTC\"], [\"KJ5IEL\", \"KN6VTC\"], [\"KJ5IEL\", \"N1ADX\"], [\"KJ5IEL\", \"N1ADX\"], [\"KJ5IEL\", \"N9PCS\"], [\"KJ5IEL\", \"N9PCS\"], [\"KJ9B\", \"W5LIC\"], [\"KJ9B\", \"W5LIC\"], [\"KJ9C\", \"K5TIA\"], [\"KJ9C\", \"K5TIA\"], [\"KJ9C\", \"KK5TY\"], [\"KJ9C\", \"KK5TY\"], [\"KJ9C\", \"N7EPD\"], [\"KJ9C\", \"N7EPD\"], [\"KJ9C\", \"W5LO\"], [\"KJ9C\", \"W5LO\"], [\"KJ9C\", \"NX5M\"], [\"KJ9C\", \"NX5M\"], [\"KJ9C\", \"N7EPD\"], [\"KJ9C\", \"N7EPD\"], [\"KJ9C\", \"NU5M\"], [\"KJ9C\", \"NU5M\"], [\"KJ9C\", \"W5JK\"], [\"KJ9C\", \"W5JK\"], [\"KJ9C\", \"K0PC\"], [\"KJ9C\", \"K0PC\"], [\"KJ9C\", \"K0PC\"], [\"KJ9C\", \"K0PC\"], [\"KK4JOE\", \"N5DN\"], [\"KK4JOE\", \"N5DN\"], [\"KK5TY\", \"K5EC\"], [\"KK5TY\", \"K5EC\"], [\"KK5TY\", \"K5QHD\"], [\"KK5TY\", \"K5QHD\"], [\"KK5TY\", \"W5GCX\"], [\"KK5TY\", \"W5GCX\"], [\"KK5TY\", \"K1ORY\"], [\"KK5TY\", \"K1ORY\"], [\"KK5TY\", \"WA2QAU\"], [\"KK5TY\", \"WA2QAU\"], [\"KK5TY\", \"F8PDR\"], [\"KK5TY\", \"F8PDR\"], [\"KM5Z\", \"KI5GNH\"], [\"KM5Z\", \"KI5GNH\"], [\"KN4JN\", \"NX5M\"], [\"KN4JN\", \"NX5M\"], [\"KN6VTC\", \"N5WBL\"], [\"KN6VTC\", \"N5WBL\"], [\"KN6VTC\", \"KG5LJZ\"], [\"KN6VTC\", \"KG5LJZ\"], [\"KN6VTC\", \"K5CM\"], [\"KN6VTC\", \"K5CM\"], [\"KN6VTC\", \"K5CM\"], [\"KN6VTC\", \"K5CM\"], [\"KN6VTC\", \"K5MAY\"], [\"KN6VTC\", \"K5MAY\"], [\"KN6VTC\", \"KJ5IEL\"], [\"KN6VTC\", \"KJ5IEL\"], [\"KO4QEX\", \"N5WCT\"], [\"KO4QEX\", \"N5WCT\"], [\"KR1BBT\", \"W5LIC\"], [\"KR1BBT\", \"W5LIC\"], [\"KR7D\", \"K5OT\"], [\"KR7D\", \"K5OT\"], [\"KR7D\", \"W6AFA\"], [\"KR7D\", \"W6AFA\"], [\"KS4X\", \"K5QHD\"], [\"KS4X\", \"K5QHD\"], [\"KT3X\", \"NE8P\"], [\"KT3X\", \"NE8P\"], [\"KT3X\", \"W0UC\"], [\"KT3X\", \"W0UC\"], [\"KT3X\", \"K4MMW\"], [\"KT3X\", \"K4MMW\"], [\"KT3X\", \"AA3R\"], [\"KT3X\", \"AA3R\"], [\"KT3X\", \"WA2QAU\"], [\"KT3X\", \"WA2QAU\"], [\"KT3X\", \"N1LN\"], [\"KT3X\", \"N1LN\"], [\"KT3X\", \"AA3R\"], [\"KT3X\", \"AA3R\"], [\"KT3X\", \"AA3R\"], [\"KT3X\", \"AA3R\"], [\"KT3X\", \"F8PDR\"], [\"KT3X\", \"F8PDR\"], [\"KT3X\", \"F8PDR\"], [\"KT3X\", \"F8PDR\"], [\"KT3X\", \"WX8C\"], [\"KT3X\", \"WX8C\"], [\"KT3X\", \"WX8C\"], [\"KT3X\", \"WX8C\"], [\"KT3X\", \"WX8C\"], [\"KT3X\", \"WX8C\"], [\"KT3X\", \"KE3LA\"], [\"KT3X\", \"KE3LA\"], [\"KT3X\", \"KE3LA\"], [\"KT3X\", \"KE3LA\"], [\"KT3X\", \"KE3LA\"], [\"KT3X\", \"KE3LA\"], [\"KT3X\", \"KY4L\"], [\"KT3X\", \"KY4L\"], [\"KT3X\", \"AA3R\"], [\"KT3X\", \"AA3R\"], [\"KT3X\", \"AA3R\"], [\"KT3X\", \"AA3R\"], [\"KT3X\", \"KB4CG\"], [\"KT3X\", \"KB4CG\"], [\"KT3X\", \"KB4CG\"], [\"KT3X\", \"KB4CG\"], [\"KT3X\", \"KB4CG\"], [\"KT3X\", \"KB4CG\"], [\"KT3X\", \"N2MF\"], [\"KT3X\", \"N2MF\"], [\"KT3X\", \"N8II\"], [\"KT3X\", \"N8II\"], [\"KT3X\", \"W2TB\"], [\"KT3X\", \"W2TB\"], [\"KT3X\", \"NW7DX\"], [\"KT3X\", \"NW7DX\"], [\"KT3X\", \"NW7DX\"], [\"KT3X\", \"NW7DX\"], [\"KT3X\", \"NM5M\"], [\"KT3X\", \"NM5M\"], [\"KT3X\", \"NM5M\"], [\"KT3X\", \"NM5M\"], [\"KT3X\", \"W5NC\"], [\"KT3X\", \"W5NC\"], [\"KT3X\", \"WA6KHK\"], [\"KT3X\", \"WA6KHK\"], [\"KT3X\", \"K2HT\"], [\"KT3X\", \"K2HT\"], [\"KT3X\", \"N5XZ\"], [\"KT3X\", \"N5XZ\"], [\"KT3X\", \"N5XZ\"], [\"KT3X\", \"N5XZ\"], [\"KT3X\", \"KG5OWB\"], [\"KT3X\", \"KG5OWB\"], [\"KT3X\", \"KG5OWB\"], [\"KT3X\", \"KG5OWB\"], [\"KT3X\", \"WA2JQK\"], [\"KT3X\", \"WA2JQK\"], [\"KT3X\", \"WA2JQK\"], [\"KT3X\", \"WA2JQK\"], [\"KT3X\", \"F8PDR\"], [\"KT3X\", \"F8PDR\"], [\"KT3X\", \"F8PDR\"], [\"KT3X\", \"F8PDR\"], [\"KT3X\", \"WO4O\"], [\"KT3X\", \"WO4O\"], [\"KT3X\", \"KK5TY\"], [\"KT3X\", \"KK5TY\"], [\"KT3X\", \"VE2FK\"], [\"KT3X\", \"VE2FK\"], [\"KT3X\", \"W5NC\"], [\"KT3X\", \"W5NC\"], [\"KT3X\", \"K8MV\"], [\"KT3X\", \"K8MV\"], [\"KU8E\", \"W5CUB\"], [\"KU8E\", \"W5CUB\"], [\"KU8E\", \"W5JK\"], [\"KU8E\", \"W5JK\"], [\"KV8Q\", \"N5JJ\"], [\"KV8Q\", \"N5JJ\"], [\"KV8Q\", \"N5T\"], [\"KV8Q\", \"N5T\"], [\"KV8Q\", \"N5T\"], [\"KV8Q\", \"N5T\"], [\"KV8Q\", \"KG5VK\"], [\"KV8Q\", \"KG5VK\"], [\"KV8Q\", \"KT3X\"], [\"KV8Q\", \"KT3X\"], [\"KV8Q\", \"KT3X\"], [\"KV8Q\", \"KT3X\"], [\"KV8Q\", \"KT3X\"], [\"KV8Q\", \"KT3X\"], [\"KW4EE\", \"W5ACQ\"], [\"KW4EE\", \"W5ACQ\"], [\"KW4EE\", \"K5T\"], [\"KW4EE\", \"K5T\"], [\"KW4EE\", \"K5T\"], [\"KW4EE\", \"K5T\"], [\"KY4L\", \"N5TJ\"], [\"KY4L\", \"N5TJ\"], [\"KZ3P\", \"KF5YUB\"], [\"KZ3P\", \"KF5YUB\"], [\"KZ3P\", \"N5XZ\"], [\"KZ3P\", \"N5XZ\"], [\"KZ3P\", \"W5HI\"], [\"KZ3P\", \"W5HI\"], [\"KZ3P\", \"K5ECT\"], [\"KZ3P\", \"K5ECT\"], [\"N0IIL\", \"K5B\"], [\"N0IIL\", \"K5B\"], [\"N0IIL\", \"K5K\"], [\"N0IIL\", \"K5K\"], [\"N0TT\", \"K5T\"], [\"N0TT\", \"K5T\"], [\"N0YL\", \"WA5DTK\"], [\"N0YL\", \"WA5DTK\"], [\"N1ADX\", \"KJ5IEL\"], [\"N1ADX\", \"KJ5IEL\"], [\"N1CEO\", \"N5XZ\"], [\"N1CEO\", \"N5XZ\"], [\"N1LN\", \"W5LXS\"], [\"N1LN\", \"W5LXS\"], [\"N1LN\", \"K5IZO\"], [\"N1LN\", \"K5IZO\"], [\"N1LN\", \"W5KU\"], [\"N1LN\", \"W5KU\"], [\"N1LN\", \"AA5UN\"], [\"N1LN\", \"AA5UN\"], [\"N1LN\", \"KT3X\"], [\"N1LN\", \"KT3X\"], [\"N1LN\", \"KT3X\"], [\"N1LN\", \"KT3X\"], [\"N1LN\", \"KT3X\"], [\"N1LN\", \"KT3X\"], [\"N2EIM\", \"K5K\"], [\"N2EIM\", \"K5K\"], [\"N2EIM\", \"K5K\"], [\"N2EIM\", \"K5K\"], [\"N2EIM\", \"N5XZ\"], [\"N2EIM\", \"N5XZ\"], [\"N2MF\", \"W5AL\"], [\"N2MF\", \"W5AL\"], [\"N2MF\", \"AD4EB\"], [\"N2MF\", \"AD4EB\"], [\"N2MF\", \"AD4EB\"], [\"N2MF\", \"AD4EB\"], [\"N2OIG\", \"W0VX\"], [\"N2OIG\", \"W0VX\"], [\"N2OIG\", \"WA8ZBT\"], [\"N2OIG\", \"WA8ZBT\"], [\"N3KN\", \"KF5YUB\"], [\"N3KN\", \"KF5YUB\"], [\"N3KN\", \"AD4EB\"], [\"N3KN\", \"AD4EB\"], [\"N4AO\", \"W5JK\"], [\"N4AO\", \"W5JK\"], [\"N4AO\", \"AD4EB\"], [\"N4AO\", \"AD4EB\"], [\"N4IU\", \"NX5M\"], [\"N4IU\", \"NX5M\"], [\"N5AW\", \"K5IZO\"], [\"N5AW\", \"K5IZO\"], [\"N5AW\", \"N5VBP\"], [\"N5AW\", \"N5VBP\"], [\"N5DN\", \"N5JJ\"], [\"N5DN\", \"N5JJ\"], [\"N5DN\", \"K5QHD\"], [\"N5DN\", \"K5QHD\"], [\"N5DN\", \"WA5DCT\"], [\"N5DN\", \"WA5DCT\"], [\"N5DN\", \"KK4JOE\"], [\"N5DN\", \"KK4JOE\"], [\"N5DN\", \"F8PDR\"], [\"N5DN\", \"F8PDR\"], [\"N5DTT\", \"N5DN\"], [\"N5DTT\", \"N5DN\"], [\"N5DTT\", \"NU5DE\"], [\"N5DTT\", \"NU5DE\"], [\"N5DTT\", \"K5WA\"], [\"N5DTT\", \"K5WA\"], [\"N5ECY\", \"KE5C\"], [\"N5ECY\", \"KE5C\"], [\"N5ECY\", \"KE5C\"], [\"N5ECY\", \"KE5C\"], [\"N5ECY\", \"KE5C\"], [\"N5ECY\", \"KE5C\"], [\"N5ECY\", \"N5NU\"], [\"N5ECY\", \"N5NU\"], [\"N5EP\", \"N5NA\"], [\"N5EP\", \"N5NA\"], [\"N5EP\", \"N5NU\"], [\"N5EP\", \"N5NU\"], [\"N5EP\", \"WB5BKL\"], [\"N5EP\", \"WB5BKL\"], [\"N5IT\", \"WA5CKF\"], [\"N5IT\", \"WA5CKF\"], [\"N5IT\", \"K5QHD\"], [\"N5IT\", \"K5QHD\"], [\"N5IT\", \"N5SLY\"], [\"N5IT\", \"N5SLY\"], [\"N5IT\", \"W5KU\"], [\"N5IT\", \"W5KU\"], [\"N5IT\", \"K5UBE\"], [\"N5IT\", \"K5UBE\"], [\"N5J\", \"NE5B\"], [\"N5J\", \"NE5B\"], [\"N5JDT\", \"K5EC\"], [\"N5JDT\", \"K5EC\"], [\"N5JJ\", \"WW5L\"], [\"N5JJ\", \"WW5L\"], [\"N5JJ\", \"KT3X\"], [\"N5JJ\", \"KT3X\"], [\"N5JJ\", \"K8RGI\"], [\"N5JJ\", \"K8RGI\"], [\"N5JJ\", \"N5YA\"], [\"N5JJ\", \"N5YA\"], [\"N5JJ\", \"K2KAR\"], [\"N5JJ\", \"K2KAR\"], [\"N5KW\", \"K3IE\"], [\"N5KW\", \"K3IE\"], [\"N5KW\", \"W0PI\"], [\"N5KW\", \"W0PI\"], [\"N5KW\", \"W0PI\"], [\"N5KW\", \"W0PI\"], [\"N5KW\", \"KA0PQW\"], [\"N5KW\", \"KA0PQW\"], [\"N5KW\", \"W4YE\"], [\"N5KW\", \"W4YE\"], [\"N5KW\", \"F8PDR\"], [\"N5KW\", \"F8PDR\"], [\"N5KW\", \"F8PDR\"], [\"N5KW\", \"F8PDR\"], [\"N5KW\", \"N6DW\"], [\"N5KW\", \"N6DW\"], [\"N5KW\", \"N6DW\"], [\"N5KW\", \"N6DW\"], [\"N5KW\", \"VE3YT\"], [\"N5KW\", \"VE3YT\"], [\"N5KW\", \"KC3M\"], [\"N5KW\", \"KC3M\"], [\"N5KW\", \"KC3M\"], [\"N5KW\", \"KC3M\"], [\"N5KW\", \"KK4CS\"], [\"N5KW\", \"KK4CS\"], [\"N5KW\", \"KK4CS\"], [\"N5KW\", \"KK4CS\"], [\"N5KW\", \"N8II\"], [\"N5KW\", \"N8II\"], [\"N5KW\", \"N7AME\"], [\"N5KW\", \"N7AME\"], [\"N5KW\", \"AG5T\"], [\"N5KW\", \"AG5T\"], [\"N5KW\", \"N5WRX\"], [\"N5KW\", \"N5WRX\"], [\"N5KW\", \"N5WRX\"], [\"N5KW\", \"N5WRX\"], [\"N5KW\", \"N5WRX\"], [\"N5KW\", \"N5WRX\"], [\"N5KW\", \"K1BZ\"], [\"N5KW\", \"K1BZ\"], [\"N5KW\", \"K1BZ\"], [\"N5KW\", \"K1BZ\"], [\"N5KW\", \"K1BZ\"], [\"N5KW\", \"K1BZ\"], [\"N5KW\", \"F6JXR\"], [\"N5KW\", \"F6JXR\"], [\"N5KW\", \"F6JXR\"], [\"N5KW\", \"F6JXR\"], [\"N5KW\", \"F6JXR\"], [\"N5KW\", \"F6JXR\"], [\"N5KW\", \"AA3R\"], [\"N5KW\", \"AA3R\"], [\"N5KW\", \"AA3R\"], [\"N5KW\", \"AA3R\"], [\"N5KW\", \"AA3R\"], [\"N5KW\", \"AA3R\"], [\"N5KW\", \"WA2JQK\"], [\"N5KW\", \"WA2JQK\"], [\"N5KW\", \"W2TB\"], [\"N5KW\", \"W2TB\"], [\"N5KW\", \"W2TB\"], [\"N5KW\", \"W2TB\"], [\"N5KW\", \"W2TB\"], [\"N5KW\", \"W2TB\"], [\"N5KW\", \"W9QL\"], [\"N5KW\", \"W9QL\"], [\"N5KW\", \"W9QL\"], [\"N5KW\", \"W9QL\"], [\"N5KW\", \"W9QL\"], [\"N5KW\", \"W9QL\"], [\"N5KW\", \"WB2WPM\"], [\"N5KW\", \"WB2WPM\"], [\"N5KW\", \"N9GXA\"], [\"N5KW\", \"N9GXA\"], [\"N5KW\", \"N9GXA\"], [\"N5KW\", \"N9GXA\"], [\"N5KW\", \"OM2VL\"], [\"N5KW\", \"OM2VL\"], [\"N5KW\", \"KZ3P\"], [\"N5KW\", \"KZ3P\"], [\"N5KW\", \"KZ3P\"], [\"N5KW\", \"KZ3P\"], [\"N5KW\", \"WA2JQK\"], [\"N5KW\", \"WA2JQK\"], [\"N5KW\", \"WA2JQK\"], [\"N5KW\", \"WA2JQK\"], [\"N5KW\", \"W3US\"], [\"N5KW\", \"W3US\"], [\"N5KW\", \"W3US\"], [\"N5KW\", \"W3US\"], [\"N5KW\", \"WX8C\"], [\"N5KW\", \"WX8C\"], [\"N5KW\", \"WX8C\"], [\"N5KW\", \"WX8C\"], [\"N5KW\", \"KN6VTC\"], [\"N5KW\", \"KN6VTC\"], [\"N5KW\", \"KB9LGS\"], [\"N5KW\", \"KB9LGS\"], [\"N5KW\", \"KB9LGS\"], [\"N5KW\", \"KB9LGS\"], [\"N5NA\", \"WA5DTK\"], [\"N5NA\", \"WA5DTK\"], [\"N5NA\", \"N5EP\"], [\"N5NA\", \"N5EP\"], [\"N5NA\", \"W5KU\"], [\"N5NA\", \"W5KU\"], [\"N5NA\", \"VE7SCC\"], [\"N5NA\", \"VE7SCC\"], [\"N5NA\", \"N7SE\"], [\"N5NA\", \"N7SE\"], [\"N5NA\", \"F8PDR\"], [\"N5NA\", \"F8PDR\"], [\"N5NA\", \"F8PDR\"], [\"N5NA\", \"F8PDR\"], [\"N5NA\", \"N5JJ\"], [\"N5NA\", \"N5JJ\"], [\"N5NA\", \"N0YL\"], [\"N5NA\", \"N0YL\"], [\"N5NA\", \"WA2QAU\"], [\"N5NA\", \"WA2QAU\"], [\"N5NA\", \"NE8P\"], [\"N5NA\", \"NE8P\"], [\"N5NA\", \"WA5DTK\"], [\"N5NA\", \"WA5DTK\"], [\"N5NA\", \"K2YG\"], [\"N5NA\", \"K2YG\"], [\"N5NA\", \"WA5DTK\"], [\"N5NA\", \"WA5DTK\"], [\"N5NA\", \"K2SG\"], [\"N5NA\", \"K2SG\"], [\"N5NA\", \"K5K\"], [\"N5NA\", \"K5K\"], [\"N5NAA\", \"K2QB\"], [\"N5NAA\", \"K2QB\"], [\"N5NU\", \"WA5DTK\"], [\"N5NU\", \"WA5DTK\"], [\"N5NU\", \"AA3R\"], [\"N5NU\", \"AA3R\"], [\"N5NU\", \"K0TRL\"], [\"N5NU\", \"K0TRL\"], [\"N5NU\", \"K0TRL\"], [\"N5NU\", \"K0TRL\"], [\"N5NU\", \"KA6BIM\"], [\"N5NU\", \"KA6BIM\"], [\"N5NU\", \"N9GXA\"], [\"N5NU\", \"N9GXA\"], [\"N5NU\", \"F8PDR\"], [\"N5NU\", \"F8PDR\"], [\"N5NU\", \"N6AR\"], [\"N5NU\", \"N6AR\"], [\"N5NU\", \"AA6MU\"], [\"N5NU\", \"AA6MU\"], [\"N5NU\", \"WA6KHK\"], [\"N5NU\", \"WA6KHK\"], [\"N5NU\", \"K0MPH\"], [\"N5NU\", \"K0MPH\"], [\"N5NU\", \"K1ORY\"], [\"N5NU\", \"K1ORY\"], [\"N5NU\", \"N5ECY\"], [\"N5NU\", \"N5ECY\"], [\"N5NU\", \"KF3G\"], [\"N5NU\", \"KF3G\"], [\"N5NU\", \"K8MV\"], [\"N5NU\", \"K8MV\"], [\"N5PBP\", \"WA4JA\"], [\"N5PBP\", \"WA4JA\"], [\"N5PBP\", \"OM2VL\"], [\"N5PBP\", \"OM2VL\"], [\"N5PBP\", \"KA6BIM\"], [\"N5PBP\", \"KA6BIM\"], [\"N5PBP\", \"WA1SAY\"], [\"N5PBP\", \"WA1SAY\"], [\"N5PBP\", \"NZ5X\"], [\"N5PBP\", \"NZ5X\"], [\"N5RZ\", \"K0PC\"], [\"N5RZ\", \"K0PC\"], [\"N5RZ\", \"K0PC\"], [\"N5RZ\", \"K0PC\"], [\"N5RZ\", \"K1ORY\"], [\"N5RZ\", \"K1ORY\"], [\"N5RZ\", \"AA9RK\"], [\"N5RZ\", \"AA9RK\"], [\"N5RZ\", \"F8PDR\"], [\"N5RZ\", \"F8PDR\"], [\"N5SLY\", \"K0YY\"], [\"N5SLY\", \"K0YY\"], [\"N5SLY\", \"N5IT\"], [\"N5SLY\", \"N5IT\"], [\"N5SLY\", \"NU5M\"], [\"N5SLY\", \"NU5M\"], [\"N5SLY\", \"K5EC\"], [\"N5SLY\", \"K5EC\"], [\"N5SLY\", \"N5VBL\"], [\"N5SLY\", \"N5VBL\"], [\"N5SLY\", \"KI5NCJ\"], [\"N5SLY\", \"KI5NCJ\"], [\"N5T\", \"K2QB\"], [\"N5T\", \"K2QB\"], [\"N5T\", \"K2QB\"], [\"N5T\", \"K2QB\"], [\"N5T\", \"K2QB\"], [\"N5T\", \"K2QB\"], [\"N5T\", \"W8PI\"], [\"N5T\", \"W8PI\"], [\"N5T\", \"VE3YT\"], [\"N5T\", \"VE3YT\"], [\"N5T\", \"K4FT\"], [\"N5T\", \"K4FT\"], [\"N5T\", \"WA2QAU\"], [\"N5T\", \"WA2QAU\"], [\"N5T\", \"K3TW\"], [\"N5T\", \"K3TW\"], [\"N5T\", \"VA3IJK\"], [\"N5T\", \"VA3IJK\"], [\"N5T\", \"N3KN\"], [\"N5T\", \"N3KN\"], [\"N5T\", \"WA3AER\"], [\"N5T\", \"WA3AER\"], [\"N5T\", \"NQ1B\"], [\"N5T\", \"NQ1B\"], [\"N5T\", \"NQ1B\"], [\"N5T\", \"NQ1B\"], [\"N5T\", \"KI4MZC\"], [\"N5T\", \"KI4MZC\"], [\"N5T\", \"K8RGI\"], [\"N5T\", \"K8RGI\"], [\"N5T\", \"N8VU\"], [\"N5T\", \"N8VU\"], [\"N5T\", \"N8VU\"], [\"N5T\", \"N8VU\"], [\"N5T\", \"WA9LEY\"], [\"N5T\", \"WA9LEY\"], [\"N5T\", \"KA0PQW\"], [\"N5T\", \"KA0PQW\"], [\"N5T\", \"KA0PQW\"], [\"N5T\", \"KA0PQW\"], [\"N5T\", \"KD4S\"], [\"N5T\", \"KD4S\"], [\"N5T\", \"KN6VTC\"], [\"N5T\", \"KN6VTC\"], [\"N5T\", \"W8PI\"], [\"N5T\", \"W8PI\"], [\"N5T\", \"WA6KHK\"], [\"N5T\", \"WA6KHK\"], [\"N5T\", \"N9GXA\"], [\"N5T\", \"N9GXA\"], [\"N5T\", \"VE9CF\"], [\"N5T\", \"VE9CF\"], [\"N5T\", \"WY1H\"], [\"N5T\", \"WY1H\"], [\"N5T\", \"WY1H\"], [\"N5T\", \"WY1H\"], [\"N5T\", \"WQ6X\"], [\"N5T\", \"WQ6X\"], [\"N5T\", \"K7BG\"], [\"N5T\", \"K7BG\"], [\"N5T\", \"NI8W\"], [\"N5T\", \"NI8W\"], [\"N5T\", \"DL3GA\"], [\"N5T\", \"DL3GA\"], [\"N5T\", \"N1XI\"], [\"N5T\", \"N1XI\"], [\"N5T\", \"WO9B\"], [\"N5T\", \"WO9B\"], [\"N5T\", \"AC6ZM\"], [\"N5T\", \"AC6ZM\"], [\"N5T\", \"F8PDR\"], [\"N5T\", \"F8PDR\"], [\"N5T\", \"F8PDR\"], [\"N5T\", \"F8PDR\"], [\"N5T\", \"N5XZ\"], [\"N5T\", \"N5XZ\"], [\"N5T\", \"WA3AAN\"], [\"N5T\", \"WA3AAN\"], [\"N5T\", \"VE3KP\"], [\"N5T\", \"VE3KP\"], [\"N5T\", \"K0RC\"], [\"N5T\", \"K0RC\"], [\"N5T\", \"K0RC\"], [\"N5T\", \"K0RC\"], [\"N5T\", \"KC3M\"], [\"N5T\", \"KC3M\"], [\"N5T\", \"KY4L\"], [\"N5T\", \"KY4L\"], [\"N5T\", \"N0IIL\"], [\"N5T\", \"N0IIL\"], [\"N5T\", \"K5K\"], [\"N5T\", \"K5K\"], [\"N5T\", \"W5NC\"], [\"N5T\", \"W5NC\"], [\"N5TJ\", \"F8PDR\"], [\"N5TJ\", \"F8PDR\"], [\"N5TJ\", \"W5GCX\"], [\"N5TJ\", \"W5GCX\"], [\"N5TJ\", \"K1ORY\"], [\"N5TJ\", \"K1ORY\"], [\"N5TJ\", \"KY4L\"], [\"N5TJ\", \"KY4L\"], [\"N5TJ\", \"KG5OWB\"], [\"N5TJ\", \"KG5OWB\"], [\"N5TJ\", \"KT3X\"], [\"N5TJ\", \"KT3X\"], [\"N5TJ\", \"KT3X\"], [\"N5TJ\", \"KT3X\"], [\"N5TJ\", \"KT3X\"], [\"N5TJ\", \"KT3X\"], [\"N5TJ\", \"AD4EB\"], [\"N5TJ\", \"AD4EB\"], [\"N5TJ\", \"AD4EB\"], [\"N5TJ\", \"AD4EB\"], [\"N5TJ\", \"AD4EB\"], [\"N5TJ\", \"AD4EB\"], [\"N5TJ\", \"AD4EB\"], [\"N5TJ\", \"AD4EB\"], [\"N5TJ\", \"AD4EB\"], [\"N5TJ\", \"AD4EB\"], [\"N5TTT\", \"N6OKU\"], [\"N5TTT\", \"N6OKU\"], [\"N5TTT\", \"N6OKU\"], [\"N5TTT\", \"N6OKU\"], [\"N5VBL\", \"WA6KHK\"], [\"N5VBL\", \"WA6KHK\"], [\"N5VBL\", \"OM2VL\"], [\"N5VBL\", \"OM2VL\"], [\"N5VBL\", \"N6AR\"], [\"N5VBL\", \"N6AR\"], [\"N5VBP\", \"K5CM\"], [\"N5VBP\", \"K5CM\"], [\"N5VBP\", \"N5AW\"], [\"N5VBP\", \"N5AW\"], [\"N5WBL\", \"N7AME\"], [\"N5WBL\", \"N7AME\"], [\"N5WBL\", \"KJ5IEL\"], [\"N5WBL\", \"KJ5IEL\"], [\"N5WCT\", \"K5QHD\"], [\"N5WCT\", \"K5QHD\"], [\"N5WCT\", \"K2WJ\"], [\"N5WCT\", \"K2WJ\"], [\"N5WCT\", \"K5K\"], [\"N5WCT\", \"K5K\"], [\"N5WRX\", \"KI5GNH\"], [\"N5WRX\", \"KI5GNH\"], [\"N5WRX\", \"NE5B\"], [\"N5WRX\", \"NE5B\"], [\"N5WRX\", \"NW5Q\"], [\"N5WRX\", \"NW5Q\"], [\"N5XZ\", \"AD4EB\"], [\"N5XZ\", \"AD4EB\"], [\"N5XZ\", \"N5KW\"], [\"N5XZ\", \"N5KW\"], [\"N5XZ\", \"W5ESE\"], [\"N5XZ\", \"W5ESE\"], [\"N5XZ\", \"K1ORY\"], [\"N5XZ\", \"K1ORY\"], [\"N5XZ\", \"AD4EB\"], [\"N5XZ\", \"AD4EB\"], [\"N5XZ\", \"F8PDR\"], [\"N5XZ\", \"F8PDR\"], [\"N5XZ\", \"N9NM\"], [\"N5XZ\", \"N9NM\"], [\"N5XZ\", \"K0WRY\"], [\"N5XZ\", \"K0WRY\"], [\"N5XZ\", \"KD5ZZU\"], [\"N5XZ\", \"KD5ZZU\"], [\"N5XZ\", \"NN3E\"], [\"N5XZ\", \"NN3E\"], [\"N5XZ\", \"WU8T\"], [\"N5XZ\", \"WU8T\"], [\"N5XZ\", \"KB4DE\"], [\"N5XZ\", \"KB4DE\"], [\"N5XZ\", \"F8PDR\"], [\"N5XZ\", \"F8PDR\"], [\"N5XZ\", \"W8PI\"], [\"N5XZ\", \"W8PI\"], [\"N5XZ\", \"K5CM\"], [\"N5XZ\", \"K5CM\"], [\"N5XZ\", \"AC7DD\"], [\"N5XZ\", \"AC7DD\"], [\"N5YA\", \"K5QHD\"], [\"N5YA\", \"K5QHD\"], [\"N5YA\", \"NE8P\"], [\"N5YA\", \"NE8P\"], [\"N5YA\", \"W5ESE\"], [\"N5YA\", \"W5ESE\"], [\"N5YA\", \"K0SV\"], [\"N5YA\", \"K0SV\"], [\"N5YA\", \"K2SG\"], [\"N5YA\", \"K2SG\"], [\"N5YA\", \"KE0TT\"], [\"N5YA\", \"KE0TT\"], [\"N5YA\", \"VE2FK\"], [\"N5YA\", \"VE2FK\"], [\"N5YA\", \"K8MV\"], [\"N5YA\", \"K8MV\"], [\"N5YA\", \"N1LN\"], [\"N5YA\", \"N1LN\"], [\"N5YA\", \"K1GU\"], [\"N5YA\", \"K1GU\"], [\"N5YA\", \"N6DW\"], [\"N5YA\", \"N6DW\"], [\"N5YA\", \"K3TW\"], [\"N5YA\", \"K3TW\"], [\"N5YA\", \"KA3EHL\"], [\"N5YA\", \"KA3EHL\"], [\"N5YA\", \"K0TQ\"], [\"N5YA\", \"K0TQ\"], [\"N5YA\", \"W9QL\"], [\"N5YA\", \"W9QL\"], [\"N5YA\", \"N1XI\"], [\"N5YA\", \"N1XI\"], [\"N5YA\", \"K0PC\"], [\"N5YA\", \"K0PC\"], [\"N5YA\", \"AA7V\"], [\"N5YA\", \"AA7V\"], [\"N6AR\", \"N5T\"], [\"N6AR\", \"N5T\"], [\"N6AR\", \"N5WBL\"], [\"N6AR\", \"N5WBL\"], [\"N6AR\", \"AD4EB\"], [\"N6AR\", \"AD4EB\"], [\"N6AR\", \"KJ5IEL\"], [\"N6AR\", \"KJ5IEL\"], [\"N6AR\", \"NE5B\"], [\"N6AR\", \"NE5B\"], [\"N6DW\", \"K5WA\"], [\"N6DW\", \"K5WA\"], [\"N6DW\", \"AD4EB\"], [\"N6DW\", \"AD4EB\"], [\"N6DW\", \"K5OT\"], [\"N6DW\", \"K5OT\"], [\"N6MDV\", \"W5JK\"], [\"N6MDV\", \"W5JK\"], [\"N6MDV\", \"WA5DCT\"], [\"N6MDV\", \"WA5DCT\"], [\"N6OKU\", \"WJ9O\"], [\"N6OKU\", \"WJ9O\"], [\"N6OKU\", \"WA5CKF\"], [\"N6OKU\", \"WA5CKF\"], [\"N6OKU\", \"N5TTT\"], [\"N6OKU\", \"N5TTT\"], [\"N6OKU\", \"K2WJ\"], [\"N6OKU\", \"K2WJ\"], [\"N6OKU\", \"N5TTT\"], [\"N6OKU\", \"N5TTT\"], [\"N6OKU\", \"K5UBE\"], [\"N6OKU\", \"K5UBE\"], [\"N6TQ\", \"AD4EB\"], [\"N6TQ\", \"AD4EB\"], [\"N6TQ\", \"AD4EB\"], [\"N6TQ\", \"AD4EB\"], [\"N6TQ\", \"W5HI\"], [\"N6TQ\", \"W5HI\"], [\"N6TQ\", \"NE5B\"], [\"N6TQ\", \"NE5B\"], [\"N7AME\", \"N5KW\"], [\"N7AME\", \"N5KW\"], [\"N7EPD\", \"N9NM\"], [\"N7EPD\", \"N9NM\"], [\"N7EPD\", \"N9NM\"], [\"N7EPD\", \"N9NM\"], [\"N7EPD\", \"N5KW\"], [\"N7EPD\", \"N5KW\"], [\"N7EPD\", \"N5KW\"], [\"N7EPD\", \"N5KW\"], [\"N7EPD\", \"AD4EB\"], [\"N7EPD\", \"AD4EB\"], [\"N7EPD\", \"WA5DCT\"], [\"N7EPD\", \"WA5DCT\"], [\"N7EPD\", \"W5LO\"], [\"N7EPD\", \"W5LO\"], [\"N7EPD\", \"KG5VK\"], [\"N7EPD\", \"KG5VK\"], [\"N7EPD\", \"AD4EB\"], [\"N7EPD\", \"AD4EB\"], [\"N7IR\", \"WB5BKL\"], [\"N7IR\", \"WB5BKL\"], [\"N7IR\", \"K5OT\"], [\"N7IR\", \"K5OT\"], [\"N7SE\", \"N5NA\"], [\"N7SE\", \"N5NA\"], [\"N7SE\", \"KE5C\"], [\"N7SE\", \"KE5C\"], [\"N7SE\", \"WA5LFD\"], [\"N7SE\", \"WA5LFD\"], [\"N8DNA\", \"K5OT\"], [\"N8DNA\", \"K5OT\"], [\"N8II\", \"K5QHD\"], [\"N8II\", \"K5QHD\"], [\"N8II\", \"N5KW\"], [\"N8II\", \"N5KW\"], [\"N8II\", \"KT3X\"], [\"N8II\", \"KT3X\"], [\"N8II\", \"KT3X\"], [\"N8II\", \"KT3X\"], [\"N8II\", \"KT3X\"], [\"N8II\", \"KT3X\"], [\"N8VU\", \"N5T\"], [\"N8VU\", \"N5T\"], [\"N8VU\", \"W5NC\"], [\"N8VU\", \"W5NC\"], [\"N9GXA\", \"N5NU\"], [\"N9GXA\", \"N5NU\"], [\"N9GXA\", \"W5LXS\"], [\"N9GXA\", \"W5LXS\"], [\"N9GXA\", \"N5T\"], [\"N9GXA\", \"N5T\"], [\"N9GXA\", \"K5CM\"], [\"N9GXA\", \"K5CM\"], [\"N9GXA\", \"N5KW\"], [\"N9GXA\", \"N5KW\"], [\"N9GXA\", \"AD4EB\"], [\"N9GXA\", \"AD4EB\"], [\"N9GXA\", \"K5CM\"], [\"N9GXA\", \"K5CM\"], [\"N9NM\", \"N5XZ\"], [\"N9NM\", \"N5XZ\"], [\"N9NM\", \"K5K\"], [\"N9NM\", \"K5K\"], [\"NA4C\", \"N5NA\"], [\"NA4C\", \"N5NA\"], [\"NC4FG\", \"NU5M\"], [\"NC4FG\", \"NU5M\"], [\"NC4FG\", \"NU5M\"], [\"NC4FG\", \"NU5M\"], [\"NC4FG\", \"K5CM\"], [\"NC4FG\", \"K5CM\"], [\"NC5T\", \"WA5DCT\"], [\"NC5T\", \"WA5DCT\"], [\"ND0C\", \"K5T\"], [\"ND0C\", \"K5T\"], [\"ND0C\", \"K5T\"], [\"ND0C\", \"K5T\"], [\"ND0C\", \"K5T\"], [\"ND0C\", \"K5T\"], [\"ND0C\", \"K5T\"], [\"ND0C\", \"K5T\"], [\"ND0C\", \"K5B\"], [\"ND0C\", \"K5B\"], [\"ND0C\", \"K5B\"], [\"ND0C\", \"K5B\"], [\"ND0C\", \"KG5LJZ\"], [\"ND0C\", \"KG5LJZ\"], [\"ND0C\", \"K5T\"], [\"ND0C\", \"K5T\"], [\"ND0C\", \"K5T\"], [\"ND0C\", \"K5T\"], [\"NE5B\", \"K5QHD\"], [\"NE5B\", \"K5QHD\"], [\"NE5B\", \"KF5VDX\"], [\"NE5B\", \"KF5VDX\"], [\"NE5B\", \"WA5CKF\"], [\"NE5B\", \"WA5CKF\"], [\"NE5B\", \"K5EC\"], [\"NE5B\", \"K5EC\"], [\"NE5B\", \"N5J\"], [\"NE5B\", \"N5J\"], [\"NE8P\", \"K5QHD\"], [\"NE8P\", \"K5QHD\"], [\"NE8P\", \"WA5DCT\"], [\"NE8P\", \"WA5DCT\"], [\"NE8P\", \"NX5M\"], [\"NE8P\", \"NX5M\"], [\"NM2A\", \"KG5IEE\"], [\"NM2A\", \"KG5IEE\"], [\"NM5M\", \"K2QB\"], [\"NM5M\", \"K2QB\"], [\"NM5M\", \"F8PDR\"], [\"NM5M\", \"F8PDR\"], [\"NO5W\", \"KG5VK\"], [\"NO5W\", \"KG5VK\"], [\"NO5W\", \"KG5OWB\"], [\"NO5W\", \"KG5OWB\"], [\"NQ1B\", \"N5T\"], [\"NQ1B\", \"N5T\"], [\"NQ9N\", \"NU5M\"], [\"NQ9N\", \"NU5M\"], [\"NQ9N\", \"KG5LJZ\"], [\"NQ9N\", \"KG5LJZ\"], [\"NQ9N\", \"K5EC\"], [\"NQ9N\", \"K5EC\"], [\"NQ9N\", \"K5EC\"], [\"NQ9N\", \"K5EC\"], [\"NQ9N\", \"K5EC\"], [\"NQ9N\", \"K5EC\"], [\"NR0P\", \"KD5ZZU\"], [\"NR0P\", \"KD5ZZU\"], [\"NS4X\", \"W5JK\"], [\"NS4X\", \"W5JK\"], [\"NT6X\", \"KG5LJZ\"], [\"NT6X\", \"KG5LJZ\"], [\"NU5DE\", \"K8MV\"], [\"NU5DE\", \"K8MV\"], [\"NU5DE\", \"WU8T\"], [\"NU5DE\", \"WU8T\"], [\"NU5DE\", \"WA5CKF\"], [\"NU5DE\", \"WA5CKF\"], [\"NU5DE\", \"KE5OBS\"], [\"NU5DE\", \"KE5OBS\"], [\"NU5DE\", \"KE5OBS\"], [\"NU5DE\", \"KE5OBS\"], [\"NU5DE\", \"K5QHD\"], [\"NU5DE\", \"K5QHD\"], [\"NU5DE\", \"KC6UCN\"], [\"NU5DE\", \"KC6UCN\"], [\"NU5DE\", \"KD5ZZU\"], [\"NU5DE\", \"KD5ZZU\"], [\"NU5M\", \"WA5CKF\"], [\"NU5M\", \"WA5CKF\"], [\"NU5M\", \"NQ9N\"], [\"NU5M\", \"NQ9N\"], [\"NU5M\", \"K5QHD\"], [\"NU5M\", \"K5QHD\"], [\"NU5M\", \"KK5TY\"], [\"NU5M\", \"KK5TY\"], [\"NU5M\", \"N5SLY\"], [\"NU5M\", \"N5SLY\"], [\"NU5M\", \"NC4FG\"], [\"NU5M\", \"NC4FG\"], [\"NU5M\", \"PU5HVK\"], [\"NU5M\", \"PU5HVK\"], [\"NU5M\", \"K5CM\"], [\"NU5M\", \"K5CM\"], [\"NU5M\", \"KJ9C\"], [\"NU5M\", \"KJ9C\"], [\"NU5M\", \"NC4FG\"], [\"NU5M\", \"NC4FG\"], [\"NV4T\", \"K5T\"], [\"NV4T\", \"K5T\"], [\"NV4T\", \"K5T\"], [\"NV4T\", \"K5T\"], [\"NV4T\", \"K5QHD\"], [\"NV4T\", \"K5QHD\"], [\"NV4T\", \"KI5NCJ\"], [\"NV4T\", \"KI5NCJ\"], [\"NV4T\", \"N5XZ\"], [\"NV4T\", \"N5XZ\"], [\"NW0M\", \"WA5DTK\"], [\"NW0M\", \"WA5DTK\"], [\"NW5Q\", \"WA5DCT\"], [\"NW5Q\", \"WA5DCT\"], [\"NW5Q\", \"N5WRX\"], [\"NW5Q\", \"N5WRX\"], [\"NW7DX\", \"W5ACQ\"], [\"NW7DX\", \"W5ACQ\"], [\"NW7DX\", \"N5JJ\"], [\"NW7DX\", \"N5JJ\"], [\"NX5M\", \"AD4EB\"], [\"NX5M\", \"AD4EB\"], [\"NX5M\", \"WA3AER\"], [\"NX5M\", \"WA3AER\"], [\"NX5M\", \"N4IU\"], [\"NX5M\", \"N4IU\"], [\"NX5M\", \"N5JJ\"], [\"NX5M\", \"N5JJ\"], [\"NX5M\", \"K5QHD\"], [\"NX5M\", \"K5QHD\"], [\"NX5M\", \"WA5CKF\"], [\"NX5M\", \"WA5CKF\"], [\"NX5M\", \"KD5ZZU\"], [\"NX5M\", \"KD5ZZU\"], [\"NX5M\", \"F8PDR\"], [\"NX5M\", \"F8PDR\"], [\"NX5M\", \"N5SLY\"], [\"NX5M\", \"N5SLY\"], [\"NX5M\", \"N5J\"], [\"NX5M\", \"N5J\"], [\"NX5M\", \"KT3X\"], [\"NX5M\", \"KT3X\"], [\"NX5M\", \"KJ9C\"], [\"NX5M\", \"KJ9C\"], [\"NX5M\", \"K1ORY\"], [\"NX5M\", \"K1ORY\"], [\"NX5M\", \"KN4JN\"], [\"NX5M\", \"KN4JN\"], [\"NX5M\", \"KC6UCN\"], [\"NX5M\", \"KC6UCN\"], [\"NX5M\", \"K5WW\"], [\"NX5M\", \"K5WW\"], [\"NX5M\", \"AD4EB\"], [\"NX5M\", \"AD4EB\"], [\"NX5M\", \"F8PDR\"], [\"NX5M\", \"F8PDR\"], [\"NX5M\", \"K5CM\"], [\"NX5M\", \"K5CM\"], [\"NX5M\", \"AD4EB\"], [\"NX5M\", \"AD4EB\"], [\"NX5M\", \"F8PDR\"], [\"NX5M\", \"F8PDR\"], [\"NZ5X\", \"WA5DTK\"], [\"NZ5X\", \"WA5DTK\"], [\"NZ5X\", \"K5ECT\"], [\"NZ5X\", \"K5ECT\"], [\"OM2VL\", \"K5WA\"], [\"OM2VL\", \"K5WA\"], [\"OM2VL\", \"NU5DE\"], [\"OM2VL\", \"NU5DE\"], [\"OM2VL\", \"W5GCX\"], [\"OM2VL\", \"W5GCX\"], [\"OM2VL\", \"K5WA\"], [\"OM2VL\", \"K5WA\"], [\"OM2VL\", \"KK5TY\"], [\"OM2VL\", \"KK5TY\"], [\"OM2VL\", \"W5LIC\"], [\"OM2VL\", \"W5LIC\"], [\"OM2VL\", \"K5K\"], [\"OM2VL\", \"K5K\"], [\"OM2VL\", \"K5K\"], [\"OM2VL\", \"K5K\"], [\"OM2VL\", \"KE5OBS\"], [\"OM2VL\", \"KE5OBS\"], [\"OM2VL\", \"KE5OBS\"], [\"OM2VL\", \"KE5OBS\"], [\"OM2VL\", \"N5VBL\"], [\"OM2VL\", \"N5VBL\"], [\"OM2VL\", \"KJ5IEL\"], [\"OM2VL\", \"KJ5IEL\"], [\"OM2VL\", \"WA5DTK\"], [\"OM2VL\", \"WA5DTK\"], [\"OM2VL\", \"K5B\"], [\"OM2VL\", \"K5B\"], [\"OM2VL\", \"K5B\"], [\"OM2VL\", \"K5B\"], [\"OM2VL\", \"N5PBP\"], [\"OM2VL\", \"N5PBP\"], [\"OM2VL\", \"KT3X\"], [\"OM2VL\", \"KT3X\"], [\"OM2VL\", \"N5YA\"], [\"OM2VL\", \"N5YA\"], [\"OM2VL\", \"K5WA\"], [\"OM2VL\", \"K5WA\"], [\"OM2VL\", \"N5KW\"], [\"OM2VL\", \"N5KW\"], [\"OM2VL\", \"KD5ZZU\"], [\"OM2VL\", \"KD5ZZU\"], [\"OM2VL\", \"K5K\"], [\"OM2VL\", \"K5K\"], [\"OM2VL\", \"AA5UN\"], [\"OM2VL\", \"AA5UN\"], [\"OM2VL\", \"W5ESE\"], [\"OM2VL\", \"W5ESE\"], [\"OM2VL\", \"K5TU\"], [\"OM2VL\", \"K5TU\"], [\"PU5HVK\", \"NU5M\"], [\"PU5HVK\", \"NU5M\"], [\"SP6JOE\", \"K5WA\"], [\"SP6JOE\", \"K5WA\"], [\"SP6JOE\", \"N5XZ\"], [\"SP6JOE\", \"N5XZ\"], [\"SP6JOE\", \"NX5M\"], [\"SP6JOE\", \"NX5M\"], [\"SP6JOE\", \"K5WA\"], [\"SP6JOE\", \"K5WA\"], [\"SP6JOE\", \"W5AL\"], [\"SP6JOE\", \"W5AL\"], [\"SP6JOE\", \"N5T\"], [\"SP6JOE\", \"N5T\"], [\"SP6JOE\", \"N5T\"], [\"SP6JOE\", \"N5T\"], [\"SP6JOE\", \"N5YA\"], [\"SP6JOE\", \"N5YA\"], [\"SP6JOE\", \"WA8ZBT\"], [\"SP6JOE\", \"WA8ZBT\"], [\"SP6JOE\", \"KG5OWB\"], [\"SP6JOE\", \"KG5OWB\"], [\"SP6JOE\", \"KE5C\"], [\"SP6JOE\", \"KE5C\"], [\"VA3FN\", \"K5CM\"], [\"VA3FN\", \"K5CM\"], [\"VA3FN\", \"K5CM\"], [\"VA3FN\", \"K5CM\"], [\"VA4JS\", \"KC4EEL\"], [\"VA4JS\", \"KC4EEL\"], [\"VA4JS\", \"KC4EEL\"], [\"VA4JS\", \"KC4EEL\"], [\"VA4JS\", \"KC6UCN\"], [\"VA4JS\", \"KC6UCN\"], [\"VA6AGR\", \"WA5DTK\"], [\"VA6AGR\", \"WA5DTK\"], [\"VA6RCN\", \"AD4EB\"], [\"VA6RCN\", \"AD4EB\"], [\"VE1RGO\", \"W5LO\"], [\"VE1RGO\", \"W5LO\"], [\"VE2FK\", \"KG5OWB\"], [\"VE2FK\", \"KG5OWB\"], [\"VE2FK\", \"KG5VK\"], [\"VE2FK\", \"KG5VK\"], [\"VE3DQN\", \"K5WW\"], [\"VE3DQN\", \"K5WW\"], [\"VE3KP\", \"WA5DTK\"], [\"VE3KP\", \"WA5DTK\"], [\"VE3RQ\", \"KJ5IEL\"], [\"VE3RQ\", \"KJ5IEL\"], [\"VE3RQ\", \"AD4EB\"], [\"VE3RQ\", \"AD4EB\"], [\"VE3YT\", \"KF5YUB\"], [\"VE3YT\", \"KF5YUB\"], [\"VE3YT\", \"N5KW\"], [\"VE3YT\", \"N5KW\"], [\"VE3YT\", \"AD4EB\"], [\"VE3YT\", \"AD4EB\"], [\"VE3YT\", \"AD4EB\"], [\"VE3YT\", \"AD4EB\"], [\"VE3YT\", \"AD4EB\"], [\"VE3YT\", \"AD4EB\"], [\"VE7SCC\", \"N5NA\"], [\"VE7SCC\", \"N5NA\"], [\"VE7SCC\", \"KF5YUB\"], [\"VE7SCC\", \"KF5YUB\"], [\"VE9CF\", \"KF5YUB\"], [\"VE9CF\", \"KF5YUB\"], [\"VE9CF\", \"KC6UCN\"], [\"VE9CF\", \"KC6UCN\"], [\"VE9CF\", \"W5PTX\"], [\"VE9CF\", \"W5PTX\"], [\"VE9RLW\", \"WA5JMZ\"], [\"VE9RLW\", \"WA5JMZ\"], [\"VE9RLW\", \"W5NC\"], [\"VE9RLW\", \"W5NC\"], [\"W0PI\", \"N5KW\"], [\"W0PI\", \"N5KW\"], [\"W0PI\", \"N5KW\"], [\"W0PI\", \"N5KW\"], [\"W0UC\", \"KT3X\"], [\"W0UC\", \"KT3X\"], [\"W0UC\", \"KT3X\"], [\"W0UC\", \"KT3X\"], [\"W0UC\", \"KT3X\"], [\"W0UC\", \"KT3X\"], [\"W0UC\", \"AA5AH\"], [\"W0UC\", \"AA5AH\"], [\"W0UC\", \"KI5GNH\"], [\"W0UC\", \"KI5GNH\"], [\"W0UC\", \"WA5DCT\"], [\"W0UC\", \"WA5DCT\"], [\"W0UC\", \"WA5LFD\"], [\"W0UC\", \"WA5LFD\"], [\"W0UC\", \"N5NA\"], [\"W0UC\", \"N5NA\"], [\"W0VX\", \"N0TT\"], [\"W0VX\", \"N0TT\"], [\"W0VX\", \"KM8L\"], [\"W0VX\", \"KM8L\"], [\"W0VX\", \"W5ESE\"], [\"W0VX\", \"W5ESE\"], [\"W0VX\", \"N2OIG\"], [\"W0VX\", \"N2OIG\"], [\"W0VX\", \"F8PDR\"], [\"W0VX\", \"F8PDR\"], [\"W0VX\", \"W5GCX\"], [\"W0VX\", \"W5GCX\"], [\"W0VX\", \"N5VBP\"], [\"W0VX\", \"N5VBP\"], [\"W0VX\", \"K1ORY\"], [\"W0VX\", \"K1ORY\"], [\"W1QK\", \"KK5TY\"], [\"W1QK\", \"KK5TY\"], [\"W2TB\", \"KK5TY\"], [\"W2TB\", \"KK5TY\"], [\"W2TB\", \"KT3X\"], [\"W2TB\", \"KT3X\"], [\"W2TB\", \"KT3X\"], [\"W2TB\", \"KT3X\"], [\"W2TB\", \"KT3X\"], [\"W2TB\", \"KT3X\"], [\"W2TB\", \"AD4EB\"], [\"W2TB\", \"AD4EB\"], [\"W2TB\", \"AD4EB\"], [\"W2TB\", \"AD4EB\"], [\"W2TB\", \"AD4EB\"], [\"W2TB\", \"AD4EB\"], [\"W4CHI\", \"W5NC\"], [\"W4CHI\", \"W5NC\"], [\"W4CHI\", \"K5CM\"], [\"W4CHI\", \"K5CM\"], [\"W4EE\", \"W5ACQ\"], [\"W4EE\", \"W5ACQ\"], [\"W4SSF\", \"W5LXS\"], [\"W4SSF\", \"W5LXS\"], [\"W4SSF\", \"K5K\"], [\"W4SSF\", \"K5K\"], [\"W4SSF\", \"K5K\"], [\"W4SSF\", \"K5K\"], [\"W4SSF\", \"K5T\"], [\"W4SSF\", \"K5T\"], [\"W4SSF\", \"W5JK\"], [\"W4SSF\", \"W5JK\"], [\"W4SSF\", \"KG5IEE\"], [\"W4SSF\", \"KG5IEE\"], [\"W5ACQ\", \"KW4EE\"], [\"W5ACQ\", \"KW4EE\"], [\"W5ACQ\", \"F8PDR\"], [\"W5ACQ\", \"F8PDR\"], [\"W5ACQ\", \"AA3R\"], [\"W5ACQ\", \"AA3R\"], [\"W5ACQ\", \"AA3R\"], [\"W5ACQ\", \"AA3R\"], [\"W5ACQ\", \"K1ORY\"], [\"W5ACQ\", \"K1ORY\"], [\"W5ACQ\", \"NW7DX\"], [\"W5ACQ\", \"NW7DX\"], [\"W5ACQ\", \"K3YDX\"], [\"W5ACQ\", \"K3YDX\"], [\"W5ACQ\", \"W4EE\"], [\"W5ACQ\", \"W4EE\"], [\"W5ACQ\", \"KG5OWB\"], [\"W5ACQ\", \"KG5OWB\"], [\"W5ACQ\", \"K0TRL\"], [\"W5ACQ\", \"K0TRL\"], [\"W5ACQ\", \"AA3R\"], [\"W5ACQ\", \"AA3R\"], [\"W5ACQ\", \"N5RZ\"], [\"W5ACQ\", \"N5RZ\"], [\"W5ACQ\", \"AD4EB\"], [\"W5ACQ\", \"AD4EB\"], [\"W5AJ\", \"K5WA\"], [\"W5AJ\", \"K5WA\"], [\"W5AL\", \"W5ESE\"], [\"W5AL\", \"W5ESE\"], [\"W5AL\", \"F8PDR\"], [\"W5AL\", \"F8PDR\"], [\"W5CUB\", \"KU8E\"], [\"W5CUB\", \"KU8E\"], [\"W5ESE\", \"W5AL\"], [\"W5ESE\", \"W5AL\"], [\"W5ESE\", \"K5QQ\"], [\"W5ESE\", \"K5QQ\"], [\"W5ESE\", \"W0VX\"], [\"W5ESE\", \"W0VX\"], [\"W5ESE\", \"DL3DXX\"], [\"W5ESE\", \"DL3DXX\"], [\"W5ESE\", \"N5YA\"], [\"W5ESE\", \"N5YA\"], [\"W5ESE\", \"AA3R\"], [\"W5ESE\", \"AA3R\"], [\"W5ESE\", \"OM2VL\"], [\"W5ESE\", \"OM2VL\"], [\"W5GCX\", \"W5LIC\"], [\"W5GCX\", \"W5LIC\"], [\"W5GCX\", \"WA5JMZ\"], [\"W5GCX\", \"WA5JMZ\"], [\"W5GCX\", \"WA5DTK\"], [\"W5GCX\", \"WA5DTK\"], [\"W5GCX\", \"K5WA\"], [\"W5GCX\", \"K5WA\"], [\"W5GCX\", \"K2WJ\"], [\"W5GCX\", \"K2WJ\"], [\"W5GCX\", \"KK5TY\"], [\"W5GCX\", \"KK5TY\"], [\"W5GCX\", \"W0VX\"], [\"W5GCX\", \"W0VX\"], [\"W5GCX\", \"N5TJ\"], [\"W5GCX\", \"N5TJ\"], [\"W5GCX\", \"K5TIA\"], [\"W5GCX\", \"K5TIA\"], [\"W5GCX\", \"AD4EB\"], [\"W5GCX\", \"AD4EB\"], [\"W5GCX\", \"WA8ZBT\"], [\"W5GCX\", \"WA8ZBT\"], [\"W5GCX\", \"KG5IEE\"], [\"W5GCX\", \"KG5IEE\"], [\"W5GCX\", \"W5NC\"], [\"W5GCX\", \"W5NC\"], [\"W5GCX\", \"KG5OWB\"], [\"W5GCX\", \"KG5OWB\"], [\"W5GCX\", \"W5JK\"], [\"W5GCX\", \"W5JK\"], [\"W5GCX\", \"K5IZO\"], [\"W5GCX\", \"K5IZO\"], [\"W5GCX\", \"WA5DTK\"], [\"W5GCX\", \"WA5DTK\"], [\"W5GCX\", \"KG5VK\"], [\"W5GCX\", \"KG5VK\"], [\"W5HI\", \"WA3AER\"], [\"W5HI\", \"WA3AER\"], [\"W5JK\", \"F8PDR\"], [\"W5JK\", \"F8PDR\"], [\"W5JK\", \"KJ9C\"], [\"W5JK\", \"KJ9C\"], [\"W5JK\", \"AI4DB\"], [\"W5JK\", \"AI4DB\"], [\"W5JK\", \"W5GCX\"], [\"W5JK\", \"W5GCX\"], [\"W5JK\", \"K5RJM\"], [\"W5JK\", \"K5RJM\"], [\"W5JK\", \"F8PDR\"], [\"W5JK\", \"F8PDR\"], [\"W5KU\", \"N5NA\"], [\"W5KU\", \"N5NA\"], [\"W5KU\", \"N5NU\"], [\"W5KU\", \"N5NU\"], [\"W5KU\", \"K1ORY\"], [\"W5KU\", \"K1ORY\"], [\"W5KU\", \"N0TT\"], [\"W5KU\", \"N0TT\"], [\"W5KU\", \"F8PDR\"], [\"W5KU\", \"F8PDR\"], [\"W5LIC\", \"N5SLY\"], [\"W5LIC\", \"N5SLY\"], [\"W5LIC\", \"K5QHD\"], [\"W5LIC\", \"K5QHD\"], [\"W5LO\", \"VE1RGO\"], [\"W5LO\", \"VE1RGO\"], [\"W5LO\", \"KJ9C\"], [\"W5LO\", \"KJ9C\"], [\"W5LO\", \"N7EPD\"], [\"W5LO\", \"N7EPD\"], [\"W5LO\", \"N5DTT\"], [\"W5LO\", \"N5DTT\"], [\"W5LXS\", \"N9GXA\"], [\"W5LXS\", \"N9GXA\"], [\"W5LXS\", \"WB2PJH\"], [\"W5LXS\", \"WB2PJH\"], [\"W5LXS\", \"K2KAR\"], [\"W5LXS\", \"K2KAR\"], [\"W5LXS\", \"K5IZO\"], [\"W5LXS\", \"K5IZO\"], [\"W5LXS\", \"WB2PJH\"], [\"W5LXS\", \"WB2PJH\"], [\"W5LXS\", \"WB2WPM\"], [\"W5LXS\", \"WB2WPM\"], [\"W5NC\", \"WA5DTK\"], [\"W5NC\", \"WA5DTK\"], [\"W5NC\", \"K5K\"], [\"W5NC\", \"K5K\"], [\"W5NC\", \"K5K\"], [\"W5NC\", \"K5K\"], [\"W5NC\", \"K2MN\"], [\"W5NC\", \"K2MN\"], [\"W5NC\", \"K0RJK\"], [\"W5NC\", \"K0RJK\"], [\"W5NC\", \"K3TD\"], [\"W5NC\", \"K3TD\"], [\"W5NC\", \"W5GCX\"], [\"W5NC\", \"W5GCX\"], [\"W5NC\", \"W6AFA\"], [\"W5NC\", \"W6AFA\"], [\"W5NC\", \"KT3X\"], [\"W5NC\", \"KT3X\"], [\"W5NC\", \"N5KW\"], [\"W5NC\", \"N5KW\"], [\"W5NC\", \"AD4EB\"], [\"W5NC\", \"AD4EB\"], [\"W5NC\", \"K8MV\"], [\"W5NC\", \"K8MV\"], [\"W6AFA\", \"KI5GNH\"], [\"W6AFA\", \"KI5GNH\"], [\"W6AFA\", \"NX5M\"], [\"W6AFA\", \"NX5M\"], [\"W6AFA\", \"KE5ZPP\"], [\"W6AFA\", \"KE5ZPP\"], [\"W6AFA\", \"W5NC\"], [\"W6AFA\", \"W5NC\"], [\"W6ECK\", \"W5NC\"], [\"W6ECK\", \"W5NC\"], [\"W7GF\", \"K5CM\"], [\"W7GF\", \"K5CM\"], [\"W7LG\", \"K5WA\"], [\"W7LG\", \"K5WA\"], [\"W7LG\", \"N5XZ\"], [\"W7LG\", \"N5XZ\"], [\"W8OV\", \"W5JK\"], [\"W8OV\", \"W5JK\"], [\"W8OV\", \"AI5G\"], [\"W8OV\", \"AI5G\"], [\"W8PI\", \"K5EC\"], [\"W8PI\", \"K5EC\"], [\"W8PI\", \"AD4EB\"], [\"W8PI\", \"AD4EB\"], [\"W9QL\", \"N5NA\"], [\"W9QL\", \"N5NA\"], [\"W9QL\", \"WA5LFD\"], [\"W9QL\", \"WA5LFD\"], [\"W9QL\", \"AD4EB\"], [\"W9QL\", \"AD4EB\"], [\"W9WE\", \"N5XZ\"], [\"W9WE\", \"N5XZ\"], [\"WA2JQK\", \"W5NC\"], [\"WA2JQK\", \"W5NC\"], [\"WA2JQK\", \"K5ECT\"], [\"WA2JQK\", \"K5ECT\"], [\"WA2JQK\", \"N5KW\"], [\"WA2JQK\", \"N5KW\"], [\"WA2JQK\", \"N5NU\"], [\"WA2JQK\", \"N5NU\"], [\"WA2JQK\", \"K5CM\"], [\"WA2JQK\", \"K5CM\"], [\"WA2JQK\", \"K5CM\"], [\"WA2JQK\", \"K5CM\"], [\"WA2JQK\", \"W5NC\"], [\"WA2JQK\", \"W5NC\"], [\"WA2JQK\", \"K5CM\"], [\"WA2JQK\", \"K5CM\"], [\"WA2QAU\", \"NU5DE\"], [\"WA2QAU\", \"NU5DE\"], [\"WA2QAU\", \"K5ECT\"], [\"WA2QAU\", \"K5ECT\"], [\"WA2QAU\", \"WA5DTK\"], [\"WA2QAU\", \"WA5DTK\"], [\"WA3AAN\", \"K5OT\"], [\"WA3AAN\", \"K5OT\"], [\"WA3AAN\", \"N5JJ\"], [\"WA3AAN\", \"N5JJ\"], [\"WA3AER\", \"NX5M\"], [\"WA3AER\", \"NX5M\"], [\"WA3AER\", \"W5NC\"], [\"WA3AER\", \"W5NC\"], [\"WA3AER\", \"W5NC\"], [\"WA3AER\", \"W5NC\"], [\"WA3AER\", \"W5HI\"], [\"WA3AER\", \"W5HI\"], [\"WA4GMW\", \"K5QHD\"], [\"WA4GMW\", \"K5QHD\"], [\"WA5CKF\", \"NU5M\"], [\"WA5CKF\", \"NU5M\"], [\"WA5CKF\", \"NU5DE\"], [\"WA5CKF\", \"NU5DE\"], [\"WA5CKF\", \"N5IT\"], [\"WA5CKF\", \"N5IT\"], [\"WA5CKF\", \"N6OKU\"], [\"WA5CKF\", \"N6OKU\"], [\"WA5CKF\", \"KE5OBS\"], [\"WA5CKF\", \"KE5OBS\"], [\"WA5CKF\", \"KE5OBS\"], [\"WA5CKF\", \"KE5OBS\"], [\"WA5CKF\", \"NE5B\"], [\"WA5CKF\", \"NE5B\"], [\"WA5CKF\", \"NE5B\"], [\"WA5CKF\", \"NE5B\"], [\"WA5CKF\", \"NE5B\"], [\"WA5CKF\", \"NE5B\"], [\"WA5CKF\", \"NE5B\"], [\"WA5CKF\", \"NE5B\"], [\"WA5CKF\", \"NX5M\"], [\"WA5CKF\", \"NX5M\"], [\"WA5CKF\", \"WA5DTK\"], [\"WA5CKF\", \"WA5DTK\"], [\"WA5DCT\", \"NW5Q\"], [\"WA5DCT\", \"NW5Q\"], [\"WA5DCT\", \"W5LIC\"], [\"WA5DCT\", \"W5LIC\"], [\"WA5DCT\", \"K0YY\"], [\"WA5DCT\", \"K0YY\"], [\"WA5DCT\", \"K5QHD\"], [\"WA5DCT\", \"K5QHD\"], [\"WA5DCT\", \"N5DN\"], [\"WA5DCT\", \"N5DN\"], [\"WA5DCT\", \"N6MDV\"], [\"WA5DCT\", \"N6MDV\"], [\"WA5DCT\", \"W0UC\"], [\"WA5DCT\", \"W0UC\"], [\"WA5DCT\", \"AG5T\"], [\"WA5DCT\", \"AG5T\"], [\"WA5DSS\", \"KI5NCJ\"], [\"WA5DSS\", \"KI5NCJ\"], [\"WA5DTK\", \"K5T\"], [\"WA5DTK\", \"K5T\"], [\"WA5DTK\", \"K5T\"], [\"WA5DTK\", \"K5T\"], [\"WA5DTK\", \"N5NA\"], [\"WA5DTK\", \"N5NA\"], [\"WA5DTK\", \"W5NC\"], [\"WA5DTK\", \"W5NC\"], [\"WA5DTK\", \"AI5OL\"], [\"WA5DTK\", \"AI5OL\"], [\"WA5DTK\", \"NZ5X\"], [\"WA5DTK\", \"NZ5X\"], [\"WA5DTK\", \"W5GCX\"], [\"WA5DTK\", \"W5GCX\"], [\"WA5DTK\", \"WA5CKF\"], [\"WA5DTK\", \"WA5CKF\"], [\"WA5DTK\", \"K5B\"], [\"WA5DTK\", \"K5B\"], [\"WA5DTK\", \"K5B\"], [\"WA5DTK\", \"K5B\"], [\"WA5DTK\", \"KT3X\"], [\"WA5DTK\", \"KT3X\"], [\"WA5DTK\", \"AA3R\"], [\"WA5DTK\", \"AA3R\"], [\"WA5DTK\", \"K0AE\"], [\"WA5DTK\", \"K0AE\"], [\"WA5DTK\", \"W5AL\"], [\"WA5DTK\", \"W5AL\"], [\"WA5DTK\", \"K4BAI\"], [\"WA5DTK\", \"K4BAI\"], [\"WA5DTK\", \"KA0PQW\"], [\"WA5DTK\", \"KA0PQW\"], [\"WA5DTK\", \"K2KAR\"], [\"WA5DTK\", \"K2KAR\"], [\"WA5DTK\", \"AA3R\"], [\"WA5DTK\", \"AA3R\"], [\"WA5DTK\", \"K8RGI\"], [\"WA5DTK\", \"K8RGI\"], [\"WA5DTK\", \"AA3R\"], [\"WA5DTK\", \"AA3R\"], [\"WA5DTK\", \"KE3LA\"], [\"WA5DTK\", \"KE3LA\"], [\"WA5DTK\", \"AC6ZM\"], [\"WA5DTK\", \"AC6ZM\"], [\"WA5DTK\", \"K5T\"], [\"WA5DTK\", \"K5T\"], [\"WA5DTK\", \"W5JK\"], [\"WA5DTK\", \"W5JK\"], [\"WA5DTK\", \"KJ5IEL\"], [\"WA5DTK\", \"KJ5IEL\"], [\"WA5DTK\", \"K8MFO\"], [\"WA5DTK\", \"K8MFO\"], [\"WA5DTK\", \"W5GCX\"], [\"WA5DTK\", \"W5GCX\"], [\"WA5DTK\", \"K8MV\"], [\"WA5DTK\", \"K8MV\"], [\"WA5DTK\", \"KZ3P\"], [\"WA5DTK\", \"KZ3P\"], [\"WA5DTK\", \"NA4J\"], [\"WA5DTK\", \"NA4J\"], [\"WA5DTK\", \"WO4O\"], [\"WA5DTK\", \"WO4O\"], [\"WA5DTK\", \"K2KAR\"], [\"WA5DTK\", \"K2KAR\"], [\"WA5JMZ\", \"K0YY\"], [\"WA5JMZ\", \"K0YY\"], [\"WA5JMZ\", \"N5SLY\"], [\"WA5JMZ\", \"N5SLY\"], [\"WA5JMZ\", \"K5QHD\"], [\"WA5JMZ\", \"K5QHD\"], [\"WA5JMZ\", \"K8MV\"], [\"WA5JMZ\", \"K8MV\"], [\"WA5JMZ\", \"VE9RLW\"], [\"WA5JMZ\", \"VE9RLW\"], [\"WA5LFD\", \"W9QL\"], [\"WA5LFD\", \"W9QL\"], [\"WA5LFD\", \"AD4EB\"], [\"WA5LFD\", \"AD4EB\"], [\"WA5LFD\", \"DL5AXX\"], [\"WA5LFD\", \"DL5AXX\"], [\"WA5SOG\", \"N5YA\"], [\"WA5SOG\", \"N5YA\"], [\"WA5SOG\", \"K5K\"], [\"WA5SOG\", \"K5K\"], [\"WA5SOG\", \"AD4EB\"], [\"WA5SOG\", \"AD4EB\"], [\"WA5SOG\", \"AD4EB\"], [\"WA5SOG\", \"AD4EB\"], [\"WA6KHK\", \"W5ACQ\"], [\"WA6KHK\", \"W5ACQ\"], [\"WA6KHK\", \"N5T\"], [\"WA6KHK\", \"N5T\"], [\"WA6KHK\", \"N5NA\"], [\"WA6KHK\", \"N5NA\"], [\"WA6KHK\", \"WA5DTK\"], [\"WA6KHK\", \"WA5DTK\"], [\"WA6KHK\", \"KT3X\"], [\"WA6KHK\", \"KT3X\"], [\"WA6KHK\", \"K5ECT\"], [\"WA6KHK\", \"K5ECT\"], [\"WA8ZBT\", \"K5EC\"], [\"WA8ZBT\", \"K5EC\"], [\"WA8ZBT\", \"WA5CKF\"], [\"WA8ZBT\", \"WA5CKF\"], [\"WA8ZBT\", \"W5GCX\"], [\"WA8ZBT\", \"W5GCX\"], [\"WA8ZBT\", \"N5YA\"], [\"WA8ZBT\", \"N5YA\"], [\"WA8ZBT\", \"F8PDR\"], [\"WA8ZBT\", \"F8PDR\"], [\"WA9LEY\", \"KG5LJZ\"], [\"WA9LEY\", \"KG5LJZ\"], [\"WA9LEY\", \"AJ4F\"], [\"WA9LEY\", \"AJ4F\"], [\"WB2PJH\", \"W5LXS\"], [\"WB2PJH\", \"W5LXS\"], [\"WB2PJH\", \"W5LXS\"], [\"WB2PJH\", \"W5LXS\"], [\"WB2WPM\", \"KK5TY\"], [\"WB2WPM\", \"KK5TY\"], [\"WB2WPM\", \"AD4EB\"], [\"WB2WPM\", \"AD4EB\"], [\"WB2WPM\", \"K5T\"], [\"WB2WPM\", \"K5T\"], [\"WB2WPM\", \"N5RZ\"], [\"WB2WPM\", \"N5RZ\"], [\"WB2WPM\", \"AD4EB\"], [\"WB2WPM\", \"AD4EB\"], [\"WB5BKL\", \"AD4EB\"], [\"WB5BKL\", \"AD4EB\"], [\"WB5BKL\", \"AA3R\"], [\"WB5BKL\", \"AA3R\"], [\"WB5BKL\", \"K5OT\"], [\"WB5BKL\", \"K5OT\"], [\"WB5BKL\", \"K0PC\"], [\"WB5BKL\", \"K0PC\"], [\"WB5BKL\", \"KT3X\"], [\"WB5BKL\", \"KT3X\"], [\"WB5BKL\", \"KG5VK\"], [\"WB5BKL\", \"KG5VK\"], [\"WB5BKL\", \"AA3R\"], [\"WB5BKL\", \"AA3R\"], [\"WB5BKL\", \"K0JV\"], [\"WB5BKL\", \"K0JV\"], [\"WB8ASI\", \"N5NA\"], [\"WB8ASI\", \"N5NA\"], [\"WB8ASI\", \"K5CM\"], [\"WB8ASI\", \"K5CM\"], [\"WB9HFK\", \"K5QHD\"], [\"WB9HFK\", \"K5QHD\"], [\"WB9HFK\", \"KK5TY\"], [\"WB9HFK\", \"KK5TY\"], [\"WB9HFK\", \"N5XZ\"], [\"WB9HFK\", \"N5XZ\"], [\"WB9HFK\", \"K5ECT\"], [\"WB9HFK\", \"K5ECT\"], [\"WB9RCE\", \"N5T\"], [\"WB9RCE\", \"N5T\"], [\"WB9RCE\", \"N5T\"], [\"WB9RCE\", \"N5T\"], [\"WJ9O\", \"KI5NCJ\"], [\"WJ9O\", \"KI5NCJ\"], [\"WN7Y\", \"W5JK\"], [\"WN7Y\", \"W5JK\"], [\"WN7Y\", \"KK5TY\"], [\"WN7Y\", \"KK5TY\"], [\"WN7Y\", \"K5CM\"], [\"WN7Y\", \"K5CM\"], [\"WO4O\", \"K5QHD\"], [\"WO4O\", \"K5QHD\"], [\"WO4O\", \"K5TIA\"], [\"WO4O\", \"K5TIA\"], [\"WO4O\", \"K5ECT\"], [\"WO4O\", \"K5ECT\"], [\"WO4O\", \"WA5DCT\"], [\"WO4O\", \"WA5DCT\"], [\"WO9B\", \"WA5DTK\"], [\"WO9B\", \"WA5DTK\"], [\"WQ6X\", \"AD4EB\"], [\"WQ6X\", \"AD4EB\"], [\"WU8T\", \"K5CM\"], [\"WU8T\", \"K5CM\"], [\"WU8T\", \"KG5VK\"], [\"WU8T\", \"KG5VK\"], [\"WU8T\", \"N5XZ\"], [\"WU8T\", \"N5XZ\"], [\"WU8T\", \"N5XZ\"], [\"WU8T\", \"N5XZ\"], [\"WU8T\", \"W5JK\"], [\"WU8T\", \"W5JK\"], [\"WU8T\", \"AD4EB\"], [\"WU8T\", \"AD4EB\"], [\"WU8T\", \"NU5DE\"], [\"WU8T\", \"NU5DE\"], [\"WU8T\", \"AD4EB\"], [\"WU8T\", \"AD4EB\"], [\"WV4P\", \"KI5GNH\"], [\"WV4P\", \"KI5GNH\"], [\"WV4P\", \"K5TIA\"], [\"WV4P\", \"K5TIA\"], [\"WV4P\", \"AD4EB\"], [\"WV4P\", \"AD4EB\"], [\"WV4P\", \"AD4EB\"], [\"WV4P\", \"AD4EB\"], [\"WV4P\", \"K5T\"], [\"WV4P\", \"K5T\"], [\"WV4P\", \"W5JK\"], [\"WV4P\", \"W5JK\"], [\"WV4P\", \"AD4EB\"], [\"WV4P\", \"AD4EB\"], [\"WW5L\", \"N5JJ\"], [\"WW5L\", \"N5JJ\"], [\"WX5LOK\", \"KC4EEL\"], [\"WX5LOK\", \"KC4EEL\"], [\"WX5LOK\", \"KC4EEL\"], [\"WX5LOK\", \"KC4EEL\"], [\"WX5LOK\", \"K5CM\"], [\"WX5LOK\", \"K5CM\"], [\"WX8C\", \"KT3X\"], [\"WX8C\", \"KT3X\"], [\"WX8C\", \"KT3X\"], [\"WX8C\", \"KT3X\"], [\"WX8C\", \"KT3X\"], [\"WX8C\", \"KT3X\"], [\"WX8C\", \"N5KW\"], [\"WX8C\", \"N5KW\"], [\"WX8C\", \"N5KW\"], [\"WX8C\", \"N5KW\"]]", "busted_calls": "[[\"WA5DTK\", \"AD4EB\"], [\"WA5DTK\", \"AD4EB\"], [\"WA2JQK\", \"AD4EB\"], [\"K0SV\", \"AD4EB\"], [\"K0SV\", \"AD4EB\"], [\"AD4EB\", \"K0SV\"], [\"N5JJ\", \"K0SV\"], [\"AD4EB\", \"K0SV\"], [\"N5RZ\", \"K0YY\"], [\"N5IT\", \"K0YY\"], [\"W5LIC\", \"K0YY\"], [\"K5EC\", \"K0YY\"], [\"K5EC\", \"K0YY\"], [\"N5DN\", \"K0YY\"], [\"N5NA\", \"K0YY\"], [\"N5NA\", \"K0YY\"], [\"KT3X\", \"K2HT\"], [\"KT3X\", \"K2HT\"], [\"K5K\", \"K2QB\"], [\"K5K\", \"K2QB\"], [\"N5XZ\", \"K4ZGB\"], [\"ND0C\", \"K5CM\"], [\"ND0C\", \"K5CM\"], [\"K0YY\", \"K5EC\"], [\"K0YY\", \"K5EC\"], [\"K8MV\", \"K5EC\"], [\"KN6VTC\", \"K5EC\"], [\"WA5DCT\", \"K5EC\"], [\"WA5DCT\", \"K5EC\"], [\"W5CUB\", \"K5ECT\"], [\"KG5IEE\", \"K5IZO\"], [\"K2QB\", \"K5K\"], [\"K2QB\", \"K5K\"], [\"W8PI\", \"K5K\"], [\"W8PI\", \"K5K\"], [\"K8MV\", \"K5K\"], [\"K8MV\", \"K5K\"], [\"N5VBL\", \"K5K\"], [\"KC4EEL\", \"K5K\"], [\"KC4EEL\", \"K5K\"], [\"KF5VDX\", \"K5UBE\"], [\"NX5M\", \"K5UBE\"], [\"NX5M\", \"K5UBE\"], [\"NX5M\", \"K6KQV\"], [\"W5NC\", \"K6KQV\"], [\"K5K\", \"K8MV\"], [\"K5K\", \"K8MV\"], [\"K5EC\", \"K8MV\"], [\"KE5OBS\", \"KC4EEL\"], [\"KE5OBS\", \"KC4EEL\"], [\"K5K\", \"KC4EEL\"], [\"K5K\", \"KC4EEL\"], [\"N5YA\", \"KE3LA\"], [\"WJ9O\", \"KE5OBS\"], [\"WJ9O\", \"KE5OBS\"], [\"KC4EEL\", \"KE5OBS\"], [\"KC4EEL\", \"KE5OBS\"], [\"K5UBE\", \"KF5VDX\"], [\"WB5BKL\", \"KG5IEE\"], [\"K5IZO\", \"KG5IEE\"], [\"W4YE\", \"KG5OWB\"], [\"NV4T\", \"KI5GNH\"], [\"N5WCT\", \"KJ5T\"], [\"W5LIC\", \"KJ5T\"], [\"KT3X\", \"KN4JN\"], [\"K5EC\", \"KN6VTC\"], [\"KN4JN\", \"KT3X\"], [\"N1LN\", \"KT3X\"], [\"WB9HFK\", \"KT3X\"], [\"WB9HFK\", \"KT3X\"], [\"K2HT\", \"KT3X\"], [\"K2HT\", \"KT3X\"], [\"WB8ASI\", \"KT3X\"], [\"WB8ASI\", \"KT3X\"], [\"WB8ASI\", \"KT3X\"], [\"N5T\", \"N0IIL\"], [\"KT3X\", \"N1LN\"], [\"K0YY\", \"N5DN\"], [\"N7AME\", \"N5DN\"], [\"W5CUB\", \"N5EP\"], [\"K0YY\", \"N5IT\"], [\"K0SV\", \"N5JJ\"], [\"WB9HFK\", \"N5NA\"], [\"K0YY\", \"N5NA\"], [\"K0YY\", \"N5NA\"], [\"WB9HFK\", \"N5NU\"], [\"N8II\", \"N5PBP\"], [\"SP6JOE\", \"N5RZ\"], [\"N0IIL\", \"N5T\"], [\"W5NC\", \"N5T\"], [\"K5K\", \"N5VBL\"], [\"NE5B\", \"N5WCT\"], [\"KJ5T\", \"N5WCT\"], [\"KE3LA\", \"N5YA\"], [\"NE5B\", \"N6TQ\"], [\"N5DN\", \"N7AME\"], [\"N5PBP\", \"N8II\"], [\"N5WCT\", \"N8II\"], [\"K5CM\", \"ND0C\"], [\"K5CM\", \"ND0C\"], [\"N5WCT\", \"NE5B\"], [\"WJ9O\", \"NE5B\"], [\"K6KQV\", \"NX5M\"], [\"K5UBE\", \"NX5M\"], [\"K5UBE\", \"NX5M\"], [\"AJ4F\", \"W4YE\"], [\"KG5OWB\", \"W4YE\"], [\"K5ECT\", \"W5CUB\"], [\"N5EP\", \"W5CUB\"], [\"WJ9O\", \"W5LIC\"], [\"KJ5T\", \"W5LIC\"], [\"K6KQV\", \"W5NC\"], [\"N5T\", \"W5NC\"], [\"K5K\", \"W8PI\"], [\"K5K\", \"W8PI\"], [\"W0VX\", \"WA2JQK\"], [\"AD4EB\", \"WA2JQK\"], [\"K5EC\", \"WA5DCT\"], [\"K5EC\", \"WA5DCT\"], [\"AD4EB\", \"WA5DTK\"], [\"AD4EB\", \"WA5DTK\"], [\"KG5IEE\", \"WB5BKL\"], [\"KT3X\", \"WB8ASI\"], [\"KT3X\", \"WB8ASI\"], [\"KT3X\", \"WB8ASI\"], [\"KT3X\", \"WB9HFK\"], [\"KT3X\", \"WB9HFK\"], [\"N5NA\", \"WB9HFK\"], [\"N5NU\", \"WB9HFK\"], [\"NE5B\", \"WJ9O\"], [\"N5IT\", \"WJ9O\"], [\"W5LIC\", \"WJ9O\"], [\"KE5OBS\", \"WJ9O\"], [\"KE5OBS\", \"WJ9O\"]]", "qsos_by_band": "{\"160\": 2, \"80\": 565, \"40\": 15001, \"20\": 30564, \"15\": 3476, \"10\": 65, \"6\": 0, \"2\": 44}", "qsos_by_mode": "{\"PH\": 18021, \"CW\": 31432, \"RY\": 39, \"DG\": 225, \"FM\": 0}", "mobile_activation_counts": "{\"MARI\": 48, \"PPIN\": 442, \"STEP\": 463, \"EAST\": 86, \"HRSN\": 110, \"CHER\": 100, \"DENT\": 675, \"COOK\": 301, \"CALL\": 44, \"PANO\": 94, \"RUSK\": 80, \"DELT\": 731, \"FANN\": 360, \"HUNT\": 410, \"HOPK\": 715, \"RBSN\": 118, \"MADI\": 140, \"LEON\": 140, \"FRAN\": 353, \"WEBB\": 128, \"JHOG\": 104, \"ZAPA\": 100, \"UPSH\": 250, \"WOOD\": 244, \"MONT\": 156, \"ECTO\": 122, \"CLAY\": 132, \"WINK\": 124, \"ARCH\": 86, \"WICH\": 194, \"HDMN\": 124, \"CAMP\": 154, \"CHIL\": 88, \"WALK\": 90, \"MIDL\": 76, \"LAMA\": 207, \"BOWI\": 297, \"CASS\": 372, \"DAWS\": 82, \"LEE\": 85, \"FAYE\": 10, \"MART\": 100, \"RAIN\": 114, \"TRIN\": 72, \"LAVA\": 42, \"TITU\": 257, \"RRIV\": 145, \"MORR\": 245, \"BZOS\": 130, \"GREG\": 84, \"SMIT\": 102, \"VZAN\": 98, \"COKE\": 70, \"KAUF\": 110, \"WILY\": 84, \"STER\": 90, \"ROCK\": 142, \"GLAS\": 106, \"DALS\": 146, \"COLN\": 130, \"NACO\": 216, \"BROO\": 76, \"TARR\": 54, \"WISE\": 244, \"ANDR\": 66, \"WILB\": 128, \"WARD\": 92, \"PECO\": 80, \"CRAN\": 68, \"CROC\": 70, \"HALL\": 130, \"COLW\": 84, \"UPTO\": 88, \"DONL\": 128, \"ARMS\": 124, \"MGMY\": 40, \"RAND\": 154, \"CARS\": 152, \"POTT\": 156, \"REAG\": 94, \"SJAC\": 66, \"BORD\": 84, \"FISH\": 66, \"CMRN\": 74, \"HIDA\": 80, \"DUVA\": 74, \"JWEL\": 64, \"LIVO\": 86, \"MMUL\": 84, \"VICT\": 52, \"JKSN\": 24, \"HOUS\": 70, \"LIBE\": 28, \"PARK\": 62, \"SHAC\": 64, \"BEE\": 76, \"GOLI\": 76, \"SCUR\": 48, \"RUNN\": 64, \"WALL\": 80, \"GRIM\": 82, \"JONE\": 50, \"REFU\": 32, \"NUEC\": 26, \"SPAT\": 38, \"BROW\": 40, \"KLEB\": 62, \"KENY\": 62, \"TAYL\": 38, \"DEWI\": 36, \"FREE\": 14, \"BZIA\": 12, \"WMSN\": 4, \"LLAN\": 4}", "worked_counties_mobile": "{\"AD4EB\": [\"HALL\", \"DONL\", \"POTT\", \"HOPK\", \"WILB\", \"KAUF\", \"FANN\", \"RUSK\", \"HDMN\", \"MORR\", \"WOOD\", \"SMIT\", \"CHIL\", \"MONT\", \"TITU\", \"CAMP\", \"CASS\", \"DELT\", \"TARR\", \"MARI\", \"COLN\", \"COLW\", \"CARS\", \"CLAY\", \"DENT\", \"WICH\", \"HRSN\", \"HUNT\", \"PARK\", \"GREG\", \"ARCH\", \"RAND\", \"LAMA\", \"RAIN\", \"DALS\", \"FRAN\", \"PANO\", \"ARMS\", \"UPSH\", \"ROCK\", \"VZAN\", \"WISE\"], \"K5T\": [\"PPIN\", \"DENT\", \"STEP\"], \"N5NA\": [\"SCUR\", \"JONE\", \"SHAC\", \"BORD\", \"WINK\", \"FISH\", \"ECTO\", \"MIDL\", \"REAG\", \"STER\", \"ANDR\", \"RUNN\", \"CROC\", \"EAST\", \"CALL\", \"CRAN\", \"BROW\", \"GLAS\", \"UPTO\", \"COKE\", \"STEP\", \"PECO\", \"DAWS\", \"MART\", \"WARD\", \"TAYL\"], \"N5NU\": [\"TRIN\", \"MGMY\", \"HOUS\", \"CHER\", \"LIBE\", \"NACO\", \"SJAC\", \"WALK\", \"RUSK\"], \"N5T\": [\"COOK\", \"DENT\"], \"K5CM\": [\"CASS\", \"DELT\", \"UPSH\", \"HOPK\", \"BOWI\", \"LAMA\", \"WOOD\", \"FANN\", \"FRAN\", \"RRIV\", \"HUNT\", \"TITU\", \"CAMP\", \"MORR\"], \"K5K\": [\"DELT\", \"HOPK\", \"DENT\"], \"K5EC\": [\"WALL\", \"RBSN\", \"LEON\", \"MADI\", \"GRIM\", \"BZOS\", \"FREE\"], \"KT3X\": [\"LAVA\", \"DEWI\", \"VICT\", \"NUEC\", \"WILY\", \"LIVO\", \"JWEL\", \"MMUL\", \"HIDA\", \"JHOG\", \"DUVA\", \"FAYE\", \"JKSN\", \"BEE\", \"WEBB\", \"BROO\", \"ZAPA\", \"CMRN\", \"GOLI\", \"REFU\", \"LEE\", \"SPAT\", \"KENY\", \"KLEB\"], \"N5KW\": [\"CASS\", \"DELT\", \"UPSH\", \"HOPK\", \"BOWI\", \"WOOD\", \"LAMA\", \"FANN\", \"RRIV\", \"FRAN\", \"HUNT\", \"TITU\", \"CAMP\", \"MORR\"], \"KE5OBS\": [\"DELT\", \"HOPK\"], \"KC4EEL\": [\"DELT\", \"HOPK\"], \"K5B\": [\"COOK\", \"DENT\"], \"KR1BBT\": [\"LEE\"], \"KE5ZPP\": [\"BZIA\"], \"KJ5GCH\": [\"TARR\"], \"N5TTT\": [\"LLAN\", \"WMSN\"]}", "created_at": "2026-11-18T19:04:28.382355+00:00", "updated_at": "2026-11-18T19:04:28.382355+00:00"}

foo =  {
    'year': '2026',
    'check': {'categorized_log': 126, 
            'scored_qsos': 0, 'scored_mode': 40111,
            'scored_band': 0, 'scored_hour': 0, 'invalidated_qsos': 47446,
            'with receiver': 0} ,
    'total_logs': 413,
    'rejected_logs': 0,
    'dx_logs': 8,
    'us_logs': 251,
    'cdn_logs': 20,
    'tx_mobile_logs': 18,
    'tx_fixed_logs': 108,
    'unclassed_logs': 1,
    'total_qsos': 52779,
    
'qsos_by_mode': {'PH': 16544, 'CW': 23303, 'RY': 39, 'DG': 225}
'qsos_by_band': {'160': 0, '80': 0, '40': 0, '20': 0, '15': 0, '10': 0, '6': 0, '2': 0}
'qsos_by_hour': 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    'qsos_with_tx': 23794,
    'qsos_with_us': 25964,
    'qsos_with_canada': 1074,
    'qsos_with_dx': 1768,
    'duplicate_qsos': 933,
    'nils': 3216,
    'busteds': 972,
    'other_invalid_qsos': 41353,
    'multi_county_exchanges': 28,
    'uniques': 18998,
    'mobile_activation_counts': {
    'MARI': 48,
    'PPIN': 444,
    'STEP': 465,
    'EAST': 88,
    'HRSN': 110,
    'CHER': 101,
    'DENT': 679,
    'COOK': 304,
    'CALL': 44,
    'PANO': 96,
    'RUSK': 81,
    'DELT': 732,
    'FANN': 360,
    'HUNT': 410,
    'HOPK': 718,
    'RBSN': 118,
    'MADI': 140,
    'LEON': 140,
    'FRAN': 357,
    'WEBB': 128,
    'JHOG': 104,
    'ZAPA': 100,
    'UPSH': 250,
    'WOOD': 244,
    'MONT': 156,
    'ECTO': 122,
    'CLAY': 131,
    'WINK': 124,
    'ARCH': 86,
    'WICH': 194,
    'HDMN': 124,
    'CAMP': 154,
    'CHIL': 88,
    'WALK': 90,
    'MIDL': 76,
    'LAMA': 207,
    'BOWI': 301,
    'CASS': 376,
    'DAWS': 82,
    'LEE': 85,
    'FAYE': 9,
    'MART': 100,
    'RAIN': 114,
    'TRIN': 72,
    'LAVA': 42,
    'TITU': 260,
    'RRIV': 145,
    'MORR': 247,
    'BZOS': 130,
    'GREG': 86,
    'SMIT': 104,
    'VZAN': 98,
    'COKE': 70,
    'KAUF': 110,
    'WILY': 84,
    'STER': 90,
    'ROCK': 142,
    'GLAS': 106,
    'DALS': 146,
    'COLN': 130,
    'NACO': 216,
    'BROO': 76,
    'TARR': 54,
    'WISE': 246,
    'ANDR': 66,
    'WILB': 128,
    'WARD': 92,
    'PECO': 80,
    'CRAN': 68,
    'CROC': 70,
    'HALL': 130,
    'COLW': 84,
    'UPTO': 88,
    'DONL': 130,
    'ARMS': 124,
    'MGMY': 40,
    'RAND': 155,
    'CARS': 154,
    'POTT': 158,
    'REAG': 94,
    'SJAC': 66,
    'BORD': 84,
    'FISH': 66,
    'CMRN': 74,
    'HIDA': 80,
    'DUVA': 74,
    'JWEL': 64,
    'LIVO': 86,
    'MMUL': 84,
    'VICT': 52,
    'JKSN': 24,
    'HOUS': 70,
    'LIBE': 28,
    'PARK': 62,
    'SHAC': 64,
    'BEE': 78,
    'GOLI': 78,
    'SCUR': 48,
    'RUNN': 66,
    'WALL': 80,
    'GRIM': 82,
    'JONE': 50,
    'REFU': 32,
    'NUEC': 26,
    'SPAT': 38,
    'BROW': 40,
    'KLEB': 64,
    'KENY': 64,
    'TAYL': 38,
    'DEWI': 36,
    'FREE': 14,
    'BZIA': 12,
    'WMSN': 4,
    'LLAN': 4},
    'worked_couunties_mobile': {
    'AD4EB': ['RUSK', 'TITU', 'ARMS', 'SMIT', 'DONL', 'PANO', 'COLN', 'PARK', 'VZAN', 'GREG', 'CAMP', 'WICH', 'RAND', 'WISE', 'MONT', 'KAUF', 'HOPK', 'CARS', 'HALL', 'WILB', 'CHIL', 'CLAY', 'CASS', 'DENT', 'FANN', 'HDMN', 'ROCK', 'MARI', 'ARCH', 'TARR', 'RAIN', 'POTT', 'MORR', 'FRAN', 'WOOD', 'LAMA', 'DELT', 'DALS', 'HUNT', 'UPSH', 'HRSN', 'COLW'],
    'K5T': ['STEP', 'PPIN', 'DENT'],
    'N5NA': ['STER', 'EAST', 'ANDR', 'BROW', 'ECTO', 'FISH', 'MIDL', 'WINK', 'CRAN', 'REAG', 'SHAC', 'SCUR', 'CALL', 'RUNN', 'STEP', 'COKE', 'PECO', 'CROC', 'MART', 'BORD', 'WARD', 'DAWS', 'TAYL', 'JONE', 'GLAS', 'UPTO'],
    'N5NU': ['TRIN', 'RUSK', 'WALK', 'NACO', 'MGMY', 'SJAC', 'HOUS', 'LIBE', 'CHER'],
    'N5T': ['COOK', 'DENT'],
    'K5CM': ['WOOD', 'TITU', 'CASS', 'FANN', 'LAMA', 'DELT', 'RRIV', 'HUNT', 'UPSH', 'HOPK', 'CAMP', 'BOWI', 'MORR', 'FRAN'],
    'K5K': ['DELT', 'HOPK', 'DENT'],
    'K5EC': ['LEON', 'GRIM', 'FREE', 'RBSN', 'MADI', 'WALL', 'BZOS'],
    'KT3X': ['KLEB', 'LAVA', 'HIDA', 'DEWI', 'CMRN', 'LEE', 'GOLI', 'SPAT', 'KENY', 'LIVO', 'BEE', 'NUEC', 'ZAPA', 'DUVA', 'JWEL', 'JHOG', 'BROO', 'MMUL', 'REFU', 'VICT', 'FAYE', 'WEBB', 'JKSN', 'WILY'],
    'N5KW': ['WOOD', 'TITU', 'CASS', 'FANN', 'LAMA', 'DELT', 'RRIV', 'HUNT', 'UPSH', 'HOPK', 'CAMP', 'BOWI', 'MORR', 'FRAN'],
    'KE5OBS': ['DELT', 'HOPK'],
    'KC4EEL': ['DELT', 'HOPK'],
    'K5B': ['COOK', 'DENT'],
    'KR1BBT': ['LEE'],
    'KE5ZPP': ['BZIA'],
    'KJ5GCH': ['TARR'],
    'N5TTT': ['WMSN', 'LLAN']}
}


# def create_tables():
#     """Create database tables if they don't exist"""
#     with sqlite3.connect(DATABASE_FILE) as conn:
#         cursor = conn.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS contest_stats (
#                 year TEXT NOT NULL,
#                 stats TEXT,
#                 PRIMARY KEY (year)
#                     )
#                 ''')

#         conn.commit()

# class ContestDatabase:

#     def __init__(self, db_path: str = 'txqp.db'):
#         """
#         Initialize database connection.
        
#         Args:
#             db_path: Path to SQLite database file
#         """
#         self.db_path = Path(db_path)
#         # Ensure directory exists
#         self.db_path.parent.mkdir(parents=True, exist_ok=True)

#         self.drop_db = True

#         self.field_types = {'integer': 0, 'string': '',
#                             'set': set(), 'list': [], 'dict': {}, 'cab': ''}
#         self.result_fields = {'integer': [
#             'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
#             'total_multipliers', 'cab_mobile_points', 
#             'mtb_mobile_points', 'cw_qsos',
#             'ph_qsos', 'dg_qsos', 'ry_qsos', 'score_wo_bonus',
#             'special_station_contacts', 'claimed_score', 'uniques', 'nils',
#             'busteds', 'dup_qsos', 'category_rank', 'invalid_exchange_qsos',
#             'other_bad_qsos'
#         ],
#         'string': [  # from the result object
#             'year',   'dxcc_entity'
#         ],
#         'set': [ 'states_worked', 'provinces_worked',
#             'de_exch_rcvd', 'dx_exch_sent', 'bands_worked', 
#             'counties_worked', 'dx_worked', 'counties_activated'
#         ],
#         'list': ['errors', 'warnings', 'qsos_by_hour', 'busted_calls', 'nil_calls'],
#         'cab_attributes': [
#             'club', 'name', 'location', 'name', 'category_band', 'email',
#             'category_mode', 'category_power', 'category_station', 
#             'cat', 'claimed_score', 'category_power', 'category_station', 'callsign',
#         ],
#         'dicts': ['qsos_by_band', 'qsos_by_mode','mobile_activation_counts', 'worked_counties_mobile', 'mobile_counties_worked']
#         }
#         self.stats_fields = {
#             'integer': ['total_logs', 'rejected_logs', 'dx__logs', 'us_cdn_logs', 'tx_logs', 'unclassed_logs', 'total_qsos', 'valid_qsos', 'qsos_with_tx', 'qsos_with_us_cdn', 'qsos_with_dx', 'duplicate_qsos', 'nils', 'busteds', 'invalid_qsos', 'uniques'],
#             'string': ['year'],  # from the result object 
#             'list': ['rejected_logs_filenames', 'qsos_by_hour', 'nil_calls', 'busted_calls'],
#             'dict': ['qsos_by_band', 'qsos_by_mode', 'mobile_activation_counts', 'worked_counties_mobile'],
#             'set': ['counties_worked', 'states_worked', 'provinces_worked', 'dx_worked', 'counties_activated'],
#             'cab_attribute': []  # placeholder so serial deserial can do both types
#         }
#         self.stats = {
#                 'year': CONTEST_YEAR,
#                 'total_logs': 200,
#                 'rejected_logs': 10,
#                 'rejected_logs_filenames': [], # logs of PARSER not_valids
#                 'qso_parser_not_valid': 23,
#                 'dx_logs': 10,
#                 'us_cdn_logs': 150,
#                 'tx_logs': 40,
#                 'unclassed_logs': 10,
#                 'total_qsos': 5000,
#                 'valid_qsos': 4800,
#                 'qsos_by_band': {'160': 0, '80': 0, '40': 34, '20': 140, '15':120, '10': 5, '6': 1, '2': 5},
#                 'qsos_by_mode': {'PH': 200, 'CW': 50, 'RY': 23, 'DG': 23},
#                 'qsos_by_hour': [0] * 24,
#                 'qsos_with_tx': 23,
#                 'qsos_with_us_cdn': 23,
#                 'qsos_with_dx': 23,
#                 'duplicate_qsos': 23,
#                 'nils': 10,
#                 'nil_calls': [],
#                 'busteds': 10,
#                 'busted_calls': [],
#                 'invalid_qsos': 23,
#                 'uniques': 23,
#                 'counties_worked': set(),
#                 'states_worked': set(),
#                 'provinces_worked': set(),
#                 'dx_worked': set(),
#                 'counties_activated': set(),
#                 'mobile_activation_counts': {},
#                 'worked_counties_mobile': {},
#                 'calls_w_not_valid_qsos': set(),
#                 'dx_log_de_missing': 23,
#                 'total_multipliers': 23,
#             }
    
#     def _serialize_result(self, result: Dict, field_types: Dict, fields: Dict) -> Dict:
#         """
#         Adds simple fields from the "result" object
#         Adds attributes of the "CAB" objext
#         Convert result dict to database-storable format.
#         Convert lists to JSONF
#         Converts sets to JSON lists, handles complex types.
#         """
#         db_result = {}
#         cab = result.get('cab', None)
#         try:
#             # put values from the above listed fields into db_result
#             for typ in list(field_types.keys()):
#                 if typ == 'set':
#                     for fld in fields[typ]:
#                         value = result.get(fld, field_types[typ])
#                         db_result[fld] = json.dumps(sorted(list(value)))

#                 elif typ == 'list':
#                     for fld in fields[typ]:
#                         value = result.get(fld, field_types[typ])
#                         db_result[fld] = json.dumps(list(value))

#                 elif typ in ['integer', 'string']:
#                     for fld in fields[typ]:
#                         db_result[fld] = result.get(fld, field_types[typ])
           
#                 elif typ == 'dict':
#                     for fld in fields[typ]:
#                         value = result.get(fld, {})
#                         # Convert sets in dict values to lists
#                         for k in list(value.keys()):
#                             if isinstance(value[k], set):
#                                 value[k] = list(value[k])
#                         db_result[fld] = json.dumps(value)

#                 elif typ == 'cab_attributes':
#                     flds = fields.get(typ, [])
#                     for fld in flds:
#                         db_result[fld] = getattr(cab, fld, '')
            
#             # Timestamps
#             now =  datetime.now(timezone.utc).isoformat()
#             db_result['created_at'] = now
#             db_result['updated_at'] = now
#         except Exception as e:
#             print(f"exception {e} in creating db_result")
#             # print('BREAK')
#         return db_result
    
#     def _deserialize_result(self, result: Dict, field_types: Dict, fields: Dict) -> Dict:
#         """ The opposite of serialize_result
#             Reads data from the databaser one operator record
#             Adds simple fields from the "result" object
#             Adds attributes of the "CAB" objext
#             Convert result dict to JSON-usable format.
#             Convert lists to JSON
#             Converts sets to JSON lists, handles complex types.
#             """
#         if result:
#             display_result = {}
#             try:
#                 for typ in list(field_types.keys()):
#                 # INTEGERS AND STRINGS
#                     if typ in ['integer', 'string']:
#                         for fld in fields[typ]:
#                             display_result[fld] = result.get(fld, field_types[typ])

#                     # SETS AND LISTS
#                     elif  typ in list([ 'set', 'list']):
#                         for fld in fields[typ]:
#                             display_result[fld] = json.loads(result.get(fld, field_types[typ]))

#                     # DICT_FIELDS
#                     elif typ == 'dict':
#                         for field in fields[typ]:
#                             if field in result and result[field]:
#                                 display_result[field] = json.loads(result[field])

#                     # the cab fields saved in the DB are all strings. We are not going to
#                     # reconstitute the cab object, but just storing the fiels in display_result
#                     elif typ == 'cab_attributes' and len(fields[typ]) > 0:
#                         for fld in fields[typ]:
#                             display_result[fld] = result.get(fld, '')

#                 display_result['cat'] = RANKINGS[display_result['cat']]

#             except Exception as e:
#                 s.out_files['errors'].write(f"could not deserialize {result}\n")
        
#         return display_result
    
#         print(f"stats keys {list(self.stats.keys())} ")

    
#     def save_stats(self, year, stats):
#         db_result = self._serialize_result(stats, self.field_types, self.stats_fields)
                
#         # Build SQL
        
#         # Use INSERT OR REPLACE to overwrite existing records
#         sql = f'''
#             INSERT OR REPLACE INTO contest_stats (year, stats) VALUES (?, ?);
#         '''
        
#         values = [year, json.dumps(db_result)]
        
#         try:
#             with sqlite3.connect(self.db_path) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute(sql, values)
#                 conn.commit()
#             return True
        
#         except Exception as e:
#             print(f"Error saving statistics: {e}")
#             return False
        
        
#     def get_stats(self, year: str) -> Dict:
#         """  Get contest statistics for a year.
#                 Args:
#                     year: Contest year
#                 Returns:
#                     Dict with statistics
#         """
#         with sqlite3.connect(self.db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute('''SELECT * FROM contest_stats WHERE year = ?''', (year))
#             row = cursor.fetchone()
#             if row:
#                 columns = [desc[0] for desc in cursor.description]
#                 result = {}
#                 for i, col in enumerate(columns):
#                     result[col] = row[i]
#                 return self._deserialize_result(result, self.field_types, self.result_fields)
                
#         return None
# # '{"total_logs": 200, "rejected_logs": 10, "dx__logs": 0, "us_cdn_logs": 150, "tx_logs": 40, "unclassed_logs": 10, "total_qsos": 5000, "valid_qsos": 4800, "qsos_with_tx": 23, "qsos_with_us_cdn": 23, "qsos_with_dx": 23, "duplicate_qsos": 23, "nils": 10, "busteds": 10, "invalid_qsos": 23, "uniques": 23, "year": "2026", "counties_worked": "[]", "states_worked": "[]", "provinces_worked": "[]", "dx_worked": "[]", "counties_activated": "[]", "rejected_logs_filenames": "[]", "qsos_by_hour": "[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]", "nil_calls": "[]", "busted_calls": "[]", "qsos_by_band": "{\\"160\\": 0, \\"80\\": 0, \\"40\\": 34, \\"20\\": 140, \\"15\\": 120, \\"10\\": 5, \\"6\\": 1, \\"2\\": 5}", "qsos_by_mode": "{\\"PH\\": 200, \\"CW\\": 50, \\"RY\\": 23, \\"DG\\": 23}", "mobile_activation_counts": "{}", "worked_counties_mobile": "{}", "created_at": "2026-10-20T22:09:35.870929+00:00", "updated_at": "2026-10-20T22:09:35.870929+00:00"}'


# db = ContestDatabase(Path(DATABASE_FILE))
# create_tables()
# # Convenience functions
# def save_stats(contest_year: str, result: Dict, db_path: str = DATABASE_FILE) -> bool:
#     """
#     Save a result to the database.
    
#     Args:
#         result: Result dictionary from processor
#         db_path: Path to database file
        
#     Returns:
#         True if saved successfully
#     """
#     db = ContestDatabase(db_path)
#     db.drop_db = False
#     return db.save_stats(contest_year, result)

# def get_stats(year: str, db_path: str = DATABASE_FILE) -> Dict:
#     """
#     Get a result from the database.
    
#     Args:
#         year: Contest year
#         callsign: Station callsign
#         db_path: Path to database file
        
#     Returns:
#         Result dict or None if not found
#     """
#     db = ContestDatabase(db_path)
#     db.drop_db = False
#     return db.get_stats(year)


# save_stats(CONTEST_YEAR, db.stats)
# print('break')
# get_stats(CONTEST_YEAR)
# print('break')

# def is_fuzzy_match(x: str, y: str, max_missing: int = 2) -> bool:
#     """
#     Determines if callsign `y` could be a mistyping of callsign `x`.
#     The rule: `y` must contain all but `max_missing` characters/numbers 
#     from `x`, and they must appear in the same relative order.
#     Args:
#         x: The original callsign.
#         y: The potentially mistyped callsign.
#         max_missing: The maximum number of characters from `x` that can 
#                      be missing in `y`. (Defaults to 2 based on the rule).
#     Returns:
#         True if it's a match, False otherwise.
#     """
#     x = x.upper()
#     y = y.upper()
    
#     m, n = len(x), len(y)
    
#     # Compute the Longest Common Subsequence (LCS)
#     dp = [[0] * (n + 1) for _ in range(m + 1)]
    
#     for i in range(1, m + 1):
#         for j in range(1, n + 1):
#             if x[i - 1] == y[j - 1]:
#                 dp[i][j] = dp[i - 1][j - 1] + 1
#             else:
#                 dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
#     lcs_length = dp[m][n]
#     if lcs_length == 1 and len(x) == 2:
#         return True
#     return lcs_length >= len(x) - max_missing

# # is_fuzzy_match('AI6G', 'AI6O')

# section = {
#     'section_title': 'Texas - Mobile Stations',
#     'table_fields': [
#         ['callsign', 'Call'], ['total_score', 'Score'], ['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs'], ['qso_points', 'QSOPts'], ['total_multipliers', 'Mults'], ['score_wo_bonus', 'w/o Bonus'], ['cab_mobile_points', 'CABPts'], ['mtb_mobile_points', 'MTBPts'], ['club', 'Club']],
#     'tables': [
#         {
#             'title': 'Texas Mobile Single Operator Mixed Mode–may be assisted (no contest power limit)', 
#             'category': 'TMS', 'headers': ['Rank', 'CallSign', 'Score', 'CWQs', 'PHQs', 'QSOPts', 'Mults', 'w/o Bonus', 'CABPts', 'MTBPts'], 
#             'rows': [
#                 [1, 'K5CM', 888220, 1478, 343, 5120, 81, 414720, 473000, 500], [2, 'KT3X', 509730, 1012, 77, 3190, 67, 213730, 296000, 0], [3, 'N5KW', 327420, 554, 203, 2068, 65, 134420, 193000, 0], [4, 'N5NU', 270232, 500, 72, 1644, 78, 128232, 142000, 0], [5, 'K5K', 264569, 347, 273, 1587, 87, 138069, 126000, 500], [6, 'N5T', 202936, 456, 384, 2136, 51, 108936, 94000, 0], [7, 'KE5OBS', 57020, 12, 160, 356, 45, 16020, 41000, 0], [8, 'KJ5GCH', 4312, 0, 20, 82, 16, 1312, 3000, 0]
#             ]
#         }
#     ]
# }

# foo = [[1, 'K5CM', 888220, 1478, 343, 5120, 81, 414720, 473000, 500], [2, 'KT3X', 509730, 1012, 77, 3190, 67, 213730, 296000, 0], [3, 'N5KW', 327420, 554, 203, 2068, 65, 134420, 193000, 0], [4, 'N5NU', 270232, 500, 72, 1644, 78, 128232, 142000, 0]]
# filenames = [p.name for p in dir_path.iterdir() if p.is_file()]
# result_index = 0
# hq_clubs = set()
# added_clubs = set()
# cab_clubs = set()
# s = SHARED()
# for file in filenames:
#     try:
#         file_path = (SCRIPT_DIR / BATCH_INPUT_DIR / CONTEST_YEAR / file).resolve()
#         cab = parse_log_file(file_path, ignore_unknown_key=True, check_categories=False, ignore_order=True, check_mode=False)
#         cab.callsign = cab.callsign.split('/')[0]
#         try:
#             if 'hq_anything' in list(cab.__dict__.keys()):
#                 if "HQ-CLUB" in list(cab.hq_anything.keys()):
#                     hq_club = cab.hq_anything['HQ-CLUB']
#                     if hq_club not in ['None', None]:
#                         hq_clubs.add(hq_club)
#                         if hq_club not in s.contest_clubs_original:
#                             added_clubs.add(hq_club)
#                     else:
#                         club = cab.club
#                         if (cab.club not in ['None', None, 'NONE']) and (cab.club not in list(hq_clubs) and cab.club not in (added_clubs)):
#                             print(f"{cab.club}")
#                             cab_clubs.add(cab.club)
#         except Exception as e:
#             print(f"error getting HQ-CLUB {cab.callsign}  {e}")
#             continue
#     except Exception as e:
#         if file:
#             s.stats["rejected_logs"] += 1
#             s.stats["rejected_logs_filenames"].append(file)
#             print(f"ERROR - REJECTED: log file {file} was rejected by the parser")
#             s.out_files['errors'].write(f"REJECTED log file {file} was rejected by the parser\n")
#             continue
# print(f"# of clubs in HQ-CLUB: that were Bruce's dropdown: {len(hq_clubs)}\n dropdown clubs:\n\n {hq_clubs}\n\n# in HQ-CLUB: that were NOT in Bruce's dropdown: {len(added_clubs)}\nclubs added: {added_clubs} {cab_clubs}\n\n# in Cabrillo CLUB: when HQ-CLUB was NULL\nThese are not in the other two lists: {len(cab_clubs)}\nclubs added: {cab_clubs}")



# [
#     {
#         "club": null
#     },
#     {
#         "club": "Alabama Contest Group"
#     },
#     {
#         "club": "Alabama contest group"
#     },
#     {
#         "club": "Alexandria Radio Club"
#     },
#     {
#         "club": "Amateur Radio Club of Parker County"
#     },
#     {
#         "club": "Arizona Outlaws Contest Club"
#     },
#     {
#         "club": "Arkansas DX Assn"
#     },
#     {
#         "club": "Atlantic Coast DX & Contest Group"
#     },
#     {
#         "club": "Austin Amateur Radio Club"
#     },
#     {
#         "club": "Austin QRP Club"
#     },
#     {
#         "club": "BAY AREA DXERS"
#     },
#     {
#         "club": "Bavarian Contest Club"
#     },
#     {
#         "club": "Bay Area DXers"
#     },
#     {
#         "club": "Big Sky Contesters"
#     },
#     {
#         "club": "Bloomington Amature Radio Club --- K9DIY"
#     },
#     {
#         "club": "Bristol (TN) ARC"
#     },
#     {
#         "club": "Bristol (TN/VA) ARC"
#     },
#     {
#         "club": "CARESS - Coquitlam Amateur Radio Club"
#     },
#     {
#         "club": "CCO"
#     },
#     {
#         "club": "CONTEST CLUB ONTARIO"
#     },
#     {
#         "club": "CW Contest Club"
#     },
#     {
#         "club": "Candlewood ARA"
#     },
#     {
#         "club": "Central Texas DX and Contest Club"
#     },
#     {
#         "club": "Central Virginia Contest Club"
#     },
#     {
#         "club": "Contest Club Ontario"
#     },
#     {
#         "club": "Contest Group du Quebec"
#     },
#     {
#         "club": "Cuyahoga ARS"
#     },
#     {
#         "club": "DCT ARC"
#     },
#     {
#         "club": "DEEP DIXIE CONTEST CLUB"
#     },
#     {
#         "club": "DFW Contest Group"
#     },
#     {
#         "club": "DICKSON COUNTY ARC"
#     },
#     {
#         "club": "DX"
#     },
#     {
#         "club": "Dawn Patrol Surf Club"
#     },
#     {
#         "club": "Dupage ARC"
#     },
#     {
#         "club": "East Lansing DX Club"
#     },
#     {
#         "club": "Ellis County ARC"
#     },
#     {
#         "club": "FCG"
#     },
#     {
#         "club": "FLORIDA CONTEST GROUP"
#     },
#     {
#         "club": "FRANKFORD RADIO CLUB"
#     },
#     {
#         "club": "Fayette County DX Club"
#     },
#     {
#         "club": "Florida Contest Group"
#     },
#     {
#         "club": "Frankford Radio Club"
#     },
#     {
#         "club": "Ft. Smith ARC"
#     },
#     {
#         "club": "Garland Amateur Radio Club"
#     },
#     {
#         "club": "Grayson County ARC"
#     },
#     {
#         "club": "Great Places Contest Club"
#     },
#     {
#         "club": "Houston ECHO Society"
#     },
#     {
#         "club": "Hudson Valley Contesters and DXers"
#     },
#     {
#         "club": "Irving ARC"
#     },
#     {
#         "club": "Jefferson ARC"
#     },
#     {
#         "club": "KANSAS CITY CONTEST CLUB"
#     },
#     {
#         "club": "KARO ECHO"
#     },
#     {
#         "club": "KCCC"
#     },
#     {
#         "club": "Kansas City Contest Cliub"
#     },
#     {
#         "club": "Kansas City Contest Club"
#     },
#     {
#         "club": "Kansas city contest club"
#     },
#     {
#         "club": "Kentucky Contest Group"
#     },
#     {
#         "club": "Lake Area Amateur Radio Club"
#     },
#     {
#         "club": "Lake Area Amateur Radio Klub"
#     },
#     {
#         "club": "MINNESOTA  WIRELESS  ASSN"
#     },
#     {
#         "club": "MINNESOTA WIRELESS ASSN"
#     },
#     {
#         "club": "Mad River Radio Club"
#     },
#     {
#         "club": "Maritime Contest Club"
#     },
#     {
#         "club": "Medina County ARC"
#     },
#     {
#         "club": "Metrocrest Amateur Radio Society"
#     },
#     {
#         "club": "Metrocrest Amateur Radio Society KB5A"
#     },
#     {
#         "club": "Midland ARC"
#     },
#     {
#         "club": "Minnesota Wireless Assn"
#     },
#     {
#         "club": "NAQCC"
#     },
#     {
#         "club": "NASA JSC W5RRR Amateur Radio Club"
#     },
#     {
#         "club": "NCARC"
#     },
#     {
#         "club": "NIAGARA FRONTIER RADIOSPORT"
#     },
#     {
#         "club": "NONE"
#     },
#     {
#         "club": "New Providence ARC"
#     },
#     {
#         "club": "Niagara Frontier Radiosport"
#     },
#     {
#         "club": "None"
#     },
#     {
#         "club": "North Coast Contesters"
#     },
#     {
#         "club": "North Texas ARS"
#     },
#     {
#         "club": "Northwest Amateur Radio Society"
#     },
#     {
#         "club": "ORANGE COUNTY AMATEUR RADIO CLUB"
#     },
#     {
#         "club": "Orca DX and Contest"
#     },
#     {
#         "club": "PART of Westford"
#     },
#     {
#         "club": "POTOMAC VALLEY RADIO CLUB"
#     },
#     {
#         "club": "PVRC"
#     },
#     {
#         "club": "Potomac Valley Radio CLub"
#     },
#     {
#         "club": "Potomac Valley Radio Club"
#     },
#     {
#         "club": "RIOARC"
#     },
#     {
#         "club": "Radio Amateurs of Northern Vermont"
#     },
#     {
#         "club": "Randolph County"
#     },
#     {
#         "club": "Red River Valley ARC"
#     },
#     {
#         "club": "Redwood Empire DX Assn"
#     },
#     {
#         "club": "River Bend Wireless Operators Club"
#     },
#     {
#         "club": "Rushmore Radio Amateurs"
#     },
#     {
#         "club": "SCCC"
#     },
#     {
#         "club": "SOCIETY OF MID-WEST CONTESTERS"
#     },
#     {
#         "club": "SOCIETY OF MIDWEST CONTESTERS"
#     },
#     {
#         "club": "SP DX CLUB"
#     },
#     {
#         "club": "SWAMP FOX CONTEST GROUP"
#     },
#     {
#         "club": "Shenandoah Valley Amateur Radio Cllub"
#     },
#     {
#         "club": "Slovak Contest Group"
#     },
#     {
#         "club": "Snohomish County Hams Club"
#     },
#     {
#         "club": "Society of Midwest Contesters"
#     },
#     {
#         "club": "Soth East Contest Club"
#     },
#     {
#         "club": "South East Contest Club"
#     },
#     {
#         "club": "South Texas Amatuer Radio Club"
#     },
#     {
#         "club": "South Texas DX and Contest Club"
#     },
#     {
#         "club": "Southern California Contest Club"
#     },
#     {
#         "club": "Sterling Park ARC"
#     },
#     {
#         "club": "Sterling Park Amateur Radio Club"
#     },
#     {
#         "club": "Swamp Fox Contest Group"
#     },
#     {
#         "club": "TCG"
#     },
#     {
#         "club": "TDXS"
#     },
#     {
#         "club": "TENNESSEE CONTEST GROUP"
#     },
#     {
#         "club": "Tennesse Contest Club"
#     },
#     {
#         "club": "Tennessee Contest Group"
#     },
#     {
#         "club": "Texas DX Society"
#     },
#     {
#         "club": "The 67 Ham Radio Group"
#     },
#     {
#         "club": "The American Legion Post 42 ARC"
#     },
#     {
#         "club": "The Houston ECHO Society, W5ECO"
#     },
#     {
#         "club": "Tri-County Amateur Radio Club"
#     },
#     {
#         "club": "WVDXC"
#     },
#     {
#         "club": "West Allis RAC"
#     },
#     {
#         "club": "West Allis Radio Amateur Club"
#     },
#     {
#         "club": "Western Washington DX Club"
#     },
#     {
#         "club": "Willamette Valley DX Club"
#     },
#     {
#         "club": "YANKEE CLIPPER CONTEST CLUB"
#     },
#     {
#         "club": "YCCC"
#     },
#     {
#         "club": "Yankee Clipper Contest Club"
#     },
#     {
#         "club": "dfw cONTEST GROUP"
#     },
#     {
#         "club": "n/a"
#     },
#     {
#         "club": "none"
#     },
#     {
#         "club": "saint paul radio club"
#     },
#     {
#         "club": "yankee clipper contest club"
#     }
# ]

# # import trace
# # trace

# # foo = {'title': 'Single Operator Mixed Mode High-Power (>150 watts power)', 'category': 'TSH', 'headers': ['Rank', 'Call', 'Score', 'CWQs', 'PHQs', 'QSOPts', 'Mults', 'w/o Bonus', 'MTBPts', 'Claimed'], 'rows': [[...], [...], [...], [...], [...], [...]]}


# # foo = [
# #         {
# #             'section_title': 'Texas - Mobile Stations',
# #             'show': [
# #                 ['callsign', 'CallSign'],
# #                 ['final_score', 'Score'],
# #                 ['qso_points', 'QSOPts'],
# #                 ['total_multipliers', 'Mults'],
# #                 ['score_wo_bonus', 'w/o Bonus'],
# #                 ['cab_mobile_points', 'CABPts'],
# #                 ['mtb_mobile_points', 'MTBPts'],
# #                 ['claimed_score', 'Claimed']
# #             ],
# #         },
# #         {'title': 'TMS', 'category': 'TXM SO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
# #         {'title': 'TMM', 'category': 'TXM MO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
# #         {'title': 'TMSC', 'category': 'TXM SO CWO', 'show': [['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]},
# #         {'title': 'TMSP', 'category': 'TXM SO PHO', 'show':[['cw_qsos', 'CWQs'], ['ph_qsos', 'PHQs']]}
# #     ]

# # {'title': 'Single Operator Mixed Mode (150 watts power limit)', 'category': 'TSL', 'headers': ['Rank', 'Call', 'Score', 'CWQs', 'PHQs', 'QSOPts', 'Mults', 'w/o Bonus', 'MTBPts', 'Claimed'], 'rows': [[...], [...], [...], [...], [...], [...], [...], [...], [...], [...], [...], [...], [...]]}



# # from pathlib import Path
# # import sqlite3
# # from pprint import pprint
# # from pathlib import Path
# # from typing import Dict, List, Optional
# # from datetime import datetime
# # from config.config_txqp import RANKINGS, RANK_TABLES
# # from config.config import DATABASE_FILE
# # # def format_result_for_display(result):
# # #     """
# # #     Convert the result dictionary to a format suitable for HTML display
# # #     Handles sets, dicts, and other complex type
# # #     """
# # #     display_result = {}
    
# # #     # Copy simple values
# # #     simple_fields = [
# # #         'callsign', 'exchange', 'overlay', 'location_type', 'mode_category',
# # #         'power_level', 'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
# # #         'total_multipliers', 'counties_worked_multiplier', 'states_worked_multiplier',
# # #         'provinces_worked_multiplier', 'dx_worked_multiplier', 'mtb_mobile_points',
# # #         'worked_n5lcc', 'num_n5lcc_contacts', 'name', 'club', 'claimed_score', 'year'
# # #     ]
    
# # #     for field in simple_fields:
# # #         display_result[field] = result.get(field, 'N/A')
    
# # #     # Convert sets to sorted lists
# # #     display_result['counties_worked'] = format_set_as_list(result.get('counties_worked', set()))
# # #     display_result['states_worked'] = format_set_as_list(result.get('states_worked', set()))
# # #     display_result['provinces_worked'] = format_set_as_list(result.get('provinces_worked', set()))
# # #     display_result['dx_worked'] = format_set_as_list(result.get('dx_worked', set()))
# # #     display_result['counties_activated'] = format_set_as_list(result.get('counties_activated', set()))
# # #     display_result['bands_worked'] = format_set_as_list(result.get('bands_worked', set()))
    
# # #     # Format QSOs by band
# # #     qsos_by_band = result.get('qsos_by_band', {})
# # #     display_result['qsos_by_band'] = [
# # #         {'band': band, 'count': count}
# # #         for band, count in sorted(qsos_by_band.items(), key=lambda x: x[0])
# # #     ]
    
# # #     # Format QSOs by mode
# # #     qsos_by_mode = result.get('qsos_by_mode', {})
# # #     display_result['qsos_by_mode'] = [
# # #         {'mode': mode, 'count': count}
# # #         for mode, count in qsos_by_mode.items()
# # #     ]
    

# # #     # Format QSOs by hour
# # #     try:
# # #         temp = result.get('qsos_by_hour', {})
# # #         display_result['qsos_by_hour'] = {}
# # #         for key in temp:
# # #             display_result['qsos_by_hour'][key] =  temp[key]
# # #     except Exception as e:
# # #         print(f"Error formatting qsos_by_hour for display: {e}")
# # #         display_result['qsos_by_hour'] = []
    
# # #     ## errors and warnings
# # #     display_result['errors'] = result['errors']
# # #     display_result['warnings'] = result['warnings']

# # #     return display_result
# # import json
# # SCRIPT_DIR = Path(__file__).resolve().parent
# # seq_cab_attributes = [
# #             'club', 'name', 'location', 'name', 'category_band', 'email',
# #             'category_mode', 'category_power', 'category_station', 
# #             'cat', 'claimed_score'
# #     ]
# #     # dict fields require different aproach from above fields
# # seq_dict_fields = [
# #             'qsos_by_band', 'qsos_by_mode','mobile_activation_counts'
# #         ]
        
# # seq_types_of_fields = {'integer': 0, 'string': '','set': set(), 'list': []}
# # seq_fields = {'integer': [
# #         'dxcc_code',
# #         'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
# #         'total_multipliers', 'cab_mobile_points', 
# #         'mtb_mobile_points', 'cw_qsos',
# #         'ph_qsos', 'dg_qsos', 'ry_qsos', 'score_wo_bonus',
# #         'special_station_contacts', 'claimed_score', 'uniques', 'nils',
# #         'busteds', 'dup_qsos', 'category_rank', 'invalid_exchange_qsos',
# #         'other_bad_qsos'
# #     ],
# #     'string': [  # from the result object
# #         'year', 'callsign',  'dxcc_entity'
# #     ],
# #     'set': [
# #         'counties_worked', 'states_worked', 'provinces_worked',
# #         'dx_worked', 'counties_activated', 'bands_worked',
# #         'de_exch_rcvd', 'dx_exch_sent', 'mobile_counties_worked',
# #         'mobile_activation_counts'
# #     ],
# #     'list': ['errors', 'warnings', 'qsos_by_hour', 'busted_calls', 'nil_calls']
# #     }

# # types_of_fields = {'integer': 0, 'string': '', 'set': set(), 'list': []}
# # fields = {'integer': [
# #     'dxcc_code',
# #     'final_score', 'qso_points', 'total_qsos', 'valid_qsos',
# #     'total_multipliers', 'cab_mobile_points', 
# #     'mtb_mobile_points', 'cw_qsos',
# #     'ph_qsos', 'dg_qsos', 'ry_qsos', 'score_wo_bonus',
# #     'special_station_contacts', 'claimed_score', 'uniques', 'nils',
# #     'busteds', 'dup_qsos', 'category_rank', 'invalid_exchange_qsos',
# #     'other_bad_qsos'
# # ],
# # 'string': [  # from the result object
# #     'year', 'callsign',  'dxcc_entity', 'club', 'name', 'location', 'name', 'category_band', 'email',
# #                 'category_mode', 'category_power', 'category_station', 
# #                 'cat', 'claimed_score'
# # ],
# # 'list': [ 'mobile_counties_worked', 'counties_worked', 'states_worked', 'provinces_worked',
# #         'dx_worked', 'counties_activated', 'bands_worked',
# #         'de_exch_rcvd', 'dx_exch_sent', 'errors', 'warnings', 'qsos_by_hour', 'busted_calls', 'nil_calls']
# # }
# # # dict fields require different aproach from above fields
# # dict_fields = [
# #     'qsos_by_band', 'qsos_by_mode','mobile_activation_counts'
# #     ]

# # cab_attributes = [
# #     'club', 'name', 'location', 'name', 'category_band', 'email',
# #     'category_mode', 'category_power', 'category_station', 
# #     'cat', 'claimed_score'
# #     ]

# # def deserialize_result(result):
# #     """ The opposite of serialize_result
# #         Reads data from the databaser one operator record
# #         Adds simple fields from the "result" object
# #         Adds attributes of the "CAB" objext
# #         Convert result dict to JSON-usable format.
# #         Convert lists to JSON
# #         Converts sets to JSON lists, handles complex types.
# #         """

# #     if result:
# #         display_result = {}
# #         try:
# #             # INTEGERS AND sTRINGHS
# #             for typ in list(['integer', 'string', 'list']):
# #                 for fld in fields[typ]:
# #                     display_result[fld] = result.get(fld, types_of_fields[typ])

# #             # SETS
# #             # for fld in fields['set']:
# #             #     display_result[fld] = list(set(json.loads(result.get(fld, []))))

# #             # DICTS
# #             for field in dict_fields:
# #                 if field in result and result[field]:
# #                     display_result[field] = result[field]

# #         except Exception as e:
# #             print(f"could not deserialize {result}")
    
# #     return result

# # def serialize_result(result):
# #     """
# #     Adds simple fields from the "result" object
# #     Adds attributes of the "CAB" objext
# #     Convert result dict to database-storable format.
# #     Convert lists to JSONF
# #     Converts sets to JSON lists, handles complex types.
# #     """
# #     db_result = {}
# #     try:
# #         # put values from the above listed fields into db_result
# #         for typ in list(seq_types_of_fields.keys()):   
# #             if typ == 'set':
# #                 for fld in seq_fields[typ]:
# #                     value = result.get(fld, seq_types_of_fields[typ])
# #                     db_result[fld] = json.dumps(sorted(list(value)))
# #             elif typ == 'list':
# #                 for fld in seq_fields[typ]:
# #                     value = result.get(fld, seq_types_of_fields[typ])
# #                     db_result[fld] = json.dumps(list(value))

# #             else:
# #                 for fld in seq_fields[typ]:
# #                     db_result[fld] = result.get(fld, seq_types_of_fields[typ])
        
# #         for field in seq_dict_fields:
# #             value = result.get(field, {})
# #             # Convert sets in dict values to lists
# #             db_result[field] = json.dumps(value)
# #             # print(f"field: {field} value: {value}")
        
# #         # Timestamps
# #         now = datetime.utcnow().isoformat()
# #         db_result['created_at'] = now
# #         db_result['updated_at'] = now
# #     except Exception as e:
# #         print(f"exception in creating db_result")
# #         # print('BREAK')
    
# #     return db_result


# # result = {
# #     "bands_worked": [],
# #     "busted_calls": [["AA5KC", "N5DN"]],
# #     "busteds": 1,
# #     "cab_mobile_points": 0,
# #     "callsign": "AA5KC",
# #     "cat": "TSL",
# #     "category_band": "ALL",
# #     "category_mode": "MIX",
# #     "category_power": "LP",
# #     "category_rank": 12,
# #     "category_station": "FIX",
# #     "claimed_score": 9204,
# #     "club": "None",
# #     "counties_activated": {"KINN"},
# #     "counties_worked": {"AUST", "BAIL", "BAST", "BURL", "COML", "DALS", "DENT", "FBEN", "GILL", "GRIM", "HARR", "HAYS", "HRSN", "JACK", "JDAV", "KAUF", "KINN", "MEDI", "MILL", "MLEN", "NUEC", "PARK", "SMIT", "SOME", "TARR", "WALK", "WASH", "WHAR", "WLSN"},
# #     "created_at": "2026-10-08T18:54:53.653180",
# #     "cw_qsos": 36,
# #     "de_exch_rcvd": {},
# #     "dg_qsos": 0,
# #     "dup_qsos": 1,
# #     "dx_exch_sent": {},
# #     "dx_worked": {},
# #     "dxcc_code": 0,
# #     "dxcc_entity": "AA5KC",
# #     "email": "KJ5BYZ@gmail.com",
# #     "errors": ["BUSTED QSO to N5DN exchs:KINN-SOME mode:PH band:40 Sept 19th 1548Z\\n", "NIL QSO from-to AA5KC-KF5VDX exchs:KINN-NUEC mode:PH band:40 Sept 19th 1648Z\\n", "Duplicate QSO from-to: AA5KC-K5LSU exchs:KINN-LA mode:CW band:20 Sept 19th 1846Z\\n", "NIL QSO from-to AA5KC-W5RAW exchs:KINN-MLEN mode:PH band:20 Sept 19th 1852Z\\n", "NIL QSO from-to AA5KC-N7EPD exchs:KINN-WA mode:PH band:20 Sept 19th 1856Z\\n"],
# #     "exchange": '',
# #     "final_score": 8466,
# #     "grid_square": '',
# #     "invalid_exchange_qsos": 0,
# #     "is_valid": '',
# #     "location": "TX",
# #     "mobile_activation_counts": {},
# #     "mobile_counties_worked": {},
# #     "mtb_mobile_points": 0,
# #     "name": "David Loftus",
# #     "nil_calls": [],
# #     "nils": 3,
# #     "other_bad_qsos": 0,
# #     "overlay": '',
# #     "ph_qsos": 29,
# #     "provinces_worked": [],
# #     "qso_points": 166,
# #     "qsos_by_band": {"160": 0, "80": 0, "40": 30, "20": 33, "15": 1, "10": 1, "6": 0, "2": 0},
# #     "qsos_by_hour": [9, 25, 7, 19, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #     "qsos_by_mode": {"PH": 29, "CW": 36, "RY": 0, "DG": 0},
# #     "ry_qsos": 0,
# #     "score_wo_bonus": 8466,
# #     "special_station_contacts": 0,
# #     "states_worked": {"AZ", "CA", "FL", "IA", "ID", "IL", "KS", "LA", "MO", "MS", "NC", "NH", "NJ", "NM", "NY", "OH", "OK", "OR", "SC", "TN", "UT", "WI"},
# #     "total_multipliers": 51,
# #     "total_qsos": 70,
# #     "uniques": 0,
# #     "updated_at": "2026-10-08T18:54:53.653180",
# #     "valid_qsos": 69,
# #     "warnings": [],
# #     "worked_special_station": '',
# #     "year": "2026"
# # }
# # xyzzy = 
# # foo = serialize_result(result)
# # pprint(foo)
# # bar = deserialize_result(foo)
# # pprint(bar)
