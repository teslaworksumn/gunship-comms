import pygame
pygame.init()
print '%s joystick(s) found.' % pygame.joystick.get_count()
j = pygame.joystick.Joystick(0)
j.init()
print 'Initialized joystick: %s' % j.get_name()
import serial
from xbee import XBee,ZigBee
import json
jse = json.JSONEncoder()

serial_port= serial.Serial()
serial_port.port = "COM7"
serial_port.baudrate = 9600
if serial_port.isOpen():
    disconnect()
serial_port.open()
print "Serial port opened on {0} at {1} baud".format(serial_port.port,serial_port.baudrate)

def get():
    out = [0] * (j.get_numaxes() + j.get_numbuttons())
    it = 0  # iterator
    pygame.event.pump()

    # Read input from the axes
    for i in range(0, j.get_numaxes()):
        out[it] = j.get_axis(i)
        it += 1
    # Read input from the buttons
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it += 1
    return out


def test():
    last_vals = get()
    while True:
        curr_vals = get()
        for index, val in enumerate(curr_vals):
            if last_vals[index] != val:
                d2s = [index, val]
                
                print d2s
                serial_port.write(bytearray(jse.encode(d2s)+'\r\l'))
        last_vals = curr_vals
        

if __name__ == '__main__':
    test()
