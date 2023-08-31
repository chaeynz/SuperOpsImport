import json

global_api_token = ""
global_customersubdomain = "" 
global_client_id = ""
global_site_id = ""

timestamp = ""



def setGlobals():
    global global_api_token, global_customersubdomain, global_client_id, global_site_id, global_content_host
    
    try:
        with open("globals.json", "r") as file:
            data = json.load(file)
        global_apikey = data.get('global_api_token', '')
        global_customersubdomain = data.get('global_customersubdomain', '')
        global_accountId = data.get('global_client_id', '')
        global_siteId = data.get('global_site_id', '')

    except FileNotFoundError:
        print("No config file found. Please enter the details.")
    
    if not global_api_token:
        global_api_token = input("API Token: ")
        saveGlobals()

    if not global_customersubdomain:
        global_customersubdomain = input("Customer Subdomain: ")
        saveGlobals()

    if not global_client_id:
        global_accountId = input("Client ID: ")
        saveGlobals()
        
    if not global_site_id:
        global_siteId = input("Site ID: ")
        saveGlobals()

def saveGlobals():
    data = {
        'global_api_token': global_api_token,
        'global_customersubdomain': global_customersubdomain,
        'global_client_id': global_client_id,
        'global_site_id': global_site_id,
    }
    with open("globals.json", "w") as file:
        json.dump(data, file)