#!/usr/bin/env python3

import subprocess
import datetime
import os

SERVICE = "nginx"
LOG_FILE = "/var/log/service_health.log"

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

def is_service_running(service):
    result = subprocess.run(["systemctl", "is-active", "--quiet", service])
    return result.returncode == 0

log("Checking service health...")

if is_service_running(SERVICE):
    log(f"{SERVICE} is running.")
else:
    log(f"ALERT: {SERVICE} is NOT running. Attempting to restart...")
    restart = subprocess.run(["systemctl", "restart", SERVICE])
    if is_service_running(SERVICE):
        log(f"SUCCESS: {SERVICE} restarted successfully.")
    else:
        log(f"ERROR: Failed to restart {SERVICE}.")
