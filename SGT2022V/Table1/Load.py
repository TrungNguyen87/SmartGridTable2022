# File: Load.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Data container for Loads, inherited from Component class
# p_set and q_set are retrieved from JSON scenario files (static network that is)
# Load objects are part of a Module object
#

from Component import Component

class Load (Component):

    def __init__(self):
        Component.__init__(self)
        
        self.type = "Load"
        self.carrier = "AC"
        self.p_set = 0
        self.q_set = 0
     