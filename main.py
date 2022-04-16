import obd
import time
import msvcrt as m
import os
import json
import numpy as np
import pint

#Go the properties of the connected device, see which COM port is being used to stablish connection.
#In my case it's COM3

connection = obd.OBD(portstr="COM3", baudrate=19200, fast=False) 
Error_Codes = []
Distance = []

def wait():
     m.getch()
     
def reset_dtc_codes():
    reset_dtc = obd.commands.CLEAR_DTC
    connection.query(reset_dtc)
    print("DTC Codes have been cleared.\n")
    
def create_diagnostics_file():
    
    dist_since_codes = obd.commands.DISTANCE_SINCE_DTC_CLEAR
    dist_since_codes_response = connection.query(dist_since_codes)
    distances = dist_since_codes_response.value
    Distance.append(distances.magnitude)  
    

    get_error_codes = obd.commands.GET_DTC
    get_error_codes_response = connection.query(get_error_codes)
    errors = get_error_codes_response.value
    Error_Codes.append(errors)
        
    lists = ["Distance","Error_Codes"]

    data = {listname: globals()[listname] for listname in lists}
    with open('code.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    
    print("Diagnostic File has been created !")

def menu():
    
    choice = "temp"
    while choice != "stop":
        print("""
        1.To reset the DTC codes press
        2.To create a file of the diagnostic data
        3.Exit/Quit
        \n""")
        ans = int(input("Your choice ?"))
        if ans == 1:
            reset_dtc_codes()
            os.system('cls')
        elif ans == 2:
            create_diagnostics_file()
            wait()
            os.system('cls')
        elif ans == 3:
            print("Thank you for using this menu !!")
            choice = "stop"



#calling main menu
menu()