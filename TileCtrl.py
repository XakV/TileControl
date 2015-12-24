#!/usr/env/python3

import subprocess
import Tinydb
import Tkinter as tk

def keypress(event):
    if event.keysym == 'Escape':
        root.destroy()
    x = event.char
    if x == "Ctrl-Z":
        execmastr1()
    elif x == "Ctrl-X":
        execmastr2()
    else:
        pass


## function to get active windows and assign a role
## see man wmctrl for info on wmctrl command
    
def buildwindb():
    roles = ['master',  'sub1', 'sub2',  'sub3',  'sub4']
    rolemark = 0
    oldesk = -1
    windodb = Tinydb('/tmp/windodb.json')
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
                screenx, screeny = screensize.split('x')
    return deskid, screenx, screeny

def move(winhxid,  sizstrng):

    subprocess.call('wmctrl',  '-i',  '-r',  winhxid, '-e',  sizstrng)

def mastr1(screenx,  mastery,  masterx,  subx,  suby):
    
    mstr = '0,10,10,'+masterx+','+mastery
    sub = '0,'+(masterx + 10)+',10,'+subx+','+mastery
    
    return mstr,  sub

def mastr2(screenx,  mastery,  masterx,  subx,  suby):
    
    mstr = '0,10,10,'+masterx+','+mastery
    sub1 = '0,'+(masterx + 10)+',10,'+subx+','+suby
    sub2 = '0,'+(masterx + 10)+',10,'+subx+','+(mastery - suby) 
    
    return mstr,  sub1,  sub2
    
def tilemeasure(screenx,  screeny,  pnlhght):

    screeny = (screeny - panelheight) - 30
    mastery = screeny + 10
    screenx = screenx - 30  
    masterx = screenx / 5 * 3
    subx = screenx - masterx
    suby = screeny / 5 * 3
    return screeny,  mastery,  screenx,  masterx,  subx,  suby


def execmastr1(deskid, windodb):
    
    screenqry = windodb.Query()
    mstr = screenqry.search((windodb.dsktp == deskid) & (windodb.role == 'master'))
    sub1 = screenqry.search((windodb.dsktp == deskid) & (windodb.role == 'sub1'))
    mstrs = mastr1(screenx,  mastery,  masterx,  subx,  suby).mstr
    subs = mastr1(screenx,  mastery,  masterx,  subx,  suby).sub
    move(mstr.hexid, mstrs)
    move(sub1.hexid, subs)
    
def execmastr2(deskid):
    
    screenqry = tinydb.Query()
    mstr = windodb.search((dsktp == deskid) & (role == 'master'))
    sub1 = windodb.search((dsktp == deskid) & (role == 'sub1'))
    sub2 = windodb.search((dsktp == deskid) & (role == 'sub2'))
    mstrs = mastr2(screenx,  mastery,  masterx,  subx,  suby).mstr
    sub1s = mastr2(screenx,  mastery,  masterx,  subx,  suby).sub1
    sub2s = mastr2(screenx,  mastery,  masterx,  subx,  suby).sub2
    move(mstr.hexid, mstrs)
    move(sub1.hexid, sub1s)
    move(sub2.hexid,  sub2s)
    

windodb = buildwindb()
while True:
    deskid,  screenx, screeny = getscreen()
    panelquery = Tinydb.Query()
    panel = panelquery.desktop.search((windodb.dsktp == -1))
    panelheight = panel.height
    tilemeasure(screenx, screeny, panelheight)
    root = tk.Tk()
    root.bind_all('<Key>', keypress)
    # don't show the tk window
    root.withdraw()
    root.mainloop()
    
