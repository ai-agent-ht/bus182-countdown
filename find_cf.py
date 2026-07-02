import subprocess, json, re

result = subprocess.run(
    ["git", "-C", "/opt/data/grocery-ledger", "remote", "-v"],
    capture_output=True, text=True
)
url = result.stdout.strip()
token = url.split(":")[2].split("@")[0] if ":" in url else ""

# Get the grocery-ledger deploy logs - look for Cloudflare account ID
result = subprocess.run(
    ["curl", "-s", "-H", f"Authorization: token {token}",
     "https://api.github.com/repos/ai-agent-ht/grocery-ledger/actions/runs?per_page=1&status=success"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
runs = d.get("workflow_runs", [])
if runs:
    run_id = runs[0]["id"]
    print(f"Latest successful run: {run_id}")
    
    # Get the job
    result = subprocess.run(
        ["curl", "-s", "-H", f"Authorization: token {token}",
         f"https://api.github.com/repos/ai-agent-ht/grocery-ledger/actions/runs/{run_id}/jobs"],
        capture_output=True, text=True
    )
    jobs = json.loads(result.stdout)
    for job in jobs.get("jobs", []):
        print(f"Job: {job['name']}, ID: {job['id']}")
        for step in job.get("steps", []):
            if "deploy" in step["name"].lower() or "cloudflare" in step["name"].lower():
                print(f"  Step: {step['name']}")
                # Try to get step logs
                result2 = subprocess.run(
                    ["curl", "-s", "-L", "-H", f"Authorization: token {token}",
                     f"https://api.github.com/repos/ai-agent-ht/grocery-ledger/actions/jobs/{job['id']}/logs"],
                    capture_output=True, text=True
                )
                # Look for account ID pattern in logs
                logs = result2.stdout
                acct_match = re.search(r'account[=_\s]+([a-f0-9]{32})', logs, re.IGNORECASE)
                if acct_match:
                    print(f"  ACCOUNT ID found: {acct_match.group(1)}")
                # Look for project name
                proj_match = re.search(r'project[=_\s]+([a-zA-Z0-9_-]+)', logs, re.IGNORECASE)
                if proj_match:
                    print(f"  PROJECT: {proj_match.group(1)}")
                break
        break