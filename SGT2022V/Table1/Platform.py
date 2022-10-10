# File: Platform.py
# Version 1.0
# Authors: Jop Merz, Thijs van Elsacker
#
# Description:
# Class which represents a table platform, identified by location numbers [RFID 0, RFID 1 etc]
# These are used to place modules on
# Platforms must have a list of accepted modules, in the case of transformer specific platforms
# error_lines is a array of lines which are "connected" to said platform and will turn red when a wrong module is placed
#

class Platform:

    def __init__(self, bus, voltage, RFID_location, error_lines, accepted_modules):
        self.bus            = bus
        self.voltage        = voltage
        self.error_lines    = error_lines
        self.RFID_location  = RFID_location
        self.RFID_tag       = ""

        self.accepted_modules      = []

        for module in accepted_modules:
            self.accepted_modules.append(module)

        self.module     = None
        self.components = []

        self.__has_changed = False


    def add_module(self, module):

        if (module != self.module):
            self.module    = module
            self.RFID_tag  = module.RFID_tag

            self.components.clear()

            for component in self.module.components:
                component.bus0 = self.bus
                self.components.append(component)

            self.__has_changed = True


    def clear_module(self):
        if (self.module):
            self.module   = None
            self.RFID_tag = "0"
            self.components.clear()
            self.__has_changed = True


    def reset_changed(self):
        self.__has_changed = False


    def has_changed(self):
        return self.__has_changed
