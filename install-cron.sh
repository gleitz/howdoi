#!/bin/bash
# Install howdou cron jobs for automatic reindexing

set -e

USER_HOME="/home/$(whoami)"
CRON_LINES="# howdou reindex jobs
*/5 * * * * . ${USER_HOME}/.bash_aliases; howdou --action=reindex
0 6 * * * . ${USER_HOME}/.bash_aliases; howdou --action=reindex --force"

# Check if already installed
if crontab -l 2>/dev/null | grep -q "howdou --action=reindex"; then
    echo "howdou cron jobs already installed"
    exit 0
fi

# Append to existing crontab (or create new one)
(crontab -l 2>/dev/null || true; echo "$CRON_LINES") | crontab -

echo "Installed howdou cron jobs:"
echo "  - Every 5 min: incremental reindex"
echo "  - Daily 6am: full reindex"
