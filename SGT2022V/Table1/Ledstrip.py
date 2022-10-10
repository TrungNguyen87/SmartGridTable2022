# File: Ledstrip.py
# Version 1.0
# Authors: Jop Merz, Thijs van Elsacker
#
# Description:
# Class which represents a ledstrip on a table section
# This class contains the led flow speed, color, direction and state
#

class Ledstrip:

    def __init__(self, voltage):
        self.state = "Passive"
        self.voltage = voltage
        self.load = "Normal"
        self.direction = 0
        self.speed  = 0
        self.error  = False
        self.active = True

        self.stress_high        = 0
        self.stress_critical    = 0

        self.speed_med          = 0
        self.speed_high         = 0

        self.previous_state     = ""
        self.previous_load      = ""
        self.previous_speed     = 0
        self.previous_direction = 0

        self.line = ""
        self.active_power = 0


    def is_changed(self):
        changed = False

        if (self.previous_state != self.state or
            self.previous_load != self.load or
            self.previous_speed != self.speed or
            self.previous_direction != self.direction):
            changed = True

        return changed


    def reset_changed_flags(self):
        self.previous_state = self.state
        self.previous_load = self.load
        self.previous_speed = self.speed
        self.previous_direction = self.direction


    def get_message_string(self):

        string = {
                "state": self.state,
                "voltage": self.voltage,
                "load": self.load,
                "direction": self.direction,
                "speed": self.speed
                }

        return str(string)


    def set_stress_levels(self, speed_med, speed_high, stress_high, stress_critical):
        self.speed_med = speed_med
        self.speed_high = speed_high
        self.stress_high = stress_high
        self.stress_critical = stress_critical


    def refresh(self):
        if (self.active_power >= 0.0):
            self.direction = 0
        else:
            self.direction = 1

        active_power_abs = abs(self.active_power)

        if(self.error):
            self.state = "Error"
        elif (self.active_power <= 0.001 and self.active_power >= -0.001):
            self.state = "Passive"
        else:
            self.state = "Active"

        if(self.active == False):
            self.state = "Off"

        if (active_power_abs <= self.speed_med):
            self.speed = 1
        elif (active_power_abs <= self.speed_high):
            self.speed = 2
        else:
            self.speed = 3

        if (active_power_abs <= self.stress_high):
            self.load = "Normal"
        elif (active_power_abs <= self.stress_critical):
            self.load = "High"
        else:
            self.load = "Critical"
