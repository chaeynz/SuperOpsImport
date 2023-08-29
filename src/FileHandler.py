
import os


def getFileContent(filePath):
    try:
        with open(filePath, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return ""

def setFileContent(filePath, _InputString):
    try:
        with open(filePath, 'w') as file:
            file.write(_InputString)
    except Exception as e:
        print(f"An error occurred: {e}")

        

    

class Index:
    position = 0
    thisDirectory = ""
    allFiles = []
    
    @classmethod
    def getCurrentFile(cls):
        return cls.allFiles[cls.position]
    
    @classmethod
    def upgradeIndex(cls):
        cls.position = cls.position+1

    @classmethod
    def getAllFiles(cls):
        return cls.allFiles
    
    @classmethod
    def selectFolder(cls, _InputString):
        cls.thisDirectory = _InputString
    
    @classmethod
    def populate_allFiles(cls):
        cls.allFiles = [f for f in os.listdir(cls.thisDirectory) if os.path.isfile(os.path.join(cls.thisDirectory, f))]
        