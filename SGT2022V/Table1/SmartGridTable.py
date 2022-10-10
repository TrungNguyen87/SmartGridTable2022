# File: SmartgridTable.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# The class which connects all the objects together
# SmartGridTable containes multiple sections and the links between them
# At network refresh, all components will be retrieved from all sections and placed in the Simulation 
# When finished the results are loaded back into the sections, which will publish over MQTT
#

from Section_HV import Section_HV
from Section_MV import Section_MV
from Section_LV import Section_LV
from Section_MV_Ring import Section_MV_Ring

from Simulation import Simulation
from SectionLink import SectionLink
from ScenarioManager import ScenarioManager
from Link import Link
from Line import Line
from TransformerLink import TransformerLink

from Timer import Timer

class SmartGridTable:

    def __init__(self):

        self.__simulation  = Simulation()

        self.buses         = []
        self.lines         = []
        self.components    = []

        self.__simulation_succes = False
        self.__elapsed_time     = 0
        self.__snapshot_index   = 0
        self.__snapshot_index_max = 0
        self.snapshot_changed   = False
        self.simulation_changed = False

        self.__table_sections = []
        self.__section_links  = []
        self.__transformer_links = []

        # manager of static scenarios
        self.__static_scenario_manager  = ScenarioManager(r"Static/")
        self.__dynamic_scenario_manager = ScenarioManager(r"Dynamic/")
        self.__current_scenario_manager = self.__static_scenario_manager
        self.__static = True

        # scenario containing all module data (generators, loads, storages and transformers)
        self.__current_scenario = self.__static_scenario_manager.get_current_scenario()

        # table sections
        self.__table_sections.append( Section_HV("Table1") )
        self.__table_sections.append( Section_MV_Ring("Table2") )
        self.__table_sections.append( Section_MV("Table3") )
        self.__table_sections.append( Section_LV("Table4") )
        self.__table_sections.append( Section_LV("Table5") )
        self.__table_sections.append( Section_LV("Table6") )

        # static connections between table sections
        self.__section_links.append( SectionLink("Table2", "bus0",  "Table3", "bus0") )
        self.__section_links.append( SectionLink("Table2", "bus4",  "Table3", "bus21") )

        # dynamic connections (transformers) between table sections
        self.__transformer_links.append( TransformerLink("Table1", "RFID 0", "Table1", "bus5",  "Table2", "bus12") )
        self.__transformer_links.append( TransformerLink("Table1", "RFID 3", "Table1", "bus9",  "Table2", "bus15") )
        self.__transformer_links.append( TransformerLink("Table4", "RFID 0", "Table3", "bus11", "Table4", "bus13") )
        self.__transformer_links.append( TransformerLink("Table5", "RFID 0", "Table2", "bus8",  "Table5", "bus13") )
        self.__transformer_links.append( TransformerLink("Table6", "RFID 0", "Table2", "bus19", "Table6", "bus13") )

        self.network_reload_static()

        self.__simulation.set_buses(self.buses)
        self.__simulation.set_lines(self.lines)
        self.__simulation.enable_static()

        self.modules_reload()
        self.modules_reset_changed()
        

    #-------------------------------
    # Table sections
    #-------------------------------

    def table_reboot_all(self):
        for section in self.__table_sections:
            section.reboot_section()


    def table_reboot(self, table_name):
        found = False

        for section in self.__table_sections:
            if (section.name == table_name):
                section.reboot_section()
                found = True

        if (found == False):
            print("Table not found -> " + table_name)


    def table_shutdown(self, table_name):
        found = False

        for section in self.__table_sections:
            if (section.name == table_name):
                section.reboot_section()
                section.mqtt_disconnect()
                found = True

        if (found == False):
            print("Table not found -> " + table_name)


    def table_poweron(self, table_name):
        found = False

        for section in self.__table_sections:
            if (section.name == table_name):
                section.mqtt_connect()
                section.reboot_section()
                found = True

        if (found == False):
            print("Table not found -> " + table_name)


    def table_print_list(self):
        for section in self.__table_sections:
            print(section.name)


    def table_retrieve_modules(self):
        for section in self.__table_sections:
            section.retrieve_modules()


    def table_is_connected(self):
        connected_sections = 0
        for section in self.__table_sections:
            if (section.section_is_connected() == True):
                connected_sections = connected_sections + 1

        if (connected_sections == len(self.__table_sections)):
            return True
        return False

    #-------------------------------
    # Modules
    #-------------------------------

    def modules_print_status(self):
        for section in self.__table_sections:
            section.print_module_status()


    def modules_enable_messages(self, enable):
        for section in self.__table_sections:
            section.print_module_messages = enable


    def modules_reload(self):
        self.__simulation.clear_components()
        self.__simulation.update_network()

        for section in self.__table_sections:
            section.set_scenario(self.__current_scenario)
            section.reload_modules()


    def modules_if_changed(self):
        for section in self.__table_sections:
            if (section.has_changed()):
                return True
        return False


    def modules_reset_changed(self):
        for section in self.__table_sections:
            section.reset_changed()

    #-------------------------------
    # Scenario
    #-------------------------------

    def scenario_refresh_list(self):
        self.__static_scenario_manager.reload_scenarios()
        self.__dynamic_scenario_manager.reload_scenarios()

        self.__current_scenario_manager = self.__static_scenario_manager
        self.__current_scenario = self.__static_scenario_manager.get_current_scenario()


    def scenario_set(self, scenario_name, static):

        if (static == True):
            status = self.__static_scenario_manager.set_scenario(scenario_name)
            if (status == True):
                self.__current_scenario_manager = self.__static_scenario_manager

        else:
            status = self.__dynamic_scenario_manager.set_scenario(scenario_name)
            if (status == True):
                self.__current_scenario_manager = self.__dynamic_scenario_manager


        if (status):
            self.__current_scenario = self.__current_scenario_manager.get_current_scenario()
            self.__current_scenario.print_scenario()

            self.__snapshot_index   = 0
            self.__elapsed_time     = 0

            if (self.__current_scenario.is_static() == False):

                self.__simulation.set_index(self.__current_scenario.index)
                self.__simulation.enable_dynamic()

                self.__static = False

            else:
                self.__static = True
                self.__simulation.enable_static()

            self.modules_reload()

        else:
            print("No scenario found with name -> " + scenario_name)


    def scenario_print_current(self):
        self.__current_scenario.print_scenario()


    def scenario_print_list(self):
        self.__static_scenario_manager.print_scenario_list()
        self.__dynamic_scenario_manager.print_scenario_list()

    #-------------------------------
    # MQTT
    #-------------------------------

    def mqtt_connect(self):
        for section in self.__table_sections:
            section.mqtt_connect()


    def mqtt_disconnect(self):
        for section in self.__table_sections:
            section.reboot_section()
            section.mqtt_disconnect()


    def mqtt_publish(self):
        for section in self.__table_sections:
            section.mqtt_publish()


    def mqtt_publish_if_changed(self):
        for section in self.__table_sections:
            section.mqtt_publish_if_changed()


    def mqtt_set_broker(self, broker):
        for section in self.__table_sections:
            section.mqtt_set_broker(broker)


    def mqtt_is_connected(self):
        connected_sections = 0
        for section in self.__table_sections:
            if (section.mqtt_is_connected() == True):
                connected_sections = connected_sections + 1

        if (connected_sections == len(self.__table_sections)):
            return True
        return False

    #-------------------------------
    # PyPSA network
    #-------------------------------

    def network_lopf(self):

        self.__simulation.set_index(self.__current_scenario.index)
        self.simulation_changed = True
        
        self.network_refresh()

        for section in self.__table_sections:
            section.active = section.is_network_connected()

        self.__simulation_succes = self.__simulation.lopf()

        if (self.__simulation_succes == False):
            for section in self.__table_sections:
                section.active = False
            self.ledstrips_update_active()

        else:
            if (self.__static):
                self.ledstrips_update_from_simulation(0)
            else:
                self.ledstrips_update_from_simulation(self.__snapshot_index)

        self.mqtt_publish()


    def network_lpf(self):

        self.network_refresh()

        for section in self.__table_sections:
            section.active = section.is_network_connected()

        if (self.__simulation.lpf() == False or self.__simulation.get_num_of_generators() == 0):
            for section in self.__table_sections:
                section.active = False
            self.ledstrips_update_active()

        else:
            self.ledstrips_update_from_simulation(0)

        self.mqtt_publish()


    def network_pf(self):

        self.network_refresh()

        for section in self.__table_sections:
            section.active = section.is_network_connected()

        if (self.__simulation.pf() == False or self.__simulation.get_num_of_generators() == 0):
            for section in self.__table_sections:
                section.active = False
            self.ledstrips_update_active()

        else:
            self.ledstrips_update_from_simulation(0)

        self.mqtt_publish()


    def network_reload_static(self):
        self.buses.clear()
        self.lines.clear()

        for section in self.__table_sections:
            for bus in section.buses:
                self.buses.append(bus)

            for line in section.lines:
                self.lines.append(line)

        for link in self.__section_links:
            new_line = Line(link.name, link.bus0, link.bus1, 0.1, 0.01)
            self.lines.append(new_line)


    def network_reload_components(self):
        self.components.clear()

        for section in self.__table_sections:
            section.reload_components()

            if (section.is_network_connected()):
                # generators, loads and storages
                for component in section.components:
                    self.components.append(component)

                # links between table sections which require transformers
                for link in self.__transformer_links:
                    if (link.RFID_table == section.name):
                        for platform in section.platforms:
                            if (platform.RFID_location == link.RFID):
                                if (platform.module != None):
                                    new_link = Link(link.name, link.bus0, link.bus1, True)
                                    self.components.append(new_link)


    def network_refresh(self):

        timer = Timer()
        timer.start()

        self.network_reload_components()

        self.__simulation.clear_components()

        for component in self.components:
            self.__simulation.add_component(component)

        self.__simulation.update_network()

        self.modules_reset_changed()

        timer.stop()
        print(f"PyPSA network reload took -> {timer.elapsed_time:0.6f} seconds")


    #-------------------------------
    # Miscellaneous
    #-------------------------------

    def ledstrips_update_from_simulation(self, index):
        for section in self.__table_sections:
            for ledstrip in section.ledstrips:
                ledstrip.active_power = self.__simulation.network.lines_t.p0[ledstrip.line][index]
                ledstrip.active = section.active
                ledstrip.refresh()


    def ledstrips_update_active(self):
        for section in self.__table_sections:
            for ledstrip in section.ledstrips:
                ledstrip.active = section.active
                ledstrip.refresh()


    def ledstrips_update_active_section(self, name):
        for section in self.__table_sections:
            if (section.name == name):
                for ledstrip in section.ledstrips:
                    ledstrip.active =  section.active
                    ledstrip.refresh()


    def append_delta_time(self, delta_time):
        if (self.__current_scenario.is_static() == False):
            self.__elapsed_time = self.__elapsed_time + delta_time

    
    def update(self):
        if (self.__current_scenario.is_static() == False):
            if(self.__elapsed_time > self.__current_scenario.time_per_snapshot):

                self.__elapsed_time = 0
                self.snapshot_changed = True

                self.ledstrips_update_from_simulation(self.__snapshot_index)
                self.mqtt_publish()

                self.__snapshot_index = self.__snapshot_index + 1

                total_snapshots = len(self.__current_scenario.index)

                if (self.__snapshot_index >= total_snapshots):
                    self.__snapshot_index = 0


    def get_simulation_succes(self):
        return self.__simulation_succes


    def get_current_snapshot(self):
        index = self.__current_scenario.index
        return index[self.__snapshot_index]


    def get_snapshots(self):
        return self.__current_scenario.index


    def get_generators_generation(self):
        if (self.__simulation_succes == True):
            return self.__simulation.network.generators_t.p
        return None
            

    def get_load_consumption(self):
        if (self.__simulation_succes == True):
            return self.__simulation.network.loads_t.p
        return None
