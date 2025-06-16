#!/bin/bash

# Path to the log file that needs monitoring
LOG_FILE="/var/log/app/bash_log.log"

# Max log size in MB before rotation is triggered
MAX_SIZE_MB=5

# Get current date and time
DATE=$(date '+%Y-%m-%d_%H-%M-%S')

# Directory where rotated logs will be stored
ARCHIVE_DIR="/var/log/app/archive"

# Create archive directory if it doesn't exist
mkdir -p "$ARCHIVE_DIR"

# Check if log file exists
if [ -f "$LOG_FILE" ]; then
    # Get file size in MB using du
    SIZE=$(du -m "$LOG_FILE" | cut -f1)

    if [ "$SIZE" -ge "$MAX_SIZE_MB" ]; then
        # Rotate and compress the log file
        mv "$LOG_FILE" "$ARCHIVE_DIR/application_$DATE.log"
        gzip "$ARCHIVE_DIR/application_$DATE.log"
        touch "$LOG_FILE"  # Create a new empty log file
        echo "[$DATE] Log file rotated. Old file moved to archive." >> "$LOG_FILE"
    fi
else
    # If log file doesn't exist, create one
    touch "$LOG_FILE"
    echo "[$DATE] Created new log file." >> "$LOG_FILE"
fi

