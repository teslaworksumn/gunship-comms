"""
Continuously read the serial port and process IO data received from a remote XBee.
"""

import sys
import time
import EnttecUsbDmxProWidget
import serial

dmx = EnttecUsbDmxProWidget.EnttecUsbDmxProWidget()
dmx.setPort("/dev/ttyUSB0", 115200)
dmx.connect()
cerial = serial.Serial()
cerial.port = "/dev/ttyO4" #Change Value once we decide.
cerial.baudrate = 115200
cerial.open()
emergencyStop = "x 127 127 0 127 127 0 0 0 0 0"

# Continuously read and print packets
while True:
    rx = dmx.getRecievedFrame() # we need channel
    ResponseList = rx['frame']
    print(ResponseList)
    dmx.sendDMX([1,2,3,4])
    try:
        #if gpiox == HIGH: #Change GPIO value soon.
        if True: # Because there's no e-stop right now
            bbStr = "x {0} {1} {2} {3} {4} {5} {6} {7} {8}".format(ResponseList[0], ResponseList[1] ResponseList[2], ResponseList[3], ResponseList[4], ResponseList[5], ResponseList[6], ResponseList[7])
            if ResponseList != []:
                cerial.write(bbStr+"\r\n".encode()) #Send messages to other microcontrollers
                print bbStr      
        else:
            cerial.write(emergencyStop+"\r\n".encode()) #Emergency Stop comes undone so turn off
    except KeyboardInterrupt:
        break
    time.sleep(0.01)
cerial.close