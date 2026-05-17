import os
import requests

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRFTOKEN = os.getenv("CSRFTOKEN")
USERNAME = os.getenv("LEETCODE_USERNAME")

url = "https://leetcode.com/graphql"

headers = {
    "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION}; csrftoken={CSRFTOKEN}",
    "x-csrftoken": CSRFTOKEN,
    "Referer": "https://leetcode.com",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}

query = """
query recentAcSubmissions($username: String!) {
  recentAcSubmissionList(username: $username) {
    id
    title
    titleSlug
    timestamp
  }
}
"""

response = requests.post(
    url,
    json={
        "query": query,
        "variables": {
            "username": USERNAME
        }
    },
    headers=headers
)

print("Status Code:", response.status_code)

data = response.json()

if "errors" in data:
    print("GraphQL Errors:")
    print(data["errors"])
else:
    print(data)