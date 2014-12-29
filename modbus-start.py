import os

startfile = open('./modbus-should-be-running.txt','w')
startfile.write("created by modbus-start.py")
startfile.close()

print("Start file created, modbus can run now")

quit()
