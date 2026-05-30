import subprocess
import requests
import os
from flask import Flask, jsonify, send_from_directory
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv()

app = Flask(__name__, static_folder='static')

GITHUB_USER = os.getenv('GITHUB_USERNAME', 'YOUR_USERNAME')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'YOUR_REPO')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
SLACK_TOKEN = os.getenv('SLACK_TOKEN', '')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL_ID', '')

HEADERS_GH = {"Authorization": f"token {GITHUB_TOKEN}"}

def run_coral(query):
    try:
        result = subprocess.run(
            ['coral', 'sql', '--output', 'json', query],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return None, result.stderr.strip()
        output = result.stdout.strip()
        if not output:
            return [], None
        import json
        rows = json.loads(output)
        return rows, None
    except FileNotFoundError:
        return None, "Coral CLI not found."
    except subprocess.TimeoutExpired:
        return None, "Coral query timed out."
    except Exception as e:
        return None, str(e)

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_duplicates(issues):
    duplicates = []
    for i in range(len(issues)):
        for j in range(i+1, len(issues)):
            score = similar(issues[i]['title'], issues[j]['title'])
            if score > 0.6:
                duplicates.append({
                    'issue1': f"#{issues[i]['number']} {issues[i]['title']}",
                    'issue2': f"#{issues[j]['number']} {issues[j]['title']}",
                    'similarity': f"{int(score*100)}%"
                })
    return duplicates

def draft_release_notes(prs):
    if not prs:
        return "No merged PRs found to generate release notes."
    notes = "## Release Notes\n\n"
    notes += "### What's Changed\n\n"
    for pr in prs:
        notes += f"- {pr.get('title', 'Untitled')} (#{pr.get('number', '?')}) by @{pr.get('user', {}).get('login', 'unknown')}\n"
    notes += f"\n**Full Changelog**: https://github.com/{GITHUB_USER}/{GITHUB_REPO}/commits/main"
    return notes

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/attention')
def get_attention():
    errors = []

    # --- GitHub Issues via Coral ---
    issues_q = f"SELECT number, title, state, created_at, user_login FROM github.issues WHERE owner='{GITHUB_USER}' AND repo='{GITHUB_REPO}' AND state='open' ORDER BY created_at DESC LIMIT 15"
    issues, err = run_coral(issues_q)
    if err:
        # Fallback to GitHub API
        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/issues?state=open&per_page=15"
        res = requests.get(url, headers=HEADERS_GH)
        issues = [{"number": i["number"], "title": i["title"], "user": i["user"]["login"], "url": i["html_url"]} for i in res.json() if "pull_request" not in i]
        errors.append(f"Issues: {err}")

    # --- Duplicate Detection ---
    duplicates = find_duplicates(issues) if issues else []

    # --- Merged PRs via Coral ---
    prs_q = f"SELECT number, title, merged_at, user_login FROM github.pulls WHERE owner='{GITHUB_USER}' AND repo='{GITHUB_REPO}' AND state='closed' ORDER BY merged_at DESC LIMIT 10"
    prs, err = run_coral(prs_q)
    if err:
        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/pulls?state=closed&per_page=10"
        res = requests.get(url, headers=HEADERS_GH)
        prs = [{"number": p["number"], "title": p["title"], "user": p["user"], "merged_at": p.get("merged_at", "")} for p in res.json() if p.get("merged_at")]
        errors.append(f"PRs: {err}")

    # --- Release Notes ---
    release_notes = draft_release_notes(prs)

    # --- Cross-source JOIN via Coral ---
    cross_join = []
    join_q = f"SELECT g.number, g.title FROM github.issues g WHERE g.owner='{GITHUB_USER}' AND g.repo='{GITHUB_REPO}' AND g.state='open' LIMIT 5"
    cross_join, err = run_coral(join_q)
    if err:
        cross_join = []

    # --- Slack ---
    slack = []
    if SLACK_TOKEN and SLACK_CHANNEL:
        slack_q = f"SELECT ts, text, user_id FROM slack.messages WHERE channel_id='{SLACK_CHANNEL}' LIMIT 8"
        slack, err = run_coral(slack_q)
        if err:
            url = "https://slack.com/api/conversations.history"
            res = requests.get(url, headers={"Authorization": f"Bearer {SLACK_TOKEN}"}, params={"channel": SLACK_CHANNEL, "limit": 8})
            slack = [{"text": m.get("text", ""), "user": m.get("user", "")} for m in res.json().get("messages", [])]
            errors.append(f"Slack: {err}")

    response = {
        'issues': issues or [],
        'prs': prs or [],
        'duplicates': duplicates,
        'cross_join': cross_join or [],
        'slack': slack or [],
        'release_notes': release_notes,
        'status': 'ok'
    }

    if errors:
        response['warnings'] = errors

    return jsonify(response)

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'github_user': GITHUB_USER, 'repo': GITHUB_REPO})

if __name__ == '__main__':
    print("🏴‍☠️  Dev's First Mate starting...")
    print(f"   GitHub: {GITHUB_USER}/{GITHUB_REPO}")
    print(f"   Slack channel: {SLACK_CHANNEL}")
    print("   Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("PORT", 10000)))
