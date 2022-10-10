
# File: GUI_MQTT.py
# Version 0.0
# Authors: Jop Merz
#
# Description:
# 
#

from pickle import NONE
import paho.mqtt.client as mqtt
import json

class GUI_MQTT:

    def __init__(self):
        self.__mqtt_client    = mqtt.Client()
        self.__mqtt_broker    = NONE #"broker.hivemq.com"
        self.__mqtt_topic     = "SmartDemoTable/GUI"
        self.__mqtt_port      = 1883
        self.__mqtt_subscribe = self.__mqtt_topic + "/Outgoing"
        self.__mqtt_publish   = self.__mqtt_topic + "/Ingoing"
        self.__mqtt_connected = False
        self.message_buffer = []

    
    def mqtt_set_broker(self, broker):
        self.__mqtt_broker = broker


    def mqtt_set_topic(self, topic):
        self.__mqtt_topic = topic


    def mqtt_set_port(self, port):
        self.__mqtt_port = 1883


    def mqtt_connect(self):
        self.__mqtt_client.on_connect = self.on_connect
        self.__mqtt_client.on_message = self.on_message

        if (self.__mqtt_connected == False):
            self.__mqtt_client.connect(self.__mqtt_broker, self.__mqtt_port)
            self.__mqtt_client.loop_start()
    

    def mqtt_disconnect(self):
        if (self.__mqtt_connected == True):
            self.__mqtt_client.loop_stop()
            self.__mqtt_connected = False


    def mqtt_publish(self, message):
        self.__mqtt_client.publish(self.__mqtt_publish, message)


    def publish_snapshot(self, snapshot):
        raw = {"current_snapshot": str(snapshot)}
        message = json.dumps(raw)
        self.mqtt_publish(message)


    def publish_dataframe(self, dataframe):
        result = dataframe.to_json()
        parsed = json.loads(result)
        json_string = json.dumps(parsed, indent=4) 
        self.mqtt_publish(json_string)


    def on_connect(self, client, userdata, flags, rc):
        self.__mqtt_client.subscribe(self.__mqtt_subscribe)

        if(rc != 0):
            print("GUI: Error: " + str(rc))
        else:
            self.__mqtt_connected = True
            print("GUI: Succesfully started GUI MQTT client")


    def on_message(self, client, userdata, msg):
        message = str(msg.payload.decode("utf-8"))  #removes b'' in string

        try:
            json_message        = json.loads(message)
            command             = json_message.get("command")
        except:
            return

        if (command):
            self.message_buffer.append(command)

