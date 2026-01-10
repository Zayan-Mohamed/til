# Job Board Scraping: API Endpoints & Cheat Sheet

I found a Python script that aggregates jobs without needing complex authentication. Here are the endpoints.

## 1. LinkedIn (The "Guest" API Trick)
You don't need OAuth if you use the "Guest" endpoint, but you **must** use a real User-Agent header.

- **URL:** `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search`
- **Method:** `GET`
- **Critical Headers:**
  - `User-Agent`: `Mozilla/5.0 ... Chrome/120.0...` (Use a real browser string)
  - `Upgrade-Insecure-Requests`: `1`
- **Parameters:**
  - `keywords`: (e.g., "software engineer")
  - `location`: (e.g., "Remote")
  - `start`: Pagination offset (0, 25, 50...)
  - `f_TP`: `1` (Crucial: filters for "Last 24 hours" to avoid dead links)

## 2. Remotive (Public API)
Clean JSON response, no scraping html needed.
- **URL:** `https://remotive.com/api/remote-jobs`
- **Params:** `category=software-dev`, `limit=10`

## 3. Arbeitnow
Returns a massive JSON list; filter it client-side.
- **URL:** `https://www.arbeitnow.com/api/job-board-api`

## Python Snippet: The Rate Limiter
Always sleep between requests to avoid IP bans.
```python
import time
import requests

# Be polite
time.sleep(2) 
response = requests.get(url, headers=headers)
```

Checkout the script [here](../python/scrape_jobs.py)
