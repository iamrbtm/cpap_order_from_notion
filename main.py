import requests
import json

url = "https://api.notion.com/v1/databases/ac64bba17a8e4a3aa696543024c86206/query"

payload = json.dumps({
  "filter": {
    "property": "OrderNow",
    "checkbox": {
      "equals": True
    }
  }
})
headers = {
  'Content-Type': 'application/json',
  'Notion-Version': '2021-05-13',
  'Authorization': 'Bearer secret_E56vtGLhJHUK1o7WerXlnUaZHcbHnnlyFiMuPPwU1bz'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
