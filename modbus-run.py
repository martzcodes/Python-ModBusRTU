import minimalmodbus as minmod
import serial
import os
import json
import datetime

# check for modbus.json

basepath = 'c:/ModBusData'

if not os.path.isfile(basepath+'/modbus.json'):
	print('No modbus.json found, please create one')
	quit()

if os.path.isfile(basepath + '/modbus-should-be-running.txt'):
        mods = json.load(open(basepath + '/modbus.json'))

        d = datetime.datetime.now()

        datapath = basepath + '/modbus-data/'

        if not os.path.isdir(datapath):
                os.mkdir(datapath)

        monthpath = datapath + ('{}-{}/').format(d.year,d.month)

        if not os.path.isdir(monthpath):
                os.mkdir(monthpath)

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

                        writestring = ("{},{},{},{},{}").format(d.day,d.hour,d.minute,d.hour*60*60+d.minute*60+d.second,channel['channel'])
                        headerstring = "day,hour,min,time,channel,name,"
                        unitstring = "day of month,hour,minute,seconds from midnight,#,,"
                        try:
                                writestring+= (",{}").format(instrument.read_string(103))
                        except ValueError as e:
                                print(e)
                        for register in mod['registers']:
                                headerstring += ("{},").format(register['name'])
                                unitstring += ("{},").format(register['units'])
                                writestring += ","
                                value = "NA"
                                if register['only'] == "" or register['only'] == channel['type']:
                                        if register['float'] != "NA":
                                                try:
                                                        #value = instrument.read_float(register['float'])
                                                        values = instrument.read_registers(register['float'],numberOfRegisters=2)
                                                        registerstring = chr(values[1].to_bytes(2,byteorder='big')[0]) + chr(values[1].to_bytes(2,byteorder='big')[1]) + chr(values[0].to_bytes(2,byteorder='big')[0]) + chr(values[1].to_bytes(2,byteorder='big')[1])
                                                        value = minmod._bytestringToFloat(registerstring)*register['convert']
                                                except ValueError as e:
                                                        print(e)

                                        print("Value: {}".format(value))

                                writestring += ("{}").format(value)

                        headerstring += "\n"
                        unitstring += "\n"
                        writestring += "\n"
                        print(writestring)
                        if d.hour < mod['savetime']:
                                datafilepath = monthpath + ("{}-{}-{}+{}hr.csv").format(d.year,d.month,d.day-1,mod['savetime'])
                        else:
                                datafilepath = monthpath + ("{}-{}-{}+{}hr.csv").format(d.year,d.month,d.day,mod['savetime'])
                        if not os.path.isfile(datafilepath):
                                print('No datafile, making one and adding header')
                                datafile = open(datafilepath, 'w+')
                                datafile.write(headerstring)
                                datafile.write(unitstring)
                                datafile.close()
        
                        datafile = open(datafilepath, 'a')
                        datafile.write(writestring)
                        datafile.close()
else:
        print("Start file is not there...")
        quit()
