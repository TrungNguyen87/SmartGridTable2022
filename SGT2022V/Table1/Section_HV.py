# File: Section_HV.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Objects of this class represents High Voltage table sections (heavy power generators)
# All platforms on this section only accepts HV modules
#

from Section import Section
from Ledstrip import Ledstrip

class Section_HV (Section):

    voltage = "HV"
    num_ledstrips  = 12
    num_buses      = 13

    critical    = 35
    high        = 30
    normal      = 20
    low         = 10

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
        self.add_line("line0",  bus0="bus0", bus1="bus1",  x=self.x, r=self.r)
        self.add_line("line1",  bus0="bus1", bus1="bus2",  x=self.x, r=self.r)
        self.add_line("line2",  bus0="bus1", bus1="bus3",  x=self.x, r=self.r)
        self.add_line("line3",  bus0="bus3", bus1="bus4",  x=self.x, r=self.r)
        self.add_line("line4",  bus0="bus4", bus1="bus5",  x=self.x, r=self.r)
        self.add_line("line5",  bus0="bus3", bus1="bus6",  x=self.x, r=self.r)
        self.add_line("line6",  bus0="bus6", bus1="bus7",  x=self.x, r=self.r)
        self.add_line("line7",  bus0="bus7", bus1="bus8",  x=self.x, r=self.r)
        self.add_line("line8",  bus0="bus8", bus1="bus9",  x=self.x, r=self.r)
        self.add_line("line9",  bus0="bus7", bus1="bus10",  x=self.x, r=self.r)
        self.add_line("line10", bus0="bus10", bus1="bus11", x=self.x, r=self.r)
        self.add_line("line11", bus0="bus10", bus1="bus12", x=self.x, r=self.r)

        any_component = []
        any_component.append("Generator")
        any_component.append("Load")
        any_component.append("Storage")

        HV_transformers = []
        HV_transformers.append("Transformer")

        # platforms
        self.add_platform("bus0",  self.voltage, "RFID 5", [0],    any_component)
        self.add_platform("bus5",  self.voltage, "RFID 0", [3, 4], HV_transformers)
        self.add_platform("bus9",  self.voltage, "RFID 3", [7, 8], HV_transformers)
        self.add_platform("bus11", self.voltage, "RFID 1", [10],   any_component)

        # bind ledstrips with its respective lines
        prefix = section_name + "_"

        for i in range(0, self.num_ledstrips):
            self.ledstrips[i].line = prefix + "line" + str(i)
            self.ledstrips[i].set_stress_levels(self.low, self.normal, self.high, self.critical)
