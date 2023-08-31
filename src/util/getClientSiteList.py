import requests
from util.constants import URL, HEADERS, QUERY_GET_CLIENT_SITE_LIST
from util.globals import timestamp, global_client_id
from FileHandler import writeFileContent

def getClientSiteList():
    
    client_site_variables = {
        "input": {
            "listInfo": {
                "page": 1,
                "pageSize": 10
            },
            "clientId": global_client_id
        }
    }

    response = requests.post(URL, headers=HEADERS, json={'query': QUERY_GET_CLIENT_SITE_LIST, 'variables': client_site_variables})
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Request: " + "QUERY_GET_CLIENT_SITE_LIST")
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Variables: " + client_site_variables)
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Response: " + response.text)
    return response