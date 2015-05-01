"""
Continuously read the serial port and process IO data received from a remote XBee.
"""

import sys
import time
import Adafruit_BBIO.PWM as PWM
import EnttecUsbDmxProWidget

dmx = EnttecUsbDmxProWidget.EnttecUsbDmxProWidget()
dmx.setPort("/dev/ttyO2", 115200)
dmx.connect()

# Continuously read and print packets
while True:
    rx = dmx.getRecievedFrame()
    ResponseArray = rx['frame']
    print(ResponseArray)
    try:
        if ResponseArray != []:            
            if ((ResponseArray[0] == 1) and ((ResponseArray[1] < .15) and (ResponseArray[1] > -.15))): #Brake
                PWM.set_duty_cycle("P9_14", 25.5) #Input A CHANGE ONCE JACK/RYAN GET HERE
                PWM.set_frequency("P9_14", 10) #Frequency A
                PWM.set_duty_cycle("P9_15", 25.5) #Input B
                PWM.set_frequency("P9_15", 10) #Frequency B
                sleep(.02)
                PWM.stop("P9_14") #stops for a second
                PWM.stop("P9_15") #stops for a second

            if ((ResponseArray[0] == 1) and (ResponseArray[1] >= .25)): #Reverse
                #PWM.set_duty_cycle("P9_14", 25.5) Input A STAY COMMENTED OUT
                #PWM.set_frequency("P9_14", 10) STAY COMMENTED OUT
                PWM.set_duty_cycle("P9_15", 25.5) #Input B
                PWM.set_frequency("P9_15", 10)
                sleep(.02)
                PWM.stop("P9_14") #stops for a second
                PWM.stop("P9_15") #stops for a second

            if ((ResponseArray[0] == 1) and (ResponseArray[1] <= -.25)): #Forward
                PWM.set_duty_cycle("P9_14", 25.5) #Input A 
                PWM.set_frequency("P9_14", 10) 
                #PWM.set_duty_cycle("P9_15", 25.5) Input B. Stay commented out.
                #PWM.set_frequency("P9_15", 10) Stay commented out.
                sleep(.02)
                PWM.stop("P9_14") #stops for a second
                PWM.stop("P9_15") #stops for a second
            if ((ResponseArray[0] == 1) and ((ResponseArray[1] < .15) and (ResponseArray[1] > -.15))): #Brake
                PWM.set_duty_cycle("P9_16", 25.5) #Input A CHANGE ONCE JACK/RYAN GET HERE
                PWM.set_frequency("P9_16", 10) #Frequency A
                PWM.set_duty_cycle("P9_17", 25.5) #Input B
                PWM.set_frequency("P9_17", 10) #Frequency B
                sleep(.02)
                PWM.stop("P9_16") #stops for a second
                PWM.stop("P9_17") #stops for a second

            if ((ResponseArray[0] == 1) and (ResponseArray[1] >= .25)): #Reverse
                #PWM.set_duty_cycle("P9_14", 25.5) Input A STAY COMMENTED OUT
                #PWM.set_frequency("P9_14", 10) STAY COMMENTED OUT
                PWM.set_duty_cycle("P9_17", 25.5) #Input B
                PWM.set_frequency("P9_17", 10)
                sleep(.02)
                PWM.stop("P9_16") #stops for a second
                PWM.stop("P9_17") #stops for a second

            if ((ResponseArray[0] == 1) and (ResponseArray[1] <= -.25)): #Forward
                PWM.set_duty_cycle("P9_16", 25.5) #Input A 
                PWM.set_frequency("P9_16", 10) 
                #PWM.set_duty_cycle("P9_15", 25.5) Input B. Stay commented out.
                #PWM.set_frequency("P9_15", 10) Stay commented out.
                sleep(.02)
                PWM.stop("P9_16") #stops for a second
                PWM.stop("P9_17") #stops for a second
    except KeyboardInterrupt:
        break
    time.sleep(0.01)
