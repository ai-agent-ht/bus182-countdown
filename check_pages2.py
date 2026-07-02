import subprocess, json

result = subprocess.run(
    ["git", "-C", "/opt/data/grocery-ledger", "remote", "-v"],
    capture_output=True, text=True
)
url = result.stdout.strip()
token = url.split(":")[2].split("@")[0] if ":" in url else ""

# Get pages build details
result = subprocess.run(
    ["curl", "-s", "-H", f"Authorization: token {token}",
     "https://api.github.com/repos/ai-agent-ht/bus182-countdown/pages/builds?per_page=1"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
if d:
    b = d[0]
    print("Status:", b.get("status"))
    print("Error:", b.get("error", {}).get("message", "none"))
    print("Commit:", b.get("commit"))

# Get recent workflow runs
result = subprocess.run(
    ["curl", "-s", "-H", f"Authorization: token {token}",
     "https://api.github.com/repos/ai-agent-ht/bus182-countdown/actions/runs?per_page=2"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
for run in d.get("workflow_runs", []):
    print(f'Workflow: {run.get("name")}, Status: {run.get("status")}, Conclusion: {run.get("conclusion")}')