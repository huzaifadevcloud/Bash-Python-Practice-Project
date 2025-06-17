#!/usr/bin/env python3

import os
import shutil
import tarfile
import datetime

SOURCE_DIR = "/opt/myapp/config"
BACKUP_DIR = "/opt/myapp/backups"
LOG_FILE = "/var/log/backup_restore.log"

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(msg):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        f.write(f"[{timestamp}] {msg}\n")

def backup():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(BACKUP_DIR, f"config_backup_{timestamp}.tar.gz")
    try:
        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(SOURCE_DIR, arcname=".")
        log(f"Backup successful: {backup_file}")
    except Exception as e:
        log(f"Backup failed: {str(e)}")

def restore():
    try:
        backups = sorted(
            [f for f in os.listdir(BACKUP_DIR) if f.endswith(".tar.gz")],
            reverse=True
        )
        if backups:
            latest = os.path.join(BACKUP_DIR, backups[0])
            with tarfile.open(latest, "r:gz") as tar:
                tar.extractall(path=SOURCE_DIR)
            log(f"Restore successful from: {latest}")
        else:
            log("No backup files found to restore.")
    except Exception as e:
        log(f"Restore failed: {str(e)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2 or sys.argv[1] not in ("backup", "restore"):
        print("Usage: python3 backup_restore.py {backup|restore}")
    elif sys.argv[1] == "backup":
        backup()
    else:
        restore()
