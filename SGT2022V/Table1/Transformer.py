# File: Transformer.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Not used, transformer objects are planned to replace the dynamic links
#

from Component import Component

class Transformer (Component):

    def __init__(self):
        Component.__init__(self)

        self.s_nom_extendable = False
        self.model = ""
        self.x = 0
        self.r = 0