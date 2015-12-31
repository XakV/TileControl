#!/usr/env/python3

import subprocess
import tinydb
from tinydb.storages import MemoryStorage
import tkinter as tk

## who knows if this is working or not?

def keypress(event):
    if event.keysym == 'Escape':
        root.destroy()
    x = event.char
    if x == "Ctrl-Z":
        print('c z')
    elif x == "Ctrl-X":
        print('c x')
    else:
        pass

## function to get all active windows
## see man wmctrl for info on wmctrl command
    
def buildwindb():
    windodb = tinydb.TinyDB(storage=MemoryStorage)
    windodb.purge()
    with subprocess.Popen(['wmctrl -lG | tr -s " "'], shell = True, stdout=subprocess.PIPE, universal_newlines=True) as wmctrlg:
        winout = wmctrlg.stdout.read().splitlines()
    for line in winout:
        winline = line.split(' ')
        hexid = winline[0]
        dsktp = winline[1]
        xpos = winline[2]
        ypos = winline[3]
        width = winline[4]
        height = winline[5]
        windodb.insert({'hexid': hexid, 'desktop': dsktp, 'xpos': xpos, 'ypos': ypos, 'width': width, 'height': height})
        print(windodb.all())		
    return windodb

## Function to get screen dimensions and active desktop
## see man wmctrl for info on wmctrl command
## this is also working

def getscreen():
    with subprocess.Popen(['wmctrl', '-d'], stdout=subprocess.PIPE, universal_newlines=True) as wmctrld:
        wmctrlout = wmctrld.stdout.read().splitlines()
        for line in wmctrlout:
            if "*" in line:
                values = line.split(' ')
                deskid = values[0]
                print (deskid)
                screensize = values[11]
                screenx, screeny = screensize.split('x')
    return deskid, screenx, screeny

def move(winhxid,  sizstrng):

    subprocess.call('wmctrl',  '-i',  '-r',  winhxid, '-e',  sizstrng)

    
##this is being called and working
##returns int 

def tilemeasure(strngxdim,  strngydim,  strngpnlhght):

    screeny = int(strngydim)
    panelheight = int(strngpnlhght)
    screeny = (screeny - panelheight) - 30
    mastery = screeny + 10
    screenx = int(strngxdim)
    screenx = screenx - 30
    masterx = int(round(screenx / 5 * 3))
    subx = screenx - masterx
    suby = int(round(screeny / 5 * 3))
    return screeny,  mastery,  screenx,  masterx,  subx,  suby

    
root = tk.Tk()
root.bind_all('<Key>', keypress)
# don't show the tk window
root.withdraw()
root.mainloop()
while True:
    windodb = buildwindb()
    deskid,  screenx, screeny = getscreen()
    panelquery = tinydb.Query()
    panel = windodb.get(panelquery.desktop == '-1')
    panelheight = panel['height']
    mastery, screeny, screenx,  masterx,  subx,  suby = tilemeasure(screenx, screeny, panelheight)
    print(screeny,  mastery,  screenx,  masterx,  subx,  suby)
