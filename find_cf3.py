import subprocess, json, re

result = subprocess.run(
    ["git", "-C", "/opt/data/grocery-ledger", "remote", "-v"],
    capture_output=True, text=True
)
url = result.stdout.strip()
token = url.split(":")[2].split("@")[0] if ":" in url else ""

# Need to use Authorization header
result = subprocess.run(
    ["curl", "-s", "-L",
     "-H", f"Authorization: token {token}",
     "-H", "Accept: application/vnd.github+json",
     f"https://api.github.com/repos/ai-agent-ht/grocery-ledger/actions/jobs/84786039505/logs"],
    capture_output=True, text=True
)
logs = result.stdout
# Look for Cloudflare info
for pattern in [r'account[_\- ]?[_\-]?([a-f0-9]{32})', r'(?i)cloudflare.*?account.*?([a-f0-9]{32})',
                r'https://[a-f0-9-]+\.pages\.dev', r'grocery-ledger\.[a-z]+']:
    matches = re.findall(pattern, logs)
    for m in matches[:3]:
        print(f"Pattern '{pattern}': {m}")

# Print first part
print("\n--- First 2000 chars ---")
print(logs[:2000])