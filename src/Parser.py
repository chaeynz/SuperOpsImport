from bs4 import BeautifulSoup
import FileHandler
from globals import timestamp, 

def getHtmlTitle(htmlData):
    soup = BeautifulSoup(htmlData, 'html.parser')
    title_tag = soup.find('title')

    if title_tag is not None:  # If title tag exists
        return title_tag.string if title_tag.string else ""  # Return the title string, or an empty string if the title is empty.
    else:
        return None

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
        
    

