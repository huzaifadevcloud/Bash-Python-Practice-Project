#!/usr/bin/env python3

import shutil
import datetime
import os

THRESHOLD = 80
LOG_FILE = "/var/log/disk_usage.log"

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

log("Running disk usage check...")

partitions = shutil.disk_usage('/')
total, used, free = partitions
percent_used = used * 100 // total

if percent_used > THRESHOLD:
    message = f"Warning: Disk usage is {percent_used}%"
    log(message)
    print(f"ALERT: {message}")
else :
    message = (f"Disk usage is in Normal state {percent_used}% ")
    log(message)

