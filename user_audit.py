#!/usr/bin/env python3

import os
import datetime
import pwd
import spwd
import time

LOG_FILE = "/var/log/user_audit.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

log("Starting user account audit...")

# 1. Normal users with login shells (UID >= 1000)
log("\nNormal users with login shells:")
for p in pwd.getpwall():
    if p.pw_uid >= 1000 and p.pw_shell not in ("/usr/sbin/nologin", "/bin/false"):
        log(f"- {p.pw_name}")

# 2. System accounts (UID < 1000)
log("\nSystem accounts:")
for p in pwd.getpwall():
    if p.pw_uid < 1000:
        log(f"- {p.pw_name}")

# 3. Users without passwords
log("\nUsers without passwords:")
try:
    for u in spwd.getspall():
        if u.sp_pwd in ("!", "*", "!!"):
            log(f"- {u.sp_nam}")
except PermissionError:
    log("Permission denied to read /etc/shadow. Run as root.")

# 4. Recently added users (home directories created in last 7 days)
log("\nRecently added users (home dirs in last 7 days):")
now = time.time()
for user_dir in os.listdir("/home"):
    full_path = os.path.join("/home", user_dir)
    if os.path.isdir(full_path):
        created_time = os.path.getctime(full_path)
        if now - created_time < 7 * 86400:
            log(f"- {user_dir}")

log("Audit completed.")
