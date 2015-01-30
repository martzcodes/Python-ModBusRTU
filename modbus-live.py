import minimalmodbus as minmod
import serial
import os
import json
import datetime
import time

# check for modbus.json

if not os.path.isfile('./modbus.json'):
	print('No modbus.json found, please create one')
	quit()

mods = json.load(open('./modbus.json'))

while True:
    d = datetime.datetime.now()
    for mod in mods:
            for channel in mod['channels']:
                    try:
                            instrument = minmod.Instrument(mod['comport'],channel['channel'])
                    except serial.SerialException:
                            print("Wrong com port, or it's not connected")
                            quit()

                    instrument.serial.baudrate = mod['baudrate']
                    instrument.serial.bytesize = mod['bytesize']
                    instrument.serial.stopbits = mod['stopbits']
                    instrument.serial.timeout = mod['timeout']
         
                    #instrument.debug = True

                    if mod['parity'] == "O":
                            instrument.serial.parity = serial.PARITY_ODD

                    if mod['parity'] == "E":
                            instrument.serial.parity = serial.PARITY_EVEN

                    if mod['parity'] == "N":
                            instrument.serial.parity = serial.PARITY_NONE

                    writestring = ("{},{}").format(d.hour*60*60+d.minute*60+d.second,channel['channel'])
                    try:
                            writestring+= (",{}").format(instrument.read_string(103))
                    except ValueError as e:
                            print(e)
                    for register in mod['registers']:
                            writestring += ","
                            value = -1
                            if register['only'] == "" or register['only'] == channel['type']:
                                    if register['float'] != -1:
                                            try:
                                                    #value = instrument.read_float(register['float'])
                                                    values = instrument.read_registers(register['float'],numberOfRegisters=2)
                                                    registerstring = chr(values[1].to_bytes(2,byteorder='big')[0]) + chr(values[1].to_bytes(2,byteorder='big')[1]) + chr(values[0].to_bytes(2,byteorder='big')[0]) + chr(values[1].to_bytes(2,byteorder='big')[1])
                                                    value = minmod._bytestringToFloat(registerstring)
                                            except ValueError as e:
                                                    print(e)

                            writestring += ("{}").format(value)

                    writestring += "\n"
                    print(writestring)
            time.sleep(5)
