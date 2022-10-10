# File: Bus.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Data container for Bus components, inherited from Component class
#

from Component import Component

class Bus (Component):

    def __init__(self, name, v_nom):
        Component.__init__(self)

        self.type   = "Bus"
        self.name   = name
        self.v_nom  = v_nom
