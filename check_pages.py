import subprocess, json

# Get token
result = subprocess.run(
    ["git", "-C", "/opt/data/grocery-ledger", "remote", "-v"],
    capture_output=True, text=True
)
url = result.stdout.strip()
token = url.split(":")[2].split("@")[0] if ":" in url else ""

# Check workflow runs
result = subprocess.run(
    ["curl", "-s", "-H", f"Authorization: token {token}",
     "https://api.github.com/repos/ai-agent-ht/bus182-countdown/actions/runs?per_page=3"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
print("=== Workflows ===")
for run in d.get("workflow_runs", []):
    print(f'  {run["name"]}: {run["status"]} / {run.get("conclusion","?")}')

# Check pages build
result = subprocess.run(
    ["curl", "-s", "-H", f"Authorization: token {token}",
     "https://api.github.com/repos/ai-agent-ht/bus182-countdown/pages/builds?per_page=3"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
print("=== Pages Builds ===")
for b in d:
    print(f'  Status: {b.get("status")}, Created: {b.get("created_at","?")[:19]}')

# Check pages status
result = subprocess.run(
    ["curl", "-s", "-H", f"Authorization: token {token}",
     "https://api.github.com/repos/ai-agent-ht/bus182-countdown/pages"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
print(f'Pages status: {d.get("status")}, URL: {d.get("html_url")}')