import sys
import os


def getFileContent(filePath):
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("File Not Found")
        return ""
    except PermissionError as e:
        print("Permission error: " + e)
        return ""

def setFileContent(filePath, _InputString):
    try:
        with open(filePath, 'w') as file:
            file.write(_InputString)
    except Exception as e:
        print(f"An error occurred: {e}")

def writeFileContent(filePath, _InputString):
    try:
        with open(filePath, 'w') as file:
            file.write(_InputString)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()
        

    

class Index:
    thisDirectory = ""
    allFiles = []
        
    @classmethod
    def selectFolder(cls, _InputString):
        cls.thisDirectory = _InputString
    
    @classmethod
    def populate_allFiles(cls):
        cls.allFiles = [f for f in os.listdir(cls.thisDirectory) if os.path.isfile(os.path.join(cls.thisDirectory, f))]
        