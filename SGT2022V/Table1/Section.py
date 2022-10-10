# File: Section.py
# Version 1.0
# Authors: Jop Merz, Thijs van Elsacker
#
# Description:
# The base of all table sections
# This class controls the MQTT connections and message handlers
#

from Bus import Bus
from Line import Line
from Platform import Platform

import paho.mqtt.client as mqtt
import json

class Section:

    voltage = ""

    def __init__(self, section_name):
        self.name   = section_name
        self.__prefix = section_name + "_"

        self.__mqtt_client    = mqtt.Client()
        self.__mqtt_broker    = "broker.hivemq.com"
        self.__mqtt_topic     = "SmartDemoTable"
        self.__mqtt_port      = 1883
        self.__mqtt_subscribe = self.__mqtt_topic + "/" + section_name + "/Outgoing"
        self.__mqtt_publish   = self.__mqtt_topic + "/" + section_name + "/Ingoing"

        self.buses      = []
        self.lines      = []
        self.components = []
        self.ledstrips  = []

        self.platforms  = []

        self.print_module_messages = False

        self.__scenario    = None

        self.__mqtt_connected    = False
        self.__section_connected = False


    def set_scenario(self, scenario):
        self.__scenario = scenario


    def reload_modules(self):
        for platform in self.platforms:
            RFID_tag = platform.RFID_tag

            module = None

            if (RFID_tag != "0"):
                module = self.__scenario.get_module(RFID_tag)
            
            if (module):
                platform.clear_module()
                platform.add_module(module)


    def get_message_string_all(self):

        command = "{'command': 'Flow Config', 'lines': {"

        for i in range(0, self.num_ledstrips):

            command += '"line {}": '.format(i)
            command += self.ledstrips[i].get_message_string()

            if (i != self.num_ledstrips-1):
                command += ", "

        command += "}}"

        return command


    def get_message_string(self):

        last_ledstrip = 0
        for i in range(0, self.num_ledstrips):
            if self.ledstrips[i].is_changed():
                last_ledstrip = i

        command = "{'command': 'Flow Config', 'lines': {"

        for i in range(0, self.num_ledstrips):
            if (self.ledstrips[i].is_changed() or i == 1):
                command += '"line {}": '.format(i)
                command += self.ledstrips[i].get_message_string()

                if (i != last_ledstrip):
                    command += ", "

        command += "}}"

        return command


    def reset_changed(self):
        for platform in self.platforms:
            platform.reset_changed()


    def has_changed(self):
        for platform in self.platforms:
            if (platform.has_changed()):
                return True
        return False


    def add_line(self, name, bus0, bus1, x, r):
        self.lines.append( Line(self.__prefix + name, bus0=self.__prefix + bus0, bus1=self.__prefix + bus1, x=x, r=r) )


    def add_bus(self, name, v_nom):
        self.buses.append( Bus(self.__prefix + name, v_nom=v_nom) )


    def add_platform(self, bus, voltage, RFID_location, error_lines, RFID_tags):
        self.platforms.append( Platform(self.__prefix+bus, voltage, RFID_location, error_lines, RFID_tags) )


    def reload_components(self):
        self.components.clear()
        for platform in self.platforms:
            for component in platform.components:
                self.components.append(component)


    def section_is_connected(self):
        return self.__section_connected


    def print_module_status(self):
        num_of_platforms = len(self.platforms)
        num_of_modules = 0
        for platform in self.platforms:
            if (platform.module):
                num_of_modules = num_of_modules + 1
        print(self.name + ": Modules -> " + str(num_of_modules) + " / " + str(num_of_platforms))


    def mqtt_set_broker(self, broker):
        self.__mqtt_broker = broker


    def mqtt_set_topic(self, topic):
        self.__mqtt_topic = topic


    def mqtt_is_connected(self):
        return self.__mqtt_connected


    def reboot_section(self):
        self.__mqtt_client.publish(self.__mqtt_publish, "{'command': 'Reboot'}")


    def mqtt_connect(self):
        self.__mqtt_client.on_connect = self.on_connect
        self.__mqtt_client.on_message = self.on_message

        if (self.__mqtt_connected == False):
            self.__mqtt_client.connect(self.__mqtt_broker, self.__mqtt_port)
            self.__mqtt_client.loop_start()


    def mqtt_disconnect(self):
        print(self.name + ": Closing MQTT Client")
        if (self.__mqtt_connected == True):
            self.__mqtt_client.loop_stop()
            self.__mqtt_connected = False


    def mqtt_publish(self):
        self.__mqtt_client.publish(self.__mqtt_publish, self.get_message_string_all())


    def mqtt_publish_if_changed(self):
        changed = False

        for ledstrip in self.ledstrips:
            if (ledstrip.is_changed()):
                changed = True

        # only publish when ledstrips have changed
        if (changed):
            self.__mqtt_client.publish(self.__mqtt_publish, self.get_message_string())

        for ledstrip in self.ledstrips:
            ledstrip.reset_changed_flags()


    def retrieve_modules(self):
        message = "{'command': 'Get Data'}"
        self.__mqtt_client.publish(self.__mqtt_publish, message)


    def is_network_connected(self):
        return True


    def on_connect(self, client, userdata, flags, rc):
        # rc is the error code returned when connecting to the broker
        self.__mqtt_client.subscribe(self.__mqtt_subscribe)

        if(rc != 0):
            print(self.name + ": Error: " + str(rc))
        else:
            self.__mqtt_connected = True
            print(self.name + ": Succesfully started MQTT client")


    def on_message(self, client, userdata, msg):
        message = str(msg.payload.decode("utf-8"))  #removes b'' in string

        try:
            json_message        = json.loads(message)
            module_location     = json_message.get("RFID")
            RFID_tag            = json_message.get("RFID Tag")
            command             = json_message.get("command")
        except:
            return

        if (command):
            if(command == "Table Connected"):
                print(self.name + ": Succesfully connected!")
                self.__section_connected = True
                self.mqtt_publish()

        if (RFID_tag):
            platform = None

            for platform_loop in self.platforms:
                if platform_loop.RFID_location == module_location:
                    platform = platform_loop
                    break

            if (platform != None):
                if (RFID_tag == "0"):

                    platform.clear_module()

                    if (self.print_module_messages):
                        print(self.name + " - " + module_location + " -> Module removed")

                    for errorlines in platform.error_lines:
                        self.ledstrips[errorlines].error = False
                        self.ledstrips[errorlines].refresh()

                    self.mqtt_publish()

                else:
                    module = self.__scenario.get_module(RFID_tag)

                    if (module != None):

                        wrong_platform = True

                        for accepted_module in platform.accepted_modules:
                            for component in module.components:

                                if (accepted_module == module.RFID_tag):
                                    wrong_platform = False

                                if (accepted_module == component.type):
                                    wrong_platform = False

                        if(module.voltage != platform.voltage):
                            wrong_platform = True

                        if (wrong_platform):

                            if (self.print_module_messages):
                                print("Module placed on incorrect platform")
                                print("    Module       -> " + module.name)
                                print("    RFID         -> " + RFID_tag)

                            for errorlines in platform.error_lines:
                                self.ledstrips[errorlines].error = True
                                self.ledstrips[errorlines].refresh()

                            self.mqtt_publish()

                        if (not wrong_platform):
                            platform.add_module(module)

                            if (self.print_module_messages):
                                print(self.name + " -> " + module_location + " -> Module placed" )
                                print("    Module -> " + module.name)
                                print("    RFID   -> " + RFID_tag)

                    else:
                        if (self.print_module_messages):
                            print(self.name + " - " + module_location + " -> Module not found in catalog: " + RFID_tag)
