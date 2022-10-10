# File: Section_MV_Ring.py
# Version 1.0
# Authors: Thijs van Elsacker
#
# Description:
# Objects of this class represents the Medium Voltage ring table section
#

from Section import Section
from Ledstrip import Ledstrip

class Section_MV_Ring (Section):

    voltage = "MV"
    num_ledstrips  = 22
    num_buses      = 22

    critical    = 30
    high        = 25
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
        self.add_line("line0",  bus0="bus0",  bus1="bus1",  x=self.x, r=self.r)
        self.add_line("line1",  bus0="bus1",  bus1="bus2",  x=self.x, r=self.r)
        self.add_line("line2",  bus0="bus2",  bus1="bus3",  x=self.x, r=self.r)
        self.add_line("line3",  bus0="bus3",  bus1="bus4",  x=self.x, r=self.r)
        self.add_line("line4",  bus0="bus3",  bus1="bus5",  x=self.x, r=self.r)
        self.add_line("line5",  bus0="bus5",  bus1="bus6",  x=self.x, r=self.r)
        self.add_line("line6",  bus0="bus6",  bus1="bus7",  x=self.x, r=self.r)
        self.add_line("line7",  bus0="bus7",  bus1="bus8",  x=self.x, r=self.r)
        self.add_line("line8",  bus0="bus7",  bus1="bus9",  x=self.x, r=self.r)
        self.add_line("line9",  bus0="bus9",  bus1="bus10", x=self.x, r=self.r)
        self.add_line("line10", bus0="bus10", bus1="bus11", x=self.x, r=self.r)
        self.add_line("line11", bus0="bus11", bus1="bus12", x=self.x, r=self.r)
        self.add_line("line12", bus0="bus11", bus1="bus13", x=self.x, r=self.r)
        self.add_line("line13", bus0="bus13", bus1="bus14", x=self.x, r=self.r)
        self.add_line("line14", bus0="bus14", bus1="bus15", x=self.x, r=self.r)
        self.add_line("line15", bus0="bus14", bus1="bus16", x=self.x, r=self.r)
        self.add_line("line16", bus0="bus16", bus1="bus17", x=self.x, r=self.r)
        self.add_line("line17", bus0="bus17", bus1="bus18", x=self.x, r=self.r)
        self.add_line("line18", bus0="bus18", bus1="bus19", x=self.x, r=self.r)
        self.add_line("line19", bus0="bus18", bus1="bus20", x=self.x, r=self.r)
        self.add_line("line20", bus0="bus20", bus1="bus21", x=self.x, r=self.r)
        self.add_line("line21", bus0="bus21", bus1="bus1",  x=self.x, r=self.r)

        # bind ledstrips with its respective lines
        prefix = section_name + "_"

        for i in range(0, self.num_ledstrips):
            self.ledstrips[i].line = prefix + "line" + str(i)
            self.ledstrips[i].set_stress_levels(self.low, self.normal, self.high, self.critical)
