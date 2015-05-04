"""
Continuously read the serial port and process IO data received from a remote XBee.
"""

import sys
import time
import EnttecUsbDmxProWidget
import serial

dmx = EnttecUsbDmxProWidget.EnttecUsbDmxProWidget()
dmx.setPort("/dev/ttyO2", 115200)
dmx.connect()
cerial = serial.Serial()
cerial.port = "/dev/ttyO4" #Change Value once we decide.
cerial.baudrate = 115200
cerial.open()
EmergencyStop = [127,127,0,127,127,0,0,0]

# Continuously read and print packets
while True:
    rx = dmx.getRecievedFrame() # we need channel
    ResponseList = rx['frame']
    print(ResponseList)
    dmx.sendDMX([1,2,3,4])
    try:
        #if gpiox == HIGH: #Change GPIO value soon.
        if True: # Because there's no e-stop right now
            if ResponseList != []:
                cerial.write(bytearray([0x7E] + ResponseList + [0xE7])) #Send messages to other microcontrollers
                       
        else:
            cerial.write(bytearray(EmergencyStop)) #Emergency Stop comes undone so turn off
    except KeyboardInterrupt:
        break
    time.sleep(0.01)
cerial.close