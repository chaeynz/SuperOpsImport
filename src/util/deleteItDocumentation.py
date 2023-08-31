import requests
from util.constants import URL, HEADERS, QUERY_DELETE_ITDOC
from util.globals import timestamp
from FileHandler import writeFileContent

def deleteItDocumentation():
    
    itdoc_variables = {
        "input": {
            "itDocId": input("Delete the IT Document with ID: ")
        }
    }

    response = requests.post(URL, headers=HEADERS, json={'query': QUERY_DELETE_ITDOC, 'variables': itdoc_variables})
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Request: QUERY_DELETE_ITDOC")
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Variables: " + itdoc_variables)
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Response: " + response.text)
