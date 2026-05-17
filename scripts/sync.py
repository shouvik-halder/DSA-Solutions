import os
import requests

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRFTOKEN = os.getenv("CSRFTOKEN")

url = "https://leetcode.com/graphql"

headers = {
    "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION}; csrftoken={CSRFTOKEN}",
    "x-csrftoken": CSRFTOKEN,
    "Referer": "https://leetcode.com",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}

query = """
query {
  recentAcSubmissionList {
    id
    title
    titleSlug
    timestamp
  }
}
"""

response = requests.post(
    url,
    json={"query": query},
    headers=headers
)

print(response.json())