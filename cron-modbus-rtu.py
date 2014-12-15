import minimalmodbus as minmod
import serial
import os
import json
import datetime

# check for modbus.json

if not os.path.isfile('./modbus.json'):
    print('No modbus.json found, please create one')
    quit()
mods = json.load(open('./modbus.json'))

d = datetime.datetime.now()

datapath = './modbus-data/'

if not os.path.isdir(datapath):
    os.mkdir(datapath)

todaypath = datapath + ('{}-{}/').format(d.year,d.month)

if not os.path.isdir(todaypath):
    os.mkdir(todaypath)

for mod in mods:
    for channel in mod['channels']:
        print(mod['channels'])
        try:
            instrument = minmod.Instrument(mod['comport'],channel['channel'])
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
            
        writestring = ("{},{}").format(d.hour*60*60+d.minute*60+d.second,channel['channel'])
        for register in mod['registers']:
            writestring += ","
            value = -1
            if register['only'] == "" or register['only'] == channel['type']:
                try:
                    x = instrument.read_register(register['register'])
                except IOError as e:
                    print(e)
                if register['type'] == "scaled":
                    try:
                        y = value
                        B = instrument.read_register(register['offset'])
                        A = instrument.read_register(register['factor'])
                        value = (y + (B - 32768))/A
                    except IOError as e:
                        print(e)
                else:
                    value = x
                print("Value: {}".format(value))
            writestring += ("{}").format(value)
        writestring += "\n"
        print(writestring)
        datafilepath = todaypath + ("{}-{}-{}.csv").format(d.year,d.month,d.day)
        datafile = open(datafilepath, 'a')
        datafile.write(writestring)
        datafile.close()