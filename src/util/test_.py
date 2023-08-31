import requests

from src.util.constants import URL, HEADERS, QUERY_GET_CLIENT_LIST
from src.util.globals import timestamp, global_client_id
from src.FileHandler import writeFileContent

  
client_variables = {
        "input": {
            "page": 1,
            "pageSize": 10
        }
    }
    
    
response = requests.post(URL, headers=HEADERS, json={'query': QUERY_GET_CLIENT_LIST, 'variables': client_variables})
    
response_client_list_json = response.json()
print("1: " + str(response_client_list_json))
clients = response_client_list_json.get('data', {}).get('getClientList', [])
print("2: " + clients)
