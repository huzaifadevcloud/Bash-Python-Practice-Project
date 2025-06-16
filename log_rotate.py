#!/usr/bin/env python3

import os
import shutil
import gzip
import datetime

# Define log file path and archive directory
LOG_FILE = "/var/log/app/application.log"
ARCHIVE_DIR = "/var/log/app/archive"
MAX_SIZE_MB = 5

# Create archive directory if it doesn't exist
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Get current timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Check if log file exists
if os.path.isfile(LOG_FILE):
    # Get file size in MB
    size_mb = os.path.getsize(LOG_FILE) / (1024 * 1024)

    if size_mb >= MAX_SIZE_MB:
        # Construct new archive file path
        archive_name = f"application_{timestamp}.log"
        archive_path = os.path.join(ARCHIVE_DIR, archive_name)

        # Move and compress the log file
        shutil.move(LOG_FILE, archive_path)
        with open(archive_path, 'rb') as f_in, gzip.open(archive_path + ".gz", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove(archive_path)  # Remove uncompressed copy

        # Create a fresh empty log file
        with open(LOG_FILE, 'w') as f:
            f.write(f"[{timestamp}] Log file rotated. Old file moved to archive.\n")
else:
    # Create the log file if it doesn't exist
    with open(LOG_FILE, 'w') as f:
        f.write(f"[{timestamp}] Created new log file.\n")
