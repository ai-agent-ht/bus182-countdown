import json, subprocess, sys

# Get the latest failed run
result = subprocess.run(
    ["curl", "-s", "https://api.github.com/repos/ai-agent-ht/bus182-countdown/actions/runs?per_page=1&status=completed&branch=main"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
run = d["workflow_runs"][0]

# Get job details
jresult = subprocess.run(["curl", "-s", run["jobs_url"]], capture_output=True, text=True)
jd = json.loads(jresult.stdout)
for job in jd.get("jobs", []):
    print(f"Job: {job['name']} - {job['status']} - {job.get('conclusion')}")
    for step in job.get("steps", []):
        icon = "✅" if step.get("conclusion") == "success" else "❌" if step.get("conclusion") == "failure" else "⏳"
        print(f"  {icon} {step['name']} - {step.get('conclusion', step['status'])}")
        if step.get("conclusion") == "failure":
            # Get the step logs
            logs_url = f"{run['jobs_url']}/{job['id']}/logs"
            # Let's try to get the annotation
            pass