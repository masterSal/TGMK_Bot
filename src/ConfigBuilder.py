#!/usr/bin/env python3
#
#
#

from configparser import SafeConfigParser


class ConfigBuilder:
    def __init__(self, fname="config.ini"):
        self.filename = str(fname)
        self.config = SafeConfigParser()
        self.config.read(self.filename)
    
    def add_section(self, name):
        self.config.add_section(name)

    def add(self, name, key, val):
        print("==> Writing: Name: %s, Key: %s, Val: %s" % (name, key, val))
        self.config.set(name, key, val)
    
    def done(self):
        with open(self.filename, 'w') as f:
            self.config.write(f)




def main():
    c = ConfigBuilder()
    c.add_section("API")

    c.add("API", "api_id", "")
    c.add("API", "api_hash", "")
    
    c.add_section("CREDENTIALS")
    c.add("CREDENTIALS", "phone", "")
    c.add("CREDENTIALS", "passwd", "")
    
    c.done() # write to file


if __name__ == "__main__":
    main()

    
