# File: Generator.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Data container for Generators, inherited from Component class
# Most variable values are retrieved from JSON scenario files (static network that is)
# Generator objects are part of a Module object
#

from Component import Component

class Generator (Component):

    def __init__(self):
        Component.__init__(self)

        self.type    = "Generator"
        self.p_nom = 0
        self.p_set = 0
        self.p_min_pu = 0
        self.p_max_pu = 1
        self.p_nom_min = 0
        self.p_nom_max = 0
        self.marginal_cost = 0
        self.p_nom_extendable = False
