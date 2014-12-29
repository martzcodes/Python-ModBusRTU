import os

filename = './modbus-should-be-running.txt'

if os.path.isfile(filename):
    os.remove(filename)

quit()
