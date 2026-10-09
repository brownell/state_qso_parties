#!/bin/bash
# Louisiana QSO Party - Docker Restore Script
#
# Restores Docker volumes from backup
#
# Usage: ./restore.sh BACKUP_DATE
# Example: ./restore.sh 20260203_120000

set -e

# Check argument
if [ -z "$1" ]; then
    echo "Usage: ./restore.sh BACKUP_DATE"
    echo ""
    echo "Available backups:"
    ls -1 backups/ 2>/dev/null || echo "  (none found)"
    exit 1
fi

BACKUP_DIR="backups/$1"

# Check if backup exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Error: Backup directory not found: $BACKUP_DIR"
    echo ""
    echo "Available backups:"
    ls -1 backups/
    exit 1
fi

echo "================================================"
echo "Louisiana QSO Party - Docker Restore"
echo "================================================"
echo "Restoring from: $BACKUP_DIR"
echo ""

# Show manifest
if [ -f "$BACKUP_DIR/manifest.txt" ]; then
    echo "Backup manifest:"
    cat "$BACKUP_DIR/manifest.txt"
    echo ""
fi

# Confirm
read -p "Are you sure you want to restore? This will OVERWRITE current data! (yes/no): " -r
echo
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Restore cancelled."
    exit 1
fi

# Stop containers
echo "Stopping containers..."
docker-compose down

# Function to restore a volume
restore_volume() {
    local volume_name=$1
    local backup_file=$2
    
    if [ ! -f "$BACKUP_DIR/$backup_file" ]; then
        echo "⚠ Warning: Backup file not found: $backup_file (skipping)"
        return 0
    fi
    
    echo "Restoring volume: $volume_name"
    docker run --rm \
        -v "$volume_name:/data" \
        -v "$(pwd)/$BACKUP_DIR:/backup" \
        alpine sh -c "rm -rf /data/* /data/..?* /data/.[!.]* 2>/dev/null || true; tar xzf /backup/$backup_file -C /data"
    
    if [ $? -eq 0 ]; then
        echo "✓ $volume_name restored"
    else
        echo "✗ Failed to restore $volume_name"
        return 1
    fi
}

# Restore database
restore_volume "txqp-database" "database.tar.gz"

# Restore logs
restore_volume "txqp-logs" "logs.tar.gz"

# Restore HTML results
restore_volume "txqp-results" "results.tar.gz"

# Start containers
echo ""
echo "Starting containers..."
docker-compose up -d

echo ""
echo "================================================"
echo "Restore complete!"
echo "================================================"
echo ""
docker-compose ps
