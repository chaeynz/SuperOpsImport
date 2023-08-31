import requests

from src.util.constants import URL, HEADERS, QUERY_GET_CLIENT_LIST
from src.util.globals import timestamp, global_client_id
from src.FileHandler import writeFileContent

def getClientList():
    
    client_variables = {
        "input": {
            "page": 1,
            "pageSize": 10
        }
    }
    
    
    response = requests.post(URL, headers=HEADERS, json={'query': QUERY_GET_CLIENT_LIST, 'variables': client_variables})
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Request: " + "QUERY_GET_CLIENT_LIST")
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Variables: " + client_variables)
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Response: " + response.text)
    return response
