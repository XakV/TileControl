#!/usr/env/python3

import subprocess

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

## Represents the placement of windows on the screen.

class layout(object):
    def __init__(self):
        self.numbrwndows = 0
        self.layout =''
        self.reversed = 'False'
        self.floating = 'False'
        
    def masterRL(self, winmatrix[]):
        for window in winmatrix[]:
            if winmatrix[window].role == 'master'
                obwin.move(winmatrix[window].hexid, 20, 20)
                obwin.resize(winmatrix[window].hexid, 1000, 920)
            if winmatrix[window].role == 'sub1'
                obwin.move(winmatrix[window].hexid, 1040, 20)
                obwin.resize(winmatrix[window].hexid, 860, 480)
            if winmatrix[window].role == 'sub2'
                obwin.move(winmatrix[window].hexid, 1040, 500)
                obwin.resize(winmatrix[window].hexid, 860, 400)
    
    def masterLR(self, winmatrix[]):
        for window in winmatrix[]:
            if winmatrix[window].role == 'master'
                obwin.move(winmatrix[window].hexid, 900, 20)
                obwin.resize(winmatrix[window].hexid, 1000, 920)
            if winmatrix[window].role == 'sub1'
                obwin.move(winmatrix[window].hexid, 20, 20)
                obwin.resize(winmatrix[window].hexid, 860, 480)
            if winmatrix[window].role == 'sub2'
                obwin.move(winmatrix[window].hexid, 20, 500)
                obwin.resize(winmatrix[window].hexid, 860, 400)

## function to get active windows and assign a role
## see man wmctrl for info on wmctrl command
    
def get ():
    roles = ['master',  'sub1', 'sub2',  'sub3',  'floatfull',  'floatbar']
    rolemark = 0
    winmatrix = []
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
        rolemark += 1
        winmatrix.append(obwin(hexid, dsktp, xpos, ypos, width, height, role))
    return winmatrix

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
    
