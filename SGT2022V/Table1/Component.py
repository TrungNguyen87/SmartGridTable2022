# File: Component.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Component, must contain a bus and type.
# Other components inherit this class
#

class Component:
    
    def __init__(self):
        self.name = "Unknown component"
        self.bus0  = ""
        self.type = ""
        self.static = True
