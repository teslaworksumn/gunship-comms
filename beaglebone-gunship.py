"""
Continuously read the serial port and process IO data received from a remote XBee.
"""

import sys
import time
import array
import traceback
import struct
import EnttecUsbDmxProWidget
import serial

if sys.version_info > (3,0):
    py2 = False
else:
    py2 = True

dmx = EnttecUsbDmxProWidget.EnttecUsbDmxProWidget()
dmx.setPort("/dev/ttyO2", 115200)
dmx.connect()

debug = {'SerialBuffer':False, 'RXWarning':False}
cerial = serial.Serial()
cerial.port = "/dev/ttyUSB0" #Change Value once we decide.
cerial.baudrate = 115200
cerial.open()
emergencyStop = "x 127 127 0 127 127 0 0 0 0 0\r\n"
rx = ()
iterv = 0

# Continuously read and print packets
while True:
    rx = dmx.getRecievedFrame() # we need channel
    ResponseList = rx['frame']
    print(ResponseList)
    stop = False;
    try:
        serialbuffer = []
        rx = b''
        datasend = ""
        if not stop: # Because there's no e-stop right now
            if ResponseList != []:
                datasend = "x {0} {1} {2} {3} {4} {5} {6} {7} {8}\r\n".format(ResponseList[0], ResponseList[1], ResponseList[2], ResponseList[3], ResponseList[4], ResponseList[5], ResponseList[6], ResponseList[7], ResponseList[8])
        else:
            datasend = emergencyStop #Emergency Stop comes undone so turn off
        cerial.write(datasend.encode()) #Send messages to other microcontrollers
        #print(datasend)
        '''
        try:
            if cerial.inWaiting() > 0:
                rx += cerial.read(cerial.inWaiting()) # Read the buffer into a variable
                for i in rx: # Convert the byte string into something a little more useful
                    if py2:
                        i =struct.unpack('B',i)[0]
                    serialbuffer += [i]
            rx = b''
            si = 0
            for i in serialbuffer: # Find the start byte
                if i != 120:
                    si += 1
                else:
                    break
            if si > 0: # Remove anything before the start byte
                if debug['RXWarning']:
                    if debug['SerialBuffer']:
                        print("IVD:",serialbuffer)
                    sys.stderr.write('RX_WARNING: Removing invalid data from buffer\n')
                serialbuffer = serialbuffer[si:-1]
        except:
            e = sys.exc_info()
            sys.stderr.write('RX_FAIL: {0}: {1}\n'.format(e[0],e[1]))
            traceback.print_tb(e[2])
            sys.stderr.write('Data in queue: {0}\n'.format(serialbuffer))
            '''
        #print(str(array.array('B',serialbuffer).tostring()))
        #dmx.sendDMX()
        dmx.clearBuffer()
        time.sleep(0.001)
    except KeyboardInterrupt:
        break
dmx.close()
cerial.close()