#!/bin/bash

# CheckMK Local Check - Count Sent Emails from Postfix Logs with Thresholds

# Define the log file path
LOG_PATH="/var/log/mail.log*"

# Define thresholds
WARN_THRESHOLD=1000
CRIT_THRESHOLD=5000

# Toggle for adding prefix
PREFIX_ENABLED=1  # 1 = Prefix "Serancon: " enabled, 0 = Prefix disabled

# Count the number of sent emails
EMAIL_COUNT=$(zgrep "status=sent" $LOG_PATH | wc -l)

# Determine the status based on thresholds
if [ $EMAIL_COUNT -ge $CRIT_THRESHOLD ]; then
    STATUS=2  # CRIT
    STATUS_TEXT="CRITICAL"
elif [ $EMAIL_COUNT -ge $WARN_THRESHOLD ]; then
    STATUS=1  # WARN
    STATUS_TEXT="WARNING"
else
    STATUS=0  # OK
    STATUS_TEXT="OK"
fi

# Define service name with optional prefix
BASE_SERVICE_NAME="Postfix Email Sent by CheckMK"
if [ "$PREFIX_ENABLED" -eq 1 ]; then
    SERVICE_NAME="Serancon: $BASE_SERVICE_NAME"
else
    SERVICE_NAME="$BASE_SERVICE_NAME"
fi

# Output in CheckMK Local Check format
echo "<<<local>>>"
echo "$STATUS \"$SERVICE_NAME\" count=$EMAIL_COUNT;$WARN_THRESHOLD;$CRIT_THRESHOLD Sent emails: $EMAIL_COUNT - $STATUS_TEXT"
