# File: Simulation.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Class which drives the PyPSA calculations and network
# Components are added to a list and this list will be compared with the current network configuration
# If Components are missing, these will be removed from the PyPSA network
# New Components will be added
#
# It is done this way because creating a whole new network each time takes extremly long
#

import pypsa

from Timer import Timer

class Simulation:

    def __init__(self):

        self.network  = pypsa.Network()

        self.__index  = [0]
        self.__static = True

        pypsa.io.logger.disabled  = True
        pypsa.pf.logger.disabled  = True
        pypsa.opf.logger.disabled = True

        self.__export_results = True

        self.static_buses = []
        self.static_lines = []

        # current component list
        self.__components = []

        # new component list
        self.__new_components = []

        self.__num_of_generators    = 0
        self.__num_of_loads         = 0
        self.__num_of_storages      = 0
        self.__num_of_links         = 0

    
    def reset_pypsa_network(self):

        self.network = None
        self.network = pypsa.Network()
        
        self.__components.clear()
        self.__new_components.clear()

        self.__num_of_generators    = 0
        self.__num_of_loads         = 0
        self.__num_of_storages      = 0
        self.__num_of_links         = 0


    def set_buses(self, buses):
        self.static_buses = buses
        for bus in self.static_buses:
            self.network.add("Bus", bus.name, v_nom=bus.v_nom)


    def set_lines(self, lines):
        self.static_lines = lines
        for line in self.static_lines:
            self.network.add("Line", line.name, bus0=line.bus0, bus1=line.bus1, x=line.x, r=line.r, s_nom_extendable=True)


    def clear_components(self):
        self.__new_components.clear()


    def add_component(self, component): 
        self.__new_components.append(component)


    # add Generator into PyPSA network
    def __add_generator(self, generator):

        p_max_pu = generator.p_max_pu

        if (generator.p_nom > 0):
            p_max_pu = p_max_pu / generator.p_nom

        self.__components.append(generator) 
        self.__num_of_generators = self.__num_of_generators + 1  

        self.network.add(
            "Generator", 
            name=generator.name, 
            bus=generator.bus0, 
            p_set=generator.p_set,
            p_nom=generator.p_nom,
            p_nom_min=generator.p_nom_min,
            p_nom_max=generator.p_nom_max,
            p_max_pu=p_max_pu,
            p_min_pu=generator.p_min_pu,
            marginal_cost=generator.marginal_cost,
            p_nom_extendable=generator.p_nom_extendable)


    # add Load into PyPSA network
    def __add_load(self, load):

        self.__components.append(load)
        self.__num_of_loads = self.__num_of_loads + 1
        self.network.add(
        "Load",
        name=load.name,
        bus=load.bus0,
        p_set=load.p_set,
        q_set=load.q_set)


    # add StorageUnit into PyPSA network
    def __add_storage(self, storage): 
        self.__components.append(storage)
        self.__num_of_storages = self.__num_of_storages + 1
        self.network.add(
        "StorageUnit",
        name=storage.name,
        bus=storage.bus0,
        p_nom_min=storage.p_nom_min,
        p_nom_max=storage.p_nom_max,
        p_nom_extendable=storage.p_nom_extendable,
        marginal_cost=storage.marginal_cost,
        state_of_charge_initial=storage.state_of_charge_initial)


    # add dynamic line into PyPSA network
    def __add_link(self, line):
        self.__components.append(line)     
        self.__num_of_links = self.__num_of_links + 1

        self.network.add(
        "Link",
        name=line.name,
        bus0=line.bus0,
        bus1=line.bus1,
        p_nom_extendable=True)


    # remove Generator from PyPSA network
    def __remove_generator(self, generator):
        self.network.remove("Generator", name=generator.name)
        self.__num_of_generators = self.__num_of_generators - 1
        self.__components.remove(generator)


    # remove Load from PyPSA network
    def __remove_load(self, load):
        self.network.remove("Load", name=load.name)
        self.__num_of_loads = self.__num_of_loads - 1
        self.__components.remove(load)


    # remove StorageUnit from PyPSA network
    def __remove_storage(self, storage):
        self.network.remove("StorageUnit", name=storage.name)
        self.__num_of_storages = self.__num_of_storages - 1
        self.__components.remove(storage)


    # remove StorageUnit from PyPSA network
    def __remove_link(self, line):
        self.network.remove("Link", name=line.name)
        self.__num_of_links = self.__num_of_links - 1
        self.__components.remove(line)


    def get_num_of_generators(self):
        return self.__num_of_generators


    def get_num_of_loads(self):
        return self.__num_of_loads


    def get_num_of_storages(self):
        return self.__num_of_storages


    def get_num_of_lines(self):
        return self.__num_of_lines


    def set_index(self, index):
        self.__index = index


    def enable_static(self):
        self.__static = True


    def enable_dynamic(self):
        self.__static = False


    def pf(self):
        timer = Timer()
        timer.start()

        succes = True

        try:
            status = self.network.pf()
            print("PF network update SUCCES! -> solution possible")
        except:
            print("PF network update FAILED! -> no solution possible")
            succes = False

        timer.stop()
        print(f"    PyPSA took  -> {timer.elapsed_time:0.6f} seconds")

        if (self.__export_results):
            timer.start()
            self.network.export_to_csv_folder("Export/PyPSA_pf")
            timer.stop()

            print(f"    Export took -> {timer.elapsed_time:0.6f} seconds")

        return succes


    def lpf(self):
        timer = Timer()
        timer.start()

        succes = True

        try:
            status = self.network.lpf()
            print("LPF network update SUCCES! -> solution possible")
        except:
            print("LPF network update FAILED! -> no solution possible")
            succes = False

        timer.stop()
        print(f"    PyPSA took  -> {timer.elapsed_time:0.6f} seconds")

        if (self.__export_results):
            timer.start()
            self.network.export_to_csv_folder("Export/PyPSA_lpf")
            timer.stop()

            print(f"    Export took -> {timer.elapsed_time:0.6f} seconds")

        return succes


    def lopf(self):

        timer = Timer()
        timer.start()
      
        succes = True

        try:
            status = self.network.lopf()

            if (status[0] == "ok" and status[1] == "optimal"):
                print("LOPF network update SUCCES! -> solution possible")
            else:
                print("LOPF network update FAILED with -> no solution possible")
                succes = False

            print("    Static      -> " + str(self.__static))
            print("    Status      -> " + status[0])
            print("    Condition   -> " + status[1])
            
        except:
            print("LOPF network update FAILED! -> no solution possible")
            succes = False

        timer.stop()
        print(f"    PyPSA took  -> {timer.elapsed_time:0.6f} seconds")

        if (self.__export_results):
            timer.start()
            #self.network.export_to_csv_folder("Export/PyPSA_lopf") # this code create an error
            timer.stop()

            print(f"    Export took -> {timer.elapsed_time:0.6f} seconds")

        return succes


    def update_network(self):

        self.network.set_snapshots(self.__index)

        # components to be removed from PyPSA network
        remove_generators = []
        remove_loads      = []
        remove_storages   = []
        remove_links      = []

        # components to be added into PyPSA network
        add_generators = []
        add_loads      = []
        add_storages   = []
        add_links      = []

        # check which components are already in PyPSA. If not, add them
        for new_component in self.__new_components:

            add_component   = True

            for component in self.__components:
                if (new_component.name == component.name):
                    add_component = False

            if (add_component):
                if (new_component.type == "Generator"):
                    add_generators.append (new_component)

                if (new_component.type == "Load"):
                    add_loads.append (new_component)

                if (new_component.type == "Storage"):
                    add_storages.append (new_component)

                if (new_component.type == "Link"):
                    add_links.append (new_component)

        # check which generators should be removed from PyPSA
        for component in self.__components:  

            remove_component = True

            for new_component in self.__new_components:
                if (component.name == new_component.name):
                    remove_component = False

            if (remove_component == True):
                if (component.type == "Generator"):
                    remove_generators.append(component)

                if (component.type == "Load"):
                    remove_loads.append(component)

                if (component.type == "Storage"):
                    remove_storages.append(component)

                if (component.type == "Link"):
                    remove_links.append(component)

        # remove old components from PyPSA network
        for generator in remove_generators:
            self.__remove_generator(generator)

        for load in remove_loads:
            self.__remove_load(load)

        for storage in remove_storages:
            self.__remove_storage(storage)

        for link in remove_links:
            self.__remove_link(link)

        # add new components to PyPSA network
        for generator in add_generators:
            self.__add_generator(generator)

        for load in add_loads:
            self.__add_load(load)

        for storage in add_storages:
            self.__add_storage(storage)

        for link in add_links:
            self.__add_link(link)
