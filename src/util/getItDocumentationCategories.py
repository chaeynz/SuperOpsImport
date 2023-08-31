import requests
from util.constants import URL, HEADERS, QUERY_GET_ITDOC_CATEGORIES
from util.globals import timestamp
from FileHandler import writeFileContent

def getItDocumentationCategories():
    
    response = requests.post(URL, headers=HEADERS, json={'query': QUERY_GET_ITDOC_CATEGORIES})
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Request: " + "QUERY_GET_ITDOC_CATEGORIES")
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Response: " + response.text)
    return response