import os
import json

print("Welcome Message")

data = {}
comport = input("What Com Port is the RS485 USB Converter Located at (format example: COM5)")
data['comport'] = comport
baudrate = input("What is the baud rate set at? (example: 9600)")
data['baudrate'] = int(baudrate)
bytesize = input("What is the byte size? (example: 8)")
data['bytesize'] = int(bytesize)
stopbits = input("What is the stopbit? (example: 1)")
data['stopbits'] = int(stopbits)
timeout = input("What is the timeout? (example: 0.5)")
data['timeout'] = float(timeout)
parity = input("What is the parity? (Single Letter: O for odd, E for even, N for none)")
data['parity'] = parity

numchannels = input("How many channels are there? (example: 2)")

channels = []
for x in range(0,int(numchannels)):
    channel = {}
    channel['channel'] = int(input(("{} - Address:").format(x)))
    channel['type'] = input(("{} - Type (supply or return):").format(x))
    channels.append(channel)

data['channels'] = channels

registerstring = '[{"name":"Mass Flow Rate","register":1,"type":"float","offset":18,"factor":28,"float":246,"only":"","units":"GPH"},'
registerstring += '{"name":"Density","register":2,"type":"float","offset":19,"factor":29,"float":248,"only":"","units":"kg/m3"},'
registerstring += '{"name":"Temperature","register":3,"type":"float","offset":21,"factor":31,"float":250,"only":"","units":"F"},'
registerstring += '{"name":"Volume Flow Rate","register":4,"type":"float","offset":22,"factor":32,"float":252,"only":"","units":"LPH"},'
registerstring += '{"name":"Mass Total","register":7,"type":"float","offset":24,"factor":34,"float":258,"only":"","units":"GAL"},'
registerstring += '{"name":"Volume Total","register":8,"type":"float","offset":25,"factor":35,"float":260,"only":"","units":"L"},'
registerstring += '{"name":"Mass Inventory","register":9,"type":"float","offset":26,"factor":36,"float":262,"only":"","units":"GAL"},'
registerstring += '{"name":"Volume Inventory","register":10,"type":"float","offset":27,"factor":37,"float":264,"only":"","units":"GAL"}'
registerstring += '{"name":"Differential Mass Flow","register":9,"type":"float","offset":26,"factor":36,"float":4437,"only":"return","units":"GAL"},'
registerstring += '{"name":"Differential Mass Total","register":10,"type":"float","offset":27,"factor":37,"float":4439,"only":"return","units":"GAL"}'
registerstring += ']'

data['registers'] = json.loads(registerstring)

print("NOTE: For the next command, if the file exists, it will be overwritten")
filename = input("Please enter a filename for the config file: (example: modbus)")

mods = []
mods.append(data)

with open('./'+filename+'.json','w') as outfile:
    json.dump(mods, outfile, sort_keys=True, indent = 4, separators=(',',': '))
