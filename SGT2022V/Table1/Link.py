# File: Link.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Data container for Link components, inherited from Component class
# Link is one direction flow
#

from Component import Component

class Link(Component):

    def __init__(self, name, bus0, bus1, p_nom_extendable):
        Component.__init__(self)

        self.type = "Link"
        self.name = name
        self.bus0 = bus0
        self.bus1 = bus1
        self.p_nom_extendable = p_nom_extendable
