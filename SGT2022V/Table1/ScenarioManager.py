# File: ScenarioManager.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Class which search a directory for JSON files and creates Scenario objects respectively
# Only one scenario can be active and is returned with the get_current_scenario() method
# Scenarios can be selected with the set_scenario(name) method 
# A name must be provided with this method, these are stored in the JSON files under "name"
#

from Timer import Timer
from Scenario import Scenario
import glob

class ScenarioManager:

    def __init__(self, rootpath):
        self.scenarios = []
        self.scenario_files = []
        self.scenario_root = rootpath
        self.current_scenario = None
        self.succes = False

        self.reload_scenarios()


    def reload_scenarios(self):
        path = self.scenario_root + r"*.json"
        scenario_paths = glob.glob(path)
        print("Scenario search succesfull")
        print("    Root  -> " + self.scenario_root)
        print("    Found -> " + str(len(scenario_paths)))

        self.scenarios.clear()

        for scenario_file in scenario_paths:
            scenario = Scenario()
            scenario.load_scenario(scenario_file)
            self.scenarios.append(scenario)

        self.current_scenario = None

        if (self.scenarios[0]):
            self.set_scenario(self.scenarios[0].get_name())


    def set_scenario(self, scenario_name):
        for scenario in self.scenarios:
            if scenario.get_name() == scenario_name:
                self.current_scenario = scenario
                return True
        # no scenario found
        return False


    def print_scenario_list(self):
        for scenario in self.scenarios:
            print(scenario.get_name())

    
    def get_current_scenario(self):
        return self.current_scenario
