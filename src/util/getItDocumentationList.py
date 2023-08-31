import requests
from util.constants import URL, HEADERS, QUERY_GET_ITDOC_CATEGORIES
from util.globals import timestamp
from FileHandler import writeFileContent

def getItDocumentationList():
    
    itdoc_variables = {
        "input": {
            "listInfo": {
                "page": 1,
                "pageSize": 10
            },
            "typeId": input("Which type ID do you want to select?"),
        }
    }

    response = requests.post(URL, headers=HEADERS, json={'query': QUERY_GET_ITDOC_CATEGORIES, 'variables': itdoc_variables})
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Request: " + "QUERY_GET_ITDOC_CATEGORIES")
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Variables: " + itdoc_variables)
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Response: " + response.text)
    return response