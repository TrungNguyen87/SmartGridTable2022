# File: Line.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Data container for Line components, inherited from Component class
# Lines are placed between Buses
# active_power is used to drive the ledstrips, currently each ledstrip is attached to one line object
# x and r must be used in PyPSA simulations
#

from Component import Component

class Line(Component):

    def __init__(self, name, bus0, bus1, x, r):
        Component.__init__(self)

        self.type = "Line"
        self.name = name
        self.bus0 = bus0
        self.bus1 = bus1
        self.x = x
        self.r = r

        self.active_power = 0
