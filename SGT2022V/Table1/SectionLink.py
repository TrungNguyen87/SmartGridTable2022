# File: SectionLink.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# A connection between table sections so power can flow from one to another
#

class SectionLink:

    def __init__(self, table0, bus0, table1, bus1):
        
        self.bus0   = table0 + "_" + bus0
        self.bus1   = table1 + "_" + bus1
        self.name   = self.bus0 + "__" + self.bus1
        