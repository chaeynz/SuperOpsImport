from globals import global_apikey, global_customersubdomain

API_REQUEST_LIMIT_PER_MINUTE = 800

URL = 'https://api.superops.ai/msp'

HEADERS = {
'Authorization': 'Bearer ' + global_apikey,
'Content-Type': 'application/json',
'Customersubdomain': global_customersubdomain,
}

QUERY_GET_ITDOC_CATEGORIES = """
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
QUERY_GET_ITDOC_LIST = """
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
QUERY_CREATE_ITDOC = """
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
QUERY_DELETE_ITDOC = """
mutation deleteItDocumentation($input: ItDocumentationIdentifierInput!) {
  deleteItDocumentation(input: $input)
}
"""
QUERY_GET_CLIENT_LIST = """
query getClientList($input: ListInfoInput!) {
  getClientList(input: $input) {
    clients {
      accountId
      name
    }
  }
}

"""
QUERY_GET_CLIENT_SITE_LIST = """
query getClientSiteList($input: GetClientSiteListInput!) {
  getClientSiteList(input: $input) {
    sites {
      id
      name
    }
  }
}

"""