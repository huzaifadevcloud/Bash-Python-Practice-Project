#!/bin/bash

SERVICE="nginx"
LOG_FILE="/var/log/service_health.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

mkdir -p "$(dirname "$LOG_FILE")"

if systemctl is-active --quiet "$SERVICE"; then
    echo "[$DATE] $SERVICE is running." >> "$LOG_FILE"
else
    echo "[$DATE] ALERT: $SERVICE is NOT running. Attempting to restart..." >> "$LOG_FILE"
    systemctl restart "$SERVICE"
    if systemctl is-active --quiet "$SERVICE"; then
        echo "[$DATE] SUCCESS: $SERVICE restarted successfully." >> "$LOG_FILE"
    else
        echo "[$DATE] ERROR: Failed to restart $SERVICE." >> "$LOG_FILE"
    fi
fi
