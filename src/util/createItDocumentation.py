import requests
from FileHandler import writeFileContent
from util.constants import URL, HEADERS, QUERY_CREATE_ITDOC
from util.globals import timestamp, global_accountId, global_siteId

def createItDocumentation(type_id, itdoc_input_name, itdoc_input_content):
    itdoc_input = {
        "typeId": type_id,
        "name": itdoc_input_name,
        "client": {
            "accountId": global_accountId
        },
        "site": {
            "id": global_siteId
        },
        "customFields": {
            "udf4rtxt": {
                "content": itdoc_input_content
            }
        }
    }
    itdoc_variables = {
        "input": itdoc_input
    }

    response = requests.post(URL, headers=HEADERS, json={'query': QUERY_CREATE_ITDOC, 'variables': itdoc_variables})
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Request: " + "QUERY_CREATE_ITDOC")
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Variables: " + itdoc_input_content)
    writeFileContent("SuperOpsImport_"+timestamp+".log", "Response: " + response.text)