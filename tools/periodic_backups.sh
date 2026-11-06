#!/bin/bash
# backup_with_cleanup.sh

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/brownell/Documents/fly_backups"

BACKUP_DB_FILE="$BACKUP_DIR/db/laqp_$TIMESTAMP.db"

BACKUP_LOGS_DIR_2026="$BACKUP_DIR/logs/2026_$TIMESTAMP/"
LOGS_2026_REMOTE_DIR="data/batch_input/2026"

mkdir -p "$BACKUP_DIR"
mkdir -p "$BACKUP_LOGS_DIR_2026"
mkdir -p "$BACKUP_DIR/db/"
mkdir -p "$LOGS_2026_REMOTE_DIR"

# Get the Database backup from REMOTE
flyctl ssh sftp get data/database/laqp.db "$BACKUP_DB_FILE"
find "$BACKUP_DIR + /db/" -name "laqp_*.db" -mtime +10 -delete
echo "✅ Database backup complete in: $BACKUP_DB_FILE"
echo "📂 Current database backups in $BACKUP_DIR/db/"
ls -lht "$BACKUP_DIR/db/"

flyctl ssh console << EOF
echo "✅ Now backing up all the log files for 2026 from REMOTE and saving to $BACKUP_LOGS_DIR_2026"
echo "📂 Tar'ing logs for 2026 on REMOTE..."
tar -czf temp/contest_logs_2026.tar.gz -C $LOGS_2026_REMOTE_DIR .
exit
EOF

flyctl ssh sftp shell << EOF
echo "📤 Getting logs tar file for 2026 from REMOTE"
get temp/contest_logs_2026.tar.gz temp/contest_logs_2026.tar.gz
EOF

echo "📂 Extracting logs for 2026 locally into BACKUP_LOGS_DIR"
tar -xzf temp/contest_logs_2026.tar.gz BACKUP_LOGS_DIR_2026 --strip-components=1
rm temp/contest_logs_2026.tar.gz
echo "✅ Extracted files:"
ls -lh

echo "🧹 Cleaning up local archive..."
rm temp/contest_logs.tar.gz