import time
from datetime import datetime

import FileHandler
from util.constants import API_REQUEST_LIMIT_PER_MINUTE
from util.createItDocumentation import createItDocumentation
from util.getItDocumentationCategories import getItDocumentationCategories
from util.globals import setGlobals, global_accountId, global_siteId
from Parser import parseHtmlFile, getHtmlTitle

itdoc_category_typeid = ""

def sendAllFilesToAPI():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    for file in FileHandler.Index.allFiles:
        htmlData = FileHandler.getFileContent(FileHandler.Index.thisDirectory + "/" + file)
        htmlTitle = getHtmlTitle(htmlData)
        if htmlTitle == "":
            print(htmlData)
            print("\n\n" + FileHandler.Index.thisDirectory + "\n\n" + file)
            htmlTitle = input("INFO: HTML Title Tag not found or empty\nManually define a Title for this document: ")
        htmlData = parseHtmlFile(htmlData)
        
        createItDocumentation(itdoc_category_typeid, htmlData)
        
        
        if(len(FileHandler.Index.allFiles) > API_REQUEST_LIMIT_PER_MINUTE): # checks if this loop could exceed the API Request Limit
            time.sleep(60 / API_REQUEST_LIMIT_PER_MINUTE)                   # ensures to only execute as many API requests as the limit per minute
            
def testAPI():
    print("Let's run a quick test on the API")
    itdoc_categories = getItDocumentationCategories    

    match_found = testTypeId(itdoc_categories)

    if itdoc_categories.status_code == 200 and match_found:
        print(itdoc_categories.text)
        print("\nINFO: typeId found in categories")
    elif itdoc_categories.status_code == 200 and match_found == False:
        print("typeId Does not match any Category!\nResponse:\n" + itdoc_categories.text)
    else:
        print(f"Failed to get data. Status code: {itdoc_categories.status_code}\nResponse Text:" + itdoc_categories.text)
    
def testTypeId(itdoc_categories):
    itdoc_categories_json = itdoc_categories.json
    categories = itdoc_categories_json.get('data', {}).get('getItDocumentationCategories', [])

    # Initialize a flag to false, which will be set true if a match is found
    match_found = False

    # Loop through each dictionary in the list
    for category in categories:
        response_typeId = category.get('typeId', None)
        if itdoc_category_typeid == response_typeId:
            match_found = True
            break
    return match_found

def testClientId(response_client_list):
    response_client_list_json = response_client_list.json
    clients = response_client_list_json.get('data', {}).get('getClientList', [])

    # Initialize a flag to false, which will be set true if a match is found
    match_found = False

    # Loop through each dictionary in the list
    for client in clients:
        response_typeId = client.get('accountId', None)
        if itdoc_category_typeid == response_typeId:
            match_found = True
            break
    return match_found
    
def testSiteId(clientid, sites):
    response_site_list_json = sites.json
    



# MAIN FUNCTION (HAHA PYTHON)



setGlobals()

local_directory = input("Please enter the exact path where you .html files are located\nUse '/' and NOT '\'\n\nWITHOUT trailing /\nLocal Path: ")
FileHandler.Index.selectFolder(local_directory)


FileHandler.Index.populate_allFiles()
CHOICE_MESSAGE = " Files were found, do you want to continue?\nThere is no check for .html suffix!\n\ny: yes\nn: no\nlist: List filenames\n\nAnswer y/n/list: "

while True:
    choice = input("\n" + str(len(FileHandler.Index.allFiles)) + CHOICE_MESSAGE)
    if choice == "y" or choice == "yes":
        sendAllFilesToAPI()
        break
    elif choice == "l" or choice == "list":
        print(FileHandler.Index.allFiles)
    else:
        print("Program Closes")
        break
