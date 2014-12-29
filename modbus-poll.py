import minimalmodbus as minmod
import serial
import os
import json
import datetime

# check for modbus.json

channelsize = 247 #0 to 247
channelrange = range(0,channelsize)
regsize = 5
regrange = range(0,regsize)
found = []

if not os.path.isfile('./modbus.json'):
    print('No modbus.json found, please create one')
    quit()
mods = json.load(open('./modbus.json'))

for mod in mods:
    for register in regrange:
        for channel in channelrange:
            if not channel in found:
                try:
                    instrument = minmod.Instrument(mod['comport'],channel)
                except serial.SerialException:
                    print("Wrong com port, or it's not connected")
                    quit()
        
                instrument.serial.baudrate = mod['baudrate']
                instrument.serial.bytesize = mod['bytesize']
                instrument.serial.stopbits = mod['stopbits']
                instrument.serial.timeout = mod['timeout']

                if mod['parity'] == "O":
                    instrument.serial.parity = serial.PARITY_ODD

                if mod['parity'] == "E":
                    instrument.serial.parity = serial.PARITY_EVEN

                if mod['parity'] == "N":
                    instrument.serial.parity = serial.PARITY_NONE

                try:
                    instrument.read_register(register)
                except IOError as e:
                    print(e)
                    print(("Nothing on channel {} at register {}").format(channel,register))
                    print(found)
                else:
                    found.append(channel)
                    print(found)