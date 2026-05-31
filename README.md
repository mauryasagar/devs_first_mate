# 🏴‍☠️ Dev's First Mate
> WeMakeDevs Hackathon — Pirates of Coral-bean | Track 2: Personal Agent.


[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-devs--first--mate.onrender.com-blue)](https://devs-first-mate.onrender.com)
[![Powered by Coral](https://img.shields.io/badge/Powered_by-Coral_SQL-0A7C8A)](https://git.new/coral-wemakedevs-may26)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-yellow?logo=python)](https://python.org)
[![Flask Backend](https://img.shields.io/badge/Flask-Backend-black?logo=flask)](https://flask.palletsprojects.com)
[![Deployed on Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?logo=render)](https://render.com)

> *"What needs my attention today?"* — answered in one shot by joining GitHub and Slack through Coral (https://git.new/coral-wemakedevs-may26)'s unified SQL runtime.

---

## 👥 Crew

| Member | GitHub |
|---|---|
| Sagar Maurya | [@mauryasagar](https://github.com/mauryasagar) |
| Disha Sonowal | [@ritamonisonowal2](https://github.com/ritamonisonowal2) |

---

## 🎯 The Problem

Developers context-switch constantly — GitHub for issues and PRs, Slack for team discussions. There's no single place that says *"here's what actually matters right now."* Every tool requires separate logins, separate queries, and mental stitching.

---

## ✨ What Dev's First Mate Does

- 🐛 Triages open GitHub issues — ordered by recency so nothing falls through
- 🔁 Detects duplicate issues — using keyword matching to cut noise
- ✅ Drafts release notes — auto-generated from merged PRs
- 💬 Shows Slack activity — recent channel messages in context
- ⚡️ Cross-source JOIN — GitHub + Slack answered in one Coral SQL query
- 🤖 MCP Integration — AI agents can query your data directly via Coral's MCP server

---

## 📸 Screenshots

!Dev's First Mate Dashboard

<img width="600" height="300" alt="image" src="https://github.com/user-attachments/assets/c0c77e2b-e0ff-4064-b8ee-a3c60068afbb" />

## ⚡ Coral in Action

!Coral SQL Demo

<img width="600" height="300" alt="image" src="https://github.com/user-attachments/assets/646f0e7e-5835-4545-a73e-043eea251355" />


---

## 🛠️ Coral Features Used

| Feature | How We Used It |
|---|---|
| SQL Interface | coral sql "SELECT ..." to query GitHub & Slack |
| Cross-source JOIN | FROM github.issues JOIN slack.messages in a single query |
| Schema Learning | SELECT * FROM coral.tables to discover available data |
| MCP Server | coral mcp to expose data to AI agents |
| Caching | Built-in Coral caching on repeated queries for speed |
| Source Discovery | coral source discover to explore bundled sources |

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Data Runtime | Coral — Cross-source SQL |
| Backend | Flask (Python) |
| Frontend | HTML / CSS |
| Deployment | Render (Free tier) |

---

## ⚡️ Coral SQL Queries

### Open Issues Triage
```
SELECT number, title, state, created_at
FROM github.issues
WHERE repo = 'devs_first_mate' AND state = 'open'
ORDER BY created_at DESC
LIMIT 10
```

### Cross-source JOIN — GitHub + Slack in one query
```
SELECT g.number, g.title, s.text AS slack_discussion
FROM github.issues g
JOIN slack.messages s ON s.channel_id = 'CHANNEL_ID'
WHERE g.state = 'open'
ORDER BY g.created_at DESC
```

### Schema Discovery
```
SELECT schema_name, table_name
FROM coral.tables
ORDER BY 1, 2
```

### Release Notes from Merged PRs
```
SELECT number, title, merged_at
FROM github.pulls
WHERE repo = 'devs_first_mate' AND state = 'closed'
ORDER BY merged_at DESC
LIMIT 10
```

---

## 🔗 Links

| | |
|---|---|
| 🌐 Live App | https://devs-first-mate.onrender.com |
| 📦 GitHub (Hackathon Project) | https://github.com/mauryasagar/devs_first_mate |
| ⭐️ Star Coral | https://git.new/coral-wemakedevs-may26 |

---

## 🏃 Run Locally
```
# 1. Clone the repo
git clone https://github.com/mauryasagar/devs_first_mate
cd devs_first_mate

# 2. Install Coral
brew install withcoral/tap/coral        # macOS
# or
curl -fsSL https://withcoral.com/install.sh | sh   # Linux

# 3. Add sources
coral source add --interactive github
coral source add --interactive slack

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Run the app
python app.py
```

---

Built with ❤️ for WeMakeDevs
Hackathon — Pirates of Coral-bean · Powered by Coral
