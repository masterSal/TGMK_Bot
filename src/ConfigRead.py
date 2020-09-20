#
#
#
#

import glob
from configparser import SafeConfigParser

class ConfigRead:
    def __init__(self, fname="config.ini"):
        self.filename = self.fileExists(fname)
        self.config = SafeConfigParser()

        # read
        self.config.read(self.filename)
    
    def fileExists(self, file):
        if glob.glob(str(file)): 
            return str(file)

        print("[-] File: " + str(file) + " not found...")
        return None
    
    def getVal(self, sec, key):
        return self.config.get(sec, key)

