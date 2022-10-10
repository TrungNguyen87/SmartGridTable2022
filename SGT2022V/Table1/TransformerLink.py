# File: StoragesUnit.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# A special link between table sections and has a connection with a Platform
# This way we can shut this link down if no transformer is present on the transfomer Platform
#

class TransformerLink:

    def __init__(self,RFID_table, RFID_location, table0, bus0, table1, bus1):
        
        self.RFID_table = RFID_table
        self.RFID       = RFID_location

        self.table0     = table0
        self.bus0       = table0 + "_" + bus0
        self.table1     = table1
        self.bus1       = table1 + "_" + bus1
        self.name       = "Dynamic_" + self.bus0 + "__" + self.bus1
        
        