import json, requests
from datetime import datetime, date
url = "https://api.notion.com/v1/pages/7b676086-5db3-451c-8d83-16c22ecea361"

payload = json.dumps({
  "properties": {
    "Last Ordered": {
      "date": {
        "start": date.today().strftime('%Y-%m-%d'),
        "end": None
      }
    }
  }
})
headers = {
  'Content-Type': 'application/json',
  'Notion-Version': '2021-05-13',
  'Authorization': 'Bearer secret_E56vtGLhJHUK1o7WerXlnUaZHcbHnnlyFiMuPPwU1bz'
}

response = requests.request("PATCH", url, headers=headers, data=payload)

print(response.text)