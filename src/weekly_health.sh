#!/bin/bash
# Weekly /health report: pull last week's numbers, then deploy taliferro.tech.
# Run by ~/Library/LaunchAgents/tech.taliferro.health.plist every Monday 00:10.
# Log: ~/Library/Logs/taliferro-health.log. A macOS notification fires on failure.
set -euo pipefail
export PATH="/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.9/bin:/usr/bin:/bin"
cd "$(dirname "$0")/.."

fail() { osascript -e 'display notification "Weekly health report failed. See ~/Library/Logs/taliferro-health.log" with title "Taliferro Health"'; }
trap fail ERR

echo "=== $(date) ==="
# 3.9 explicitly: /usr/local/bin/python3 is 3.11, which has no CA certificates installed.
/Library/Frameworks/Python.framework/Versions/3.9/bin/python3 src/health_pull.py
firebase deploy --only hosting:taliferro-tech --non-interactive
echo "done"
