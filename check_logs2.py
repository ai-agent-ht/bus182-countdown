import json, subprocess

# Get the latest failed run
result = subprocess.run(
    ["curl", "-s", "https://api.github.com/repos/ai-agent-ht/bus182-countdown/actions/runs?per_page=1&status=completed&branch=main&conclusion=failure"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
if not d.get("workflow_runs"):
    print("No failed runs found")
    for r in d.get("workflow_runs", []):
        print(f"  {r['name']} - {r.get('conclusion')}")
    exit()

run = d["workflow_runs"][0]
print(f"Run: {run['id']} - {run['name']} - {run.get('conclusion')}")

# Get the job
jresult = subprocess.run(["curl", "-s", run["jobs_url"]], capture_output=True, text=True)
jd = json.loads(jresult.stdout)
for job in jd.get("jobs", []):
    print(f"Job: {job['name']} - {job['status']} - {job.get('conclusion')}")
    # Get the failed step logs
    for step in job.get("steps", []):
        if step.get("conclusion") == "failure":
            print(f"  Failed step: {step['name']} (number {step['number']})")
            # Try to get logs for this job
            logs_url = job.get("logs_url", "")
            if logs_url:
                log_result = subprocess.run(["curl", "-s", logs_url], capture_output=True, text=True)
                # Print the last 30 lines of the log
                lines = log_result.stdout.split("\n")
                for line in lines[-30:]:
                    print(f"  | {line}")