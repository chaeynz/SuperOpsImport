import requests
import json
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup
import FileHandler


API_REQUEST_LIMIT_PER_MINUTE = 800

global_apikey = ""
global_customersubdomain = ""
global_itdocumentation_typeId = ""
global_accountId = ""
global_siteId = ""
global_content_host = ""

local_directory = "" # this contains the .html files
content_host_subfolder = ""

timestamp = ""

def setGlobals():
    global global_apikey, global_customersubdomain, global_itdocumentation_typeId, global_accountId, global_siteId, global_content_host
    
    try:
        with open("globals.json", "r") as file:
            data = json.load(file)
        global_apikey = data.get('global_apikey', '')
        global_customersubdomain = data.get('global_customersubdomain', '')
        global_itdocumentation_typeId = data.get('global_itdocumentation_typeId', '')
        global_accountId = data.get('global_accountId', '')
        global_siteId = data.get('global_siteId', '')
        global_content_host = data.get('global_content_host', '')

    except FileNotFoundError:
        print("No config file found. Please enter the details.")
    
    if not global_apikey:
        global_apikey = input("API Key:\n")
        saveGlobals()

    if not global_customersubdomain:
        global_customersubdomain = input("Customer Subdomain: ")
        saveGlobals()

    if not global_itdocumentation_typeId:
        global_itdocumentation_typeId = input("Enter typeId of the IT Documentation (Get from https://developer.superops.ai/#query-getItDocumentationList)\nEnter typeId: ")
        saveGlobals()
        
    if not global_accountId:
        global_accountId = input("Enter ID of Account to store the IT Documentation (Get from https://developer.superops.ai/#query-getClientList)\nEnter client - accountId: ")
        saveGlobals()
        
    if not global_siteId:
        global_siteId = input("Enter ID of Site to store the IT Documentation (Get from https://developer.superops.ai/#query-getClientSiteList)\nEnter site - id: ")
        saveGlobals()
    
    if not global_content_host:
        global_content_host = input("Enter URL of Root Folder where new images should be accessible\n(You will LATER define the folder INSIDE of this Root Folder, in which the images/ folder is located\n\nThe Root URL is saved in globals.json, that's why ;)\nYou can define the subfolder of this root each time the program starts\nEnter URL of Root Folder: ")
        saveGlobals()

def saveGlobals():
    data = {
        'global_apikey': global_apikey,
        'global_customersubdomain': global_customersubdomain,
        'global_itdocumentation_typeId': global_itdocumentation_typeId,
        'global_accountId': global_accountId,
        'global_siteId': global_siteId,
        'global_content_host': global_content_host
    }
    with open("globals.json", "w") as file:
        json.dump(data, file)

def getCreateItDocumentationInput(documentName, documentContent):
    CreateItDocumentationInput = {
    "typeId": global_itdocumentation_typeId,
    "name": documentName,
    "client": {"accountId": global_accountId},
    "site": {"id": global_siteId},
    "customFields": {"udf4rtxt": {"content": documentContent}}
    }
    return CreateItDocumentationInput

def replace_local_paths(css_content):
    # Define the URL prefix where the images will be hosted
    new_url_prefix = global_content_host + content_host_subfolder

    # Define regex pattern for matching URLs in the css
    pattern = r"url\(([^)]+)\)"  # matches url(...)
    
    # Define a function to be used for each regex match
    def replacer(match):
        original_path = match.group(1)  # Extract original URL
        # Extract only the filename from the original URL
        filename = original_path.split('/')[-1]
        # Create a new URL using the filename
        new_url = f"url({new_url_prefix}/{filename})"
        return new_url

    # Replace all occurrences
    new_css_content = re.sub(pattern, replacer, css_content)

    # For @atlassian-logo-neutral-image specifically
    atlassian_pattern = r"@atlassian-logo-neutral-image: '([^']+)'"

    def atlassian_replacer(match):
        original_path = match.group(1)  # Extract original URL
        # Extract only the filename from the original URL
        filename = original_path.split('/')[-1]
        # Create a new URL using the filename
        new_url = f"@atlassian-logo-neutral-image: '{new_url_prefix}/{filename}'"
        return new_url
    
    new_css_content = re.sub(atlassian_pattern, atlassian_replacer, new_css_content)

    return new_css_content
    


def parseHtmlFile(htmlData):
    soup = BeautifulSoup(htmlData, 'html.parser')

    title_tag = soup.find('title')

    if title_tag:
        FileHandler.writeFileContent("SuperOpsImport_"+timestamp+".log", "Removing tag: " + str(title_tag))
        title_tag.extract()

    main_header = soup.find('div', {'id': 'main-header'})
    if main_header:
        FileHandler.writeFileContent("SuperOpsImport_"+timestamp+".log", "Removing main-header: " + str(main_header))
        main_header.extract()
        
    head_tag = soup.head
    if not head_tag:
        head_tag = soup.new_tag('head')
        soup.html.insert(0, head_tag)
    
    style_tag = soup.new_tag('style')
    style_tag.string = CSS
    head_tag.append(style_tag)

    
    
    return str(soup)

def getHtmlTitle(htmlData):
    soup = BeautifulSoup(htmlData, 'html.parser')
    title_tag = soup.find('title')

    if title_tag is not None:  # If title tag exists
        return title_tag.string if title_tag.string else ""  # Return the title string, or an empty string if the title is empty.
    else:
        return None

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
        FileHandler.writeFileContent("SuperOpsImport_"+timestamp+".log", htmlData)
        
        variables = {
        "input": getCreateItDocumentationInput(htmlTitle, htmlData)
        }
        
        if(len(FileHandler.Index.allFiles) > API_REQUEST_LIMIT_PER_MINUTE): # checks if this loop could exceed the API Request Limit
            time.sleep(60 / API_REQUEST_LIMIT_PER_MINUTE)                   # ensures to only execute as many API requests as the limit per minute
            
        response = requests.post(URL, headers=HEADERS, json={'query': QUERY, 'variables': variables})
        
        # Logging
        print("API Response: " + response.text)
        FileHandler.writeFileContent("SuperOpsImport_"+timestamp+".log", response.text)
    


# MAIN FUNCTION (HAHA PYTHON)

URL = 'https://api.superops.ai/msp'

setGlobals()

local_directory = input("Please enter the exact path where you .html files are located\nUse '/' and NOT '\'\n\nWITHOUT trailing /\nLocal Path: ")
FileHandler.Index.selectFolder(local_directory)

content_host_subfolder = input("Please now define the subfolder in which the content of the Export will be hosted:\nThis folder should contain 'images/' and /or 'attachments/'\n\nWITHOUT TRAILING '/'\nExact URL: " + global_content_host)
CSS = replace_local_paths(FileHandler.getFileContent(FileHandler.Index.thisDirectory + "/style/site.css"))
FileHandler.writeFileContent('CSS.log', CSS)

HEADERS = {
'Authorization': 'Bearer ' + global_apikey,
'Content-Type': 'application/json',
'Customersubdomain': global_customersubdomain,
}

QUERY = """
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

TESTQUERY = """
query getItDocumentationCategories {
  getItDocumentationCategories {
    typeId
    name
    description
    entityName
    lastUpdatedTime
    customFields
  }
}

"""

print("Let's run a quick test on the API")
test_response = requests.post(URL, headers=HEADERS, json={'query': TESTQUERY})

test_response_json = json.loads(test_response.text)

categories = test_response_json.get('data', {}).get('getItDocumentationCategories', [])

# Initialize a flag to false, which will be set true if a match is found
match_found = False

# Loop through each dictionary in the list
for category in categories:
    response_typeId = category.get('typeId', None)
    if global_itdocumentation_typeId == response_typeId:
        match_found = True
        break



if test_response.status_code == 200 and match_found:
    print(test_response.text)
    print("\nINFO: typeId found in categories")
elif test_response.status_code == 200 and match_found == False:
    print("typeId Does not match any Category!\nResponse:\n" + test_response.text)
else:
    print(f"Failed to get data. Status code: {test_response.status_code}\nResponse Text:" + test_response.text)


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
