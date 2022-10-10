# File: Application.py
# Version 1.1
# Authors: Jop Merz, Thijs van Elsacker
#
# Description:
# Entry point of the program
# Handles the setup of the table sections, user console input and exit sequence
#

# we take the local ip address and put it as local broker (the broker server need to run on the same computer than the one executing the code)
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_broker_ip = s.getsockname()[0]# local broker ip is the ip of the computer executing the program
mqtt_public_broker = "broker.hivemq.com"

from json import loads
from time import sleep
from SmartGridTable import SmartGridTable
from threading import Thread

from GUI_MQTT import GUI_MQTT

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# global stuff
force_update = False
mode = "lopf"

global_console_input = ""

running = True

print("----------------------------------------------------------------")
print("--------------- Loading SmartGridTable scenarios ---------------")
print("----------------------------------------------------------------")

table = SmartGridTable()
mqtt_gui = GUI_MQTT()

def print_help_commands():
    print("----------------------------------------------------------------")
    print("help                     -> Print all commands")
    print("shutdown                 -> Close the program")
    print("mqtt public              -> Switch to public MQTT broker") # commande supprime--------------
    print("mqtt local               -> Switch to local MQTT broker") # commande supprime--------------
    print("table list               -> Print the names of all table sections")
    print("table reboot all         -> Reboot all table sections")
    print("table reboot [SECTION]   -> Reboot given table section")
    print("table shutdown [SECTION] -> Shutdown the given table section")
    print("table poweron [SECTION]  -> Boot up the given table section")
    print("scenario reload          -> Find and reload all scenarios in Static/")
    print("scenario list            -> Print the names of all available scenarios")
    print("scenario current         -> Print the current active scenario")
    print("scenario set -s [NAME]   -> Switch to given static scenario")
    print("scenario set -d [NAME]   -> Switch to given dynamic scenario")
    print("mode set lopf            -> Set calculation type to Linear Optimal Power Flow (LOPF)")
    print("mode set lpf             -> Set calculation type to Linear Power Flow (LPF)")
    print("mode set pf              -> Set calculation type to Power Flow (PF)")
    print("modules list             -> Print the number of modules placed on each table section")
    print("calculate                -> PyPSA simulation refresh")
    print("----------------------------------------------------------------")


def console_handler(input):

    global force_update
    global mode
    global running

    console_input = input.split()
    known_command = False

    if (len(console_input) >= 1):

        # global commands
        if (console_input[0] == "help"):
            print_help_commands()
            known_command = True

        if (console_input[0] == "shutdown"):
            print("Shutting down program...")
            running = False
            known_command = True

        if (console_input[0] == "calculate"):
            print("Forcing simulation update...")
            force_update = True
            known_command = True

        if (console_input[0] == "modules"):
            if (len(console_input) >= 2):
                if (console_input[1] == "list"):
                    table.modules_print_status()
                    known_command = True
                    print("----------------------------------------------------------------")

        # table commands
        if (console_input[0] == "table"):
            if (len(console_input) >= 2):
                if (console_input[1] == "list"):
                    table.table_print_list()
                    known_command = True
                    print("----------------------------------------------------------------")

                if (console_input[1] == "reboot"):
                    if (len(console_input) >= 3):
                        if (console_input[2] == "all"):
                            print("Restarting all table sections...")
                            table.table_reboot_all()
                            known_command = True
                            print("----------------------------------------------------------------")
                        else:
                            print("Restarting section -> " + console_input[2])
                            table.table_reboot(console_input[2])
                            known_command = True
                            print("----------------------------------------------------------------")

                if (console_input[1] == "shutdown"):
                    if (len(console_input) >= 3):
                        if (console_input[2] == "all"):
                            print("Shutting down all table sections...")
                            table.mqtt_disconnect()
                            known_command = True
                            print("----------------------------------------------------------------")
                        else:
                            print("Shutting down section -> " + console_input[2])
                            table.table_shutdown(console_input[2])
                            known_command = True
                            print("----------------------------------------------------------------")

                if (console_input[1] == "poweron"):
                    if (len(console_input) >= 3):
                        if (console_input[2] == "all"):
                            print("Activating all table sections...")
                            table.mqtt_connect()
                            known_command = True
                            print("----------------------------------------------------------------")
                        else:
                            print("Activating section -> " + console_input[2])
                            table.table_poweron(console_input[2])
                            known_command = True
                            print("----------------------------------------------------------------")

        # scenario commands
        if (console_input[0] == "scenario"): 
            if (len(console_input) >= 2):
                if (console_input[1] == "reload"):
                    print("Reloading scenarios...")
                    table.scenario_refresh_list()
                    known_command = True
                    print("----------------------------------------------------------------")

                if (console_input[1] == "list"):
                    table.scenario_print_list()
                    known_command = True
                    print("----------------------------------------------------------------")

                if (console_input[1] == "current"):
                    table.scenario_print_current()
                    known_command = True
                    print("----------------------------------------------------------------")

                if (console_input[1] == "set"):
                    if (len(console_input) >= 3):
                        if (console_input[2] == "-s"):
                            if (len(console_input) >= 4):
                                table.scenario_set(console_input[3], static=True)
                                known_command = True
                                print("----------------------------------------------------------------")

                        if (console_input[2] == "-d"):
                            if (len(console_input) >= 4):
                                table.scenario_set(console_input[3], static=False)
                                known_command = True
                                print("----------------------------------------------------------------")

        # mode commands
        if (console_input[0] == "mode"):
            if (len(console_input) >= 2):
                if (console_input[1] == "set"):
                    if (len(console_input) >= 3):
                        if (console_input[2] == "lopf"):
                            print("Setting mode to Linear Optimal Power Flow (LOPF)")
                            mode = "lopf"
                            known_command = True
                            force_update = True

                        if (console_input[2] == "lpf"):
                            print("Setting mode to Linear Power Flow (LPF)")
                            mode = "lpf"
                            known_command = True
                            force_update = True

                        if (console_input[2] == "pf"):
                            print("Setting mode to Power Flow (PF)")
                            mode = "pf"
                            known_command = True
                            force_update = True

        if (known_command == False):
            print("Unknown command -> " + input)
            print("Type help for all available commands")

# keyboard input
def console_thread():

    global global_console_input
    global running

    while(running):    
        global_console_input = input()

        if (global_console_input == "shutdown"):
            break


# main table routine

refresh_rate = 0.02
publish_update_rate = 20


# ask to chose local or public broker
print("\nDo you want a local broker or public broker ? \n '1' local broker \n '2' public broker")
choice_broker = input()
selection_valid = 0
while(selection_valid == 0):
    if (choice_broker == "1") :
        actual_broker = local_broker_ip
        selection_valid = 1
    elif (choice_broker == "2") :
        actual_broker = mqtt_public_broker
        selection_valid = 1
    else:
        print("invalid choice! \n select '1' for local or '2' for public broker \n")
        choice_broker = input()
    
mqtt_gui.mqtt_set_broker(actual_broker)


print("----------------------------------------------------------------")
print("-------------------- Starting MQTT clients ---------------------")
print("----------------------------------------------------------------")

mqtt_gui.mqtt_connect()
table.mqtt_connect()

while(table.mqtt_is_connected() == False):
    sleep(refresh_rate)

print("----------------------------------------------------------------")
print("------------ Connecting to SmartGridTable sections -------------")
print("----------------------------------------------------------------")

table.table_reboot_all()
table.modules_enable_messages(False)

timer = 0
timer_limit = 10.0
timeout_limit = 15.0
timeout = False

while(table.table_is_connected() == False and timeout == False):

    sleep(refresh_rate)
    timer = timer + refresh_rate

    if (timer >= timer_limit):
        time_left = timeout_limit - timer_limit
        print("Timeout in [" + str(time_left) + "] seconds...")
        timer_limit = timer_limit + 1.0

    if (timer >= timeout_limit):
        print("Timeout when trying to connect...")
        timeout = True

print("----------------------------------------------------------------")
print("-------------- Retrieving SmartGridTable Modules ---------------")
print("----------------------------------------------------------------")

table.table_retrieve_modules()

# sleep so network modules are loaded without triggering a PyPSA update
sleep(4.0)

table.modules_print_status()
table.modules_enable_messages(True)

print("----------------------------------------------------------------")
print("------------- SmartGridTable 2022 up and running! --------------")
print("----------------------------------------------------------------")

# seperate thread so table routine keeps running during keyboard input
# (keyboard input stalls main thread)
console_thread = Thread(target=console_thread)
console_thread.start()

timer = 0

# main routine
while(running):

    sleep(refresh_rate)

    # GUI mqtt message handler
    if (len(mqtt_gui.message_buffer) > 0):
        for message in mqtt_gui.message_buffer:
            console_handler(message)
        mqtt_gui.message_buffer.clear()

    # Console input message handler
    if (global_console_input != ""):
        console_handler(global_console_input)
        global_console_input  = ""

    table.append_delta_time(refresh_rate)
    table.update()

    timer = timer + refresh_rate

    if(table.modules_if_changed() or force_update == True):
        force_update = False
        timer = 0

        if (mode == "lopf"):
            table.network_lopf()
            print("----------------------------------------------------------------")

        if (mode == "lpf"):
            table.network_lpf()
            print("----------------------------------------------------------------")

        if (mode == "pf"):
            table.network_pf()
            print("----------------------------------------------------------------")


    if (table.simulation_changed == True):
        table.simulation_changed = False

        if (table.get_simulation_succes() == True):

            generators  = table.get_generators_generation()
            loads       = table.get_load_consumption()

            if (len(generators) > 0):
                mqtt_gui.publish_dataframe(generators)

            if (len(loads) > 0):
                mqtt_gui.publish_dataframe(loads)
        

    if (table.snapshot_changed == True):
        table.snapshot_changed = False
        mqtt_gui.publish_snapshot(table.get_current_snapshot())


    if(timer >= publish_update_rate):
        table.mqtt_publish()
        timer = 0


# on program shutdown
console_thread.join()
table.mqtt_disconnect()

print("----------------------------------------------------------------")
print("----------------- Goodbye, until next time! --------------------")
print("----------------------------------------------------------------")

exit()
