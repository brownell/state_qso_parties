#!/bin/bash
# Texas QSO Party - Docker Backup Script
#
# Backs up all Docker volumes to timestamped directory
#
# Usage: ./backup.sh

set -e

# Configuration
BACKUP_BASE_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$BACKUP_BASE_DIR/$DATE"

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "================================================"
echo "Texas QSO Party - Docker Backup"
echo "================================================"
echo "Backup directory: $BACKUP_DIR"
echo ""

# Function to backup a volume
backup_volume() {
    local volume_name=$1
    local backup_file=$2
    
    echo "Backing up volume: $volume_name"
    docker run --rm \
        -v "$volume_name:/data" \
        -v "$(pwd)/$BACKUP_DIR:/backup" \
        alpine tar czf "/backup/$backup_file" -C /data .
    
    if [ $? -eq 0 ]; then
        echo "✓ $backup_file created"
    else
        echo "✗ Failed to backup $volume_name"
        return 1
    fi
}

# Backup database
backup_volume "txqp-database" "database.tar.gz"

# Backup logs
backup_volume "txqp-logs" "logs.tar.gz"

# Backup HTML results
backup_volume "txqp-results" "results.tar.gz"

# Create backup manifest
cat > "$BACKUP_DIR/manifest.txt" << EOF
Texas QSO Party - Backup Manifest
======================================
Date: $(date)
Hostname: $(hostname)

Volumes:
- database.tar.gz (txqp-database)
- logs.tar.gz (txqp-logs)
- results.tar.gz (txqp-results)

Container Status:
EOF

docker-compose ps >> "$BACKUP_DIR/manifest.txt"

echo ""
echo "================================================"
echo "Backup complete!"
echo "================================================"
echo "Location: $BACKUP_DIR"
echo ""
ls -lh "$BACKUP_DIR"
echo ""
echo "To restore, run: ./restore.sh $DATE"
