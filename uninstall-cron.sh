#!/bin/bash
# Remove howdou cron jobs

set -e

# Check if any howdou jobs exist
if ! crontab -l 2>/dev/null | grep -q "howdou --action=reindex"; then
    echo "No howdou cron jobs found"
    exit 0
fi

# Remove howdou lines from crontab
crontab -l 2>/dev/null | grep -v "howdou" | crontab -

echo "Removed howdou cron jobs"
