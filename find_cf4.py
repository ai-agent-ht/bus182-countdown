import subprocess, json, re

result = subprocess.run(
    ["git", "-C", "/opt/data/grocery-ledger", "remote", "-v"],
    capture_output=True, text=True
)
url = result.stdout.strip()
token = url.split(":")[2].split("@")[0] if ":" in url else ""

result = subprocess.run(
    ["curl", "-s", "-L",
     "-H", f"Authorization: token {token}",
     "-H", "Accept: application/vnd.github+json",
     f"https://api.github.com/repos/ai-agent-ht/grocery-ledger/actions/jobs/84786039505/logs"],
    capture_output=True, text=True
)
logs = result.stdout

# Search for key terms
for keyword in ['pages.dev', 'account_id', 'accountId', 'project_name', 'Deployed', 'Success', 'wrangler']:
    for line in logs.split('\n'):
        if keyword.lower() in line.lower():
            print(line[:200])