import json, subprocess

# Get the latest failed run
result = subprocess.run(
    ["curl", "-s", "-H", "Accept: application/vnd.github+json", 
     "https://api.github.com/repos/ai-agent-ht/bus182-countdown/actions/runs?per_page=1&status=completed&branch=main"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
runs = [r for r in d.get("workflow_runs", []) if r.get("conclusion") == "failure"]
if not runs:
    # Maybe the latest is still running
    for r in d.get("workflow_runs", []):
        print(f"  {r['name']} status={r['status']} conclusion={r.get('conclusion','?')}")
    exit()

run = runs[0]
print(f"Run ID: {run['id']}")
print(f"Head SHA: {run['head_sha']}")
print(f"Check suite URL: {run.get('check_suite_url','')}")

# Try to get the logs directly
logs_result = subprocess.run(
    ["curl", "-s", "-L", f"https://api.github.com/repos/ai-agent-ht/bus182-countdown/actions/runs/{run['id']}/logs"],
    capture_output=True, text=True
)
print(f"Logs status: {logs_result.returncode}")
print(f"Logs preview (first 3000 chars):")
print(logs_result.stdout[:3000])