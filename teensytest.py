import serial
import sys
import struct
import time

debug = {'SerialBuffer':False, 'RXWarning':True}

if sys.version_info > (3,0):
    py2 = False
else:
    py2 = True

port = serial.Serial()
port.port = sys.argv[1]
port.baudrate = 115200
port.open()

out = 0;

while True:
    try:
        serialbuffer = []
        rx = b''
        ss = "x {0} 1 {1} 3 4 5 6 7".format(out,255-out)
        port.write(ss.encode())
        print(ss)
        out = (out+1)%256
        try:
            if port.inWaiting() > 0:
                rx += port.read(port.inWaiting()) # Read the buffer into a variable
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
            serialbuffer = serialbuffer[0:20]
        except:
            e = sys.exc_info()
            sys.stderr.write('RX_FAIL: {0}: {1}\n'.format(e[0],e[1]))
            traceback.print_tb(e[2])
            sys.stderr.write('Data in queue: {0}\n'.format(serialbuffer))
        print(serialbuffer)
        time.sleep(0.05)
    except (KeyboardInterrupt,SystemExit):
        break;

port.close()
