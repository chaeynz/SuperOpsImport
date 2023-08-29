import requests
import json
import re
import FileHandler

global_apikey = ""
global_customersubdomain = ""
global_directory = ""
global_itdocumentation_typeId = ""
global_accountId = ""
global_siteId = ""

def setGlobals():
    global global_apikey, global_customersubdomain, global_directory, global_itdocumentation_typeId, global_accountId, global_siteId
    
    try:
        with open("globals.json", "r") as f:
            data = json.load(f)
        global_apikey = data.get('global_apikey', '')
        global_customersubdomain = data.get('global_customersubdomain', '')
        global_directory = data.get('global_directory', '')
        global_itdocumentation_typeId = data.get('global_itdocumentation_typeId', '')
        global_accountId = data.get('global_accountId', '')
        global_siteId = data.get('global_siteId', '')

    except FileNotFoundError:
        print("No config file found. Please enter the details.")
    
    if not global_apikey:
        global_apikey = input("API Key:\n")
        saveGlobals()

    if not global_customersubdomain:
        global_customersubdomain = input("Customer Subdomain: ")
        saveGlobals()

    #if not global_directory:
        #global_directory = input("Directory with .html files to Import: ")
        #FileHandler.Index.selectFolder(global_directory)
        #saveGlobals()

    if not global_itdocumentation_typeId:
        global_itdocumentation_typeId = input("Enter typeId of the IT Documentation (Get from https://developer.superops.ai/#query-getItDocumentationList)\nEnter typeId: ")
        saveGlobals()
        
    if not global_accountId:
        global_accountId = input("Enter ID of Account to store the IT Documentation (Get from https://developer.superops.ai/#query-getClientList)\nEnter client - accountId: ")
        saveGlobals()
        
    if not global_siteId:
        global_siteId = input("Enter ID of Site to store the IT Documentation (Get from https://developer.superops.ai/#query-getClientSiteList)\nEnter site - id: ")
        saveGlobals()

def saveGlobals():
    data = {
        'global_apikey': global_apikey,
        'global_customersubdomain': global_customersubdomain,
        'global_directory': global_directory,
        'global_itdocumentation_typeId': global_itdocumentation_typeId,
        'global_accountId': global_accountId,
        'global_siteId': global_siteId
    }
    with open("globals.json", "w") as file:
        json.dump(data, file)


# MAIN FUNCTION (HAHA PYTHON)

setGlobals()

url = 'https://api.superops.ai/msp'

headers = {
    'Authorization': 'Bearer ' + global_apikey,
    'Content-Type': 'application/json',
    'Customersubdomain': global_customersubdomain,
}

query = """
mutation createItDocumentation($input: CreateItDocumentationInput!) {
  createItDocumentation(input: $input) {
    itDocId
    name
    client
    site
    customFields
  }
}

"""

CreateItDocumentationInput = {
  "typeId": global_itdocumentation_typeId,
  "name": "API_Test1",
  "client": {"accountId": global_accountId},
  "site": {"id": global_siteId},
  "customFields": {
  "udf4rtxt": {
  "content": "<p>Test via API</p>"
  }
  }
}

variables = {
    "input": CreateItDocumentationInput
    }







       

                                                                                      
response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

print("API Response:")

if response.status_code == 200:
    print(response.text)
else:
    print(f"Failed to get data. Status code: {response.status_code}")