#!/bin/bash

# Log file for audit results
LOG_FILE="/var/log/user_audit.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Start audit log
echo "[$DATE] Starting user account audit..." >> "$LOG_FILE"

# 1. List normal users with login shells
echo "Normal users with login shells:" >> "$LOG_FILE"
awk -F: '$3 >= 1000 && $7 != "/usr/sbin/nologin" && $7 != "/bin/false" {print $1}' /etc/passwd >> "$LOG_FILE"

# 2. System accounts (UID < 1000)
echo -e "\nSystem accounts:" >> "$LOG_FILE"
awk -F: '$3 < 1000 {print $1}' /etc/passwd >> "$LOG_FILE"

# 3. Users without passwords
echo -e "\nUsers without passwords:" >> "$LOG_FILE"
awk -F: '($2 == "!" || $2 == "*" || $2 == "!!") {print $1}' /etc/shadow 2>/dev/null >> "$LOG_FILE"

# 4. Recently added users (last 7 days)
echo -e "\nRecently added users (created in last 7 days):" >> "$LOG_FILE"
find /home -maxdepth 1 -type d -ctime -7 -exec basename {} \; >> "$LOG_FILE"

echo "[$DATE] Audit completed." >> "$LOG_FILE"
