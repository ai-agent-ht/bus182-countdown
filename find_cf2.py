import subprocess, json

result = subprocess.run(
    ["git", "-C", "/opt/data/grocery-ledger", "remote", "-v"],
    capture_output=True, text=True
)
url = result.stdout.strip()
token = url.split(":")[2].split("@")[0] if ":" in url else ""

# Get the deploy step log directly
result = subprocess.run(
    ["curl", "-s", "-L",
     f"https://api.github.com/repos/ai-agent-ht/grocery-ledger/actions/jobs/84786039505/logs"],
    capture_output=True, text=True,
    env={"GITHUB_TOKEN": token}
)
# Print first 2000 chars of logs
logs = result.stdout
# Find account_id, project name, deployment URL in logs
import re
for pattern in [r'account[=_\s]+([a-f0-9]{32})', r'([a-f0-9]{32})', r'pages\.dev', r'grocery-ledger']:
    matches = re.findall(pattern, logs, re.IGNORECASE)
    for m in matches[:5]:
        print(f"Found: {m}")

print("\n--- First 1500 chars ---")
print(logs[:1500])