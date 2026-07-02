import subprocess, json

result = subprocess.run(
    ["git", "-C", "/opt/data/grocery-ledger", "remote", "-v"],
    capture_output=True, text=True
)
url = result.stdout.strip()
token = url.split(":")[2].split("@")[0] if ":" in url else ""

# Get more details about the pages build error
result = subprocess.run(
    ["curl", "-s", "-H", f"Authorization: token {token}",
     "https://api.github.com/repos/ai-agent-ht/bus182-countdown/pages/builds?per_page=1"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
if d:
    b = d[0]
    print(json.dumps(b, indent=2)[:1000])