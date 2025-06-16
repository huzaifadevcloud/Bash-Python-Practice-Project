#!/bin/bash

# =====================================================
# Script Name : Disk Usage Alert Script
# Description : Monitors disk usage and logs alerts
# Author      : Huzaifa Hatim
# Version     : 1.0
# Date        : 2025-06-14
# =====================================================

set -o errexit  # Exit if any command fails
set -o nounset  # Treat unset variables as error
set -o pipefail # Catch errors in piped commands
#set -x          # Uncomment for debug: print commands during execution

THRESHOLD=80
LOG_FILE="/var/log/disk_usage.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

mkdir -p "$(dirname "$LOG_FILE")"

echo "[$DATE] Running disk usage check..." >> "$LOG_FILE"

disk_usage=$(df -h --output=source,pcent,target | tail -n +2)

echo "$disk_usage" | while read -r line; do
  usage=$(echo "$line" | awk '{print $2}' | tr -d '%')
  if (( usage > THRESHOLD )); then
    echo "[$DATE] Warning: High disk usage on $line" >> "$LOG_FILE"
    echo "ALERT: High usage on $line"
  else
    echo "✅ [$DATE] Usage normal on $line" >> "$LOG_FILE"
  fi
done
