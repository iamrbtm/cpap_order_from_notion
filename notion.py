import requests
from requests.structures import CaseInsensitiveDict
import json

def auth(auth_name):
        data = ""
        if data == "":
            with open("key.txt") as file:
                data = file.read()
                keys = json.loads(data)
        key = keys[auth_name]
        
        return key
      
def query_db(id, data, auth_name):
    headers = {
        'Authorization': f'Bearer {auth(auth_name)}',
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json',
        }
    response = requests.post(f'https://api.notion.com/v1/databases/{id}/query', headers=headers, data=data)
    return response

def get_list_database():
    url = "https://api.notion.com/v1/search"
    payload = json.dumps({"filter": {"property": "object","value": "database"}})
    headers = {'Content-Type': 'application/json','Notion-Version': '2021-05-13','Authorization': 'Bearer '+auth('notion')}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response

def get_database(id, auth_name):
    headers = {
        'Authorization': f"Bearer {auth(auth_name)}",
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json',
    }
    data = '{"filter":{"or":[{"property":"needs_macros","checkbox":{"equals":true}}]},"sorts":[{"property":"Name","direction":"ascending"}]}'
    response = requests.post(f'https://api.notion.com/v1/databases/{id}/query', headers=headers, data=data)
    return response

def get_page(id, auth_name):
    url = "https://api.notion.com/v1/pages/"+ str(id)
    url = url.translate({ord(i): None for i in '(),\''})
    headers = CaseInsensitiveDict()
    headers['Authorization'] = auth(auth_name)
    headers['Notion-Version']= "2021-05-13"
    
    response = requests.get(url, headers=headers)
    return response.text