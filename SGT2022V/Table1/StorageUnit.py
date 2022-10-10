# File: StoragesUnit.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Data container for Storages, inherited from Component class
# Most values are retrieved from JSON scenario files (static network that is)
# Storage objects are part of a Module object
#

from Component import Component

class StorageUnit (Component):

    def __init__(self):
        Component.__init__(self)
        
        self.type    = "Storage"
        self.p_nom_min = 0
        self.p_nom_max = 0
        self.p_nom_extendable = "False"
        self.marginal_cost = 0
        self.state_of_charge_initial = 0
        