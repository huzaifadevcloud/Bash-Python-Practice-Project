#!/bin/bash

# Directory to back up
SOURCE_DIR="/opt/myapp/config"
# Where to store backups
BACKUP_DIR="/opt/myapp/backups"
# Timestamp format
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
# Backup filename
BACKUP_FILE="config_backup_$TIMESTAMP.tar.gz"
# Log file
LOG_FILE="/var/log/backup_restore.log"

mkdir -p "$BACKUP_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

# Backup function
backup() {
    echo "[$TIMESTAMP] Starting backup..." >> "$LOG_FILE"
    tar -czf "$BACKUP_DIR/$BACKUP_FILE" -C "$SOURCE_DIR" . && \
    echo "[$TIMESTAMP] Backup successful: $BACKUP_FILE" >> "$LOG_FILE" || \
    echo "[$TIMESTAMP] Backup failed." >> "$LOG_FILE"
}

# Restore function (latest backup)
restore() {
    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/config_backup_*.tar.gz 2>/dev/null | head -n 1)
    if [ -f "$LATEST_BACKUP" ]; then
        echo "[$TIMESTAMP] Restoring from $LATEST_BACKUP..." >> "$LOG_FILE"
        tar -xzf "$LATEST_BACKUP" -C "$SOURCE_DIR" && \
        echo "[$TIMESTAMP] Restore completed." >> "$LOG_FILE" || \
        echo "[$TIMESTAMP] Restore failed." >> "$LOG_FILE"
    else
        echo "[$TIMESTAMP] No backup file found to restore." >> "$LOG_FILE"
    fi
}

# Main logic
if [[ "$1" == "backup" ]]; then
    backup
elif [[ "$1" == "restore" ]]; then
    restore
else
    echo "Usage: $0 {backup|restore}"
fi
