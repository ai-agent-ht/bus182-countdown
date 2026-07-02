#!/bin/bash
# Extract token and check GitHub Pages status
cd /opt/data/grocery-ledger
TOKEN=$(git remote -v | head -1 | grep -oP 'ghp_[^@]+')
echo "Token length: ${#TOKEN}"

curl -s -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/ai-agent-ht/bus182-countdown/pages" \
  | python3 -m json.tool 2>&1 | head -15