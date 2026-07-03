import json, sys, subprocess

result = subprocess.run(
    ["curl", "-s", "https://api.github.com/repos/ai-agent-ht/bus182-countdown/actions/runs?status=completed&branch=main"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
for r in d.get("workflow_runs", []):
    if "Cloudflare" in r["name"]:
        print(f"Run ID: {r['id']}")
        print(f"Conclusion: {r.get('conclusion')}")
        print(f"Jobs URL: {r['jobs_url']}")
        # Fetch job details
        jresult = subprocess.run(["curl", "-s", r["jobs_url"]], capture_output=True, text=True)
        jd = json.loads(jresult.stdout)
        for job in jd.get("jobs", []):
            print(f"  Job: {job['name']} - {job['status']} - {job.get('conclusion')}")
            for step in job.get("steps", []):
                print(f"    Step: {step['name']} - {step['status']} - {step.get('conclusion')}")
                if step.get("conclusion") == "failure":
                    # Try to get the log
                    pass
        break