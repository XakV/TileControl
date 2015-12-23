#!/usr/env/python3

import subprocess
import tinydb

## define the window object, having an id, a desktop, a role, and x/y pos + size
## methods include moving, and resizing, may also include killing

class obwin(object):
    def __init__(self):
        self.hexid = ''
        self.dsktp = ''
        self.role = ''
        self.xpos = 0
        self.ypos = 0
        self.width = 0
        self.height = 0
        
    def move(self, hexid, nwxpos, nwypos):
        self.xpos = self.nwxpos
        self.ypos = self.nwypos
        
    def resize(self, hexid,  newidth, nwheight):
        self.width = newidth
        self.height = nwheight

## function to get active windows and assign a role
## see man wmctrl for info on wmctrl command
    
def buildwindb():
    roles = ['master',  'sub1', 'sub2',  'sub3',  'sub4']
    rolemark = 0
	oldesk = -1
    windodb = tinydb('/tmp/windodb.json')
    with subprocess.Popen(['wmctrl', '-lG'], stdout=subprocess.PIPE, universal_newlines=True) as wmctrlg:
        winout = wmctrlg.stdout.read().splitlines()
    for line in winout:
        winline = line.split(' ')
        hexid = winline[0]
        dsktp = winline[1]
        xpos = winline[2]
        ypos = winline[3]
        width = winline[4]
        height = winline[5]
        role = roles[rolemark]
		if dsktp == oldesk:
		    rolemark += 1
		else:
		    rolemark = 0
        windodb.insert({'hexid': hexid, 'desktop': dsktp, 'xposv': xpos, 'ypos': ypos, 'width': width, 'height': height, 'role': role})		
    return windodb

## Function to get screen dimensions and active desktop
## see man wmctrl for info on wmctrl command

def getscreen():
    with subprocess.Popen(['wmctrl', '-d'], stdout=subprocess.PIPE, universal_newlines=True) as wmctrld:
        wmctrlout = wmctrld.stdout.read().splitlines()
        for line in wmctrlout:
            if "*" in line:
                values = line.split(' ')
                deskid = values[0]
                print (deskid)
                screensize = values[11]
                curdeskxstr,curdeskystr = screensize.split('x')
                print(curdeskxstr,  curdeskystr)
    return int(deskid), int(curdeskxstr), int(curdeskystr)

def master_rl(windodb):
    
    getscreen()
    desktop = windodb.search()

    
#movecmdprefx = 'wmctrl -i -r'
#winmovarg = '-e'
	
