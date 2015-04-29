"""
Continuously read the serial port and process IO data received from a remote XBee.
"""

from xbee import XBee
import sys
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

xbee = XBee(ser)

# Continuously read and print packets
while True:
    try:
        response = ser.wait_read_frame()
        print response # Replace once we get Communication
    except KeyboardInterrupt:
        break
ser.close()
