# File: Module.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Class which represents a module (placable piece on the table, likes houses and power plants)
# Modules have RFID tag numbers attached, this number is used to load the correct values from the JSON files
# Modules consists out of one or multiple Components
#

class Module:

    def __init__(self):

        self.RFID_tag       = ""
        self.name           = ""
        self.module_name    = ""
        self.voltage        = ""

        self.components = []

    def clear(self):
        self.components.clear()

    def add_component(self, component):
        self.components.append(component)
