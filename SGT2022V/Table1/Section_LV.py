# File: Section_LV.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Objects of this class represents Low Voltage table sections (common street with houses)
# All platforms on this section only accepts LV modules
#

from Section import Section
from Ledstrip import Ledstrip

class Section_LV (Section):

    voltage = "LV"
    num_ledstrips  = 16
    num_buses      = 16

    critical    = 0.63
    high        = 0.5
    normal      = 0.45
    low         = 0.2

    v_nom = 20
    x = 0.1
    r = 0.01
    
    def __init__(self, section_name):
        Section.__init__(self, section_name)

        # ledstrips
        for i in range(self.num_ledstrips):
            self.ledstrips.append( Ledstrip(self.voltage) )

        # buses
        for i in range(0, self.num_buses):
            bus_name = "bus" + str(i)
            self.add_bus(bus_name, self.v_nom)

        # lines
        self.add_line("line0",  bus0="bus0",  bus1="bus1",  x=self.x, r=self.r)
        self.add_line("line1",  bus0="bus1",  bus1="bus2",  x=self.x, r=self.r)
        self.add_line("line2",  bus0="bus2",  bus1="bus3",  x=self.x, r=self.r)
        self.add_line("line3",  bus0="bus2",  bus1="bus4",  x=self.x, r=self.r)
        self.add_line("line4",  bus0="bus4",  bus1="bus5",  x=self.x, r=self.r)
        self.add_line("line5",  bus0="bus4",  bus1="bus6",  x=self.x, r=self.r)
        self.add_line("line6",  bus0="bus6",  bus1="bus7",  x=self.x, r=self.r)
        self.add_line("line7",  bus0="bus6",  bus1="bus8",  x=self.x, r=self.r)
        self.add_line("line8",  bus0="bus8",  bus1="bus9",  x=self.x, r=self.r)
        self.add_line("line9",  bus0="bus8",  bus1="bus10", x=self.x, r=self.r)
        self.add_line("line10", bus0="bus10", bus1="bus11", x=self.x, r=self.r)
        self.add_line("line11", bus0="bus10", bus1="bus12", x=self.x, r=self.r)
        self.add_line("line12", bus0="bus12", bus1="bus13", x=self.x, r=self.r)
        self.add_line("line13", bus0="bus12", bus1="bus14", x=self.x, r=self.r)
        self.add_line("line14", bus0="bus14", bus1="bus15", x=self.x, r=self.r)
        self.add_line("line15", bus0="bus14", bus1="bus1",  x=self.x, r=self.r)

        any_component = []
        any_component.append("Generator")
        any_component.append("Load")
        any_component.append("Storage")

        LV_transformer = []
        LV_transformer.append("Transformer")

        # platforms
        self.add_platform("bus13", self.voltage, "RFID 0", [12], LV_transformer)
        self.add_platform("bus15", self.voltage, "RFID 1", [14], any_component)
        self.add_platform("bus0",  self.voltage, "RFID 2", [0],  any_component)
        self.add_platform("bus3",  self.voltage, "RFID 3", [2],  any_component)
        self.add_platform("bus5",  self.voltage, "RFID 4", [4],  any_component)
        self.add_platform("bus7",  self.voltage, "RFID 5", [6],  any_component)
        self.add_platform("bus9",  self.voltage, "RFID 6", [8],  any_component)
        self.add_platform("bus11", self.voltage, "RFID 7", [10], any_component)

        # bind ledstrips with its respective lines
        prefix = section_name + "_"

        for i in range(0, self.num_ledstrips):
            self.ledstrips[i].line = prefix + "line" + str(i)
            self.ledstrips[i].set_stress_levels(self.low, self.normal, self.high, self.critical)

    def is_network_connected(self):
        for platform in self.platforms:
            if (platform.RFID_location == "RFID 0"):
                if (platform.module):
                    return True
                else:
                    return False
