
# File: Scenario.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Class which represents a scenario, scenarios are loaded from JSON files (for static) and saved here
# Specific Components can be retrieved using the get_modules(RFID) method where you need to provide a RFID id
#

from Generator import Generator
from Load import Load
from StorageUnit import StorageUnit
from Transformer import Transformer

from Module import Module
from os.path import exists

import pandas as pd
import numpy as np
import json

class Scenario:

    def __init__(self):
        self.catalog = {}
        self.static = False
        self.succes = False
        self.index = [0]
        self.index_max = 0
        self.time_per_snapshot = 1
        self.filepath = ""


    def __process_component_value(self, value):

        if (type(value) == str):
            if (value[-4:] == ".csv"):

                pd_csv = pd.read_csv(value)

                np_array = np.array(pd_csv)
                np_array = np_array.flatten()

                pd_series = pd.Series(np_array, index=self.index)

                return pd_series

        # no csv file
        return value


    def load_scenario(self, filepath):
        file_exists = exists(filepath)

        if (file_exists):

            with open(filepath) as json_file:
                self.catalog = json.load(json_file)
                self.succes = True
                self.filepath = filepath
                self.static = self.is_static()
                print("Loaded scenario -> " + filepath)
                print("    Scenario name     -> " + str(self.get_name()))

                if (self.is_static()):
                    print("    Scenario type     -> Static")
                    self.index = [0]
                else:
                    self.index = pd.date_range(self.get_begin_date(), self.get_end_date(), freq=self.get_frequency())
                    self.time_per_snapshot = self.catalog.get("time_per_snapshot")

                    print("    Scenario type     -> Dynamic")
                    print("    Total snapshots   -> " + str(len(self.index)))
                    print("    Time per snapshot -> " + str(self.time_per_snapshot))

        else:
            self.succes = False
            print("Could not load scenario -> " + filepath)

        return self.succes


    def print_scenario(self):
        print("Current scenario...")
        print("    Name    -> " + str(self.get_name()))
        
        if (self.is_static()):
            print("    Type    -> Static")
        else:
            print("    Type    -> Dynamic")


    def is_static(self):
        if str(self.catalog.get("simulation_type")):
            if(self.catalog.get("simulation_type") == "Static"):
                return True
            else:
                return False


    def get_begin_date(self):
        return self.catalog.get("begin_date")


    def get_end_date(self):
        return self.catalog.get("end_date")


    def get_frequency(self):
        return self.catalog.get("frequency")


    def get_name(self):
        return self.catalog.get("name")


    def get_module(self, RFID_tag):

        if (self.succes == False):
            return None

        module = Module()
        module_dict = self.catalog.get(RFID_tag)
        if (module_dict == None):
            return None

        name = module_dict.get("name")
        voltage = module_dict.get("voltage")

        if (name == None):
            print("    No name in module")
            return None

        if (voltage == None):
            print("    No voltage in module...")
            return None

        generators_list     = module_dict.get("generators")
        loads_list          = module_dict.get("loads")
        storages_list       = module_dict.get("storages")
        transformers_list   = module_dict.get("transformer")

        if (generators_list == None and loads_list == None and storages_list == None and transformers_list == None):
            print("    No componments found in module...")
            return None

        module.name         = name
        module.voltage      = voltage
        module.RFID_tag     = RFID_tag

        if (generators_list != None):
            generator_index = 0
            for generator_dict in generators_list:

                generator = Generator()

                generator.name          = str(RFID_tag) + "_Gen" + str(generator_index)
                generator.type          = "Generator"
                generator.p_nom         = generator_dict.get("p_nom") or generator.p_nom
                generator.p_set         = generator_dict.get("p_set") or generator.p_set                
                generator.p_max_pu      = generator_dict.get("p_max_pu") or generator.p_max_pu
                generator.p_min_pu      = generator_dict.get("p_min_pu") or generator.p_min_pu
                generator.p_nom_min     = generator_dict.get("p_nom_min") or generator.p_nom_min
                generator.p_nom_max     = generator_dict.get("p_nom_max") or generator.p_nom_max
                generator.marginal_cost = generator_dict.get("marginal_cost") or generator.marginal_cost
                generator.p_nom_extendable = generator_dict.get("p_nom_extendable") or generator.p_nom_extendable

                pd_p_max_pu = self.__process_component_value(generator.p_max_pu)

                if (generator.p_nom > 0):
                    pd_p_max_pu = pd_p_max_pu / generator.p_nom

                generator.p_max_pu = pd_p_max_pu

                module.add_component(generator)
                generator_index = generator_index + 1

        if (loads_list != None):
            load_index = 0
            for load_dict in loads_list:

                load = Load()

                load.name       = str(RFID_tag) + "_Load" + str(load_index)
                load.type       = "Load"
                load.carrier    = load_dict.get("carrier") or load.carrier
                load.p_set      = load_dict.get("p_set") or load.p_set
                load.q_set      = load_dict.get("q_set") or load.q_set

                pd_p_set = self.__process_component_value(load.p_set)
                load.p_set = pd_p_set

                module.add_component(load)
                load_index = load_index + 1

        if (storages_list != None):
            storage_index = 0
            for storage_dict in storages_list:

                storage = StorageUnit()

                storage.name        = str(RFID_tag) + "_Storage" + str(storage_index)
                storage.type        = "Storage"
                storage.p_nom_min   = storage_dict.get("p_nom_min") or storage.p_nom_min
                storage.p_nom_max   = storage_dict.get("p_nom_max") or storage.p_nom_max
                storage.p_nom_extendable = storage_dict.get("p_nom_extendable") or storage.p_nom_extendable
                storage.marginal_cost = storage_dict.get("marginal_cost") or storage.marginal_cost
                storage.state_of_charge_initial = storage_dict.get("state_of_charge_initial") or storage.state_of_charge_initial

                module.add_component(storage)
                storage_index = storage_index + 1

        if (transformers_list != None):
            transformer_index = 0
            for transformer_dict in transformers_list:

                transformer = Transformer()

                transformer.name       = str(RFID_tag) + "_Transformer" + str(transformer_index)
                transformer.type       = "Transformer"
                transformer.model      = transformer_dict.get("type") or transformer.model

                module.add_component(transformer)
                transformer_index = transformer_index + 1

        return module

