import sys
import os
import time
import pygame
sys.path.append("../EnttecUsbDmxPro/")
import EnttecUsbDmxPro
pygame.init()
print '%s joystick(s) found.' % pygame.joystick.get_count()
j = []
for i in range(0,pygame.joystick.get_count()):
    j += [pygame.joystick.Joystick(i)]
    j[i].init()
    print 'Initialized joystick: %s' % j[i].get_name()

dmx = EnttecUsbDmxPro.EnttecUsbDmxPro()
dmx.setPort(sys.argv[1], 115200)
dmx.connect()

def get():
    joy = []
    pygame.event.pump()
    for i in range(0,len(j)):
        # Read input from the axes
        joy += [{"axis":[],"button":[],'hat':[],'ball':[]}]
        for i2 in range(0, j[i].get_numaxes()):
            joy[i]['axis'] += [j[i].get_axis(i2)]
        # Read input from the buttons
        for i2 in range(0, j[i].get_numbuttons()):
            joy[i]['button'] += [j[i].get_button(i2)]
        # Read input from the hats
        for i2 in range(0, j[i].get_numhats()):
            joy[i]['hat'] += [j[i].get_hat(i2)]
        # Read inputs from trackballs
        for i2 in range(0, j[i].get_numballs()):
            joy[i]['ball'] += [j[i].get_ball(i2)]
    return joy

def send(d2s):
    tx = []
    for i in d2s:
        if i > 255:
            i=255
        elif i < 0:
            i=0
        tx += [int(i)]
    dmx.sendDMX(tx)

def run():
    while True:
        joy = get()
        frame = dmx.getRecievedFrame()['frame']
        thrust = int((-joy[0]['axis'][1]+1)*127.5)
        rudder = 255-int((-joy[0]['axis'][0]+1)*127.5)
        lift   = int((-joy[0]['axis'][3]+1)*127.5)
        turret_d = joy[0]['hat'][0]
        turret_v = int((joy[0]['axis'][6]+1)*64)
        turret = [turret_d[0]*turret_v+127, turret_d[1]*turret_v+127, 0]
        turret_safety = [0,0,0]
        if joy[0]['button'][5]:
            turret_safety[0] = 37
        if joy[0]['button'][14]:
            turret_safety[1] = 97
        if joy[0]['button'][1]:
            turret_safety[2] = 123
        if joy[0]['button'][23]:
            turret[2] = 19
        if joy[0]['button'][24]:
            turret[2] = 43
        if joy[0]['button'][25]:
            turret[2] = 59
        if joy[0]['button'][30]:
            turret[2] = 79
        print joy[0]['button']
        print "Thrust: {0}, Rudder: {1}, Lift: {2}".format(thrust,rudder,lift)
        print "Turret theta: {0}, phi: {1}, safety: {2}, active {3}".format(turret[0],turret[1],turret_safety,turret[2])
        if frame != []:
            if frame[0] > 0:
                print "WARNING: LOW BATTERY!!!!!"
        tx = [thrust,rudder,lift,turret[0],turret[1]] + turret_safety + [turret[2]]
        send(tx)
        time.sleep(0.01)

if __name__ == '__main__':
    run()

