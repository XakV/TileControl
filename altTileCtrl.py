#!/usr/env/python3

from subprocess import *
from collections import *

class windo:

    def __init__(self, windata):
        self.windata = {}
        
    def getwindata():
        with Popen(['wmctrl -lG | tr -s " "'], shell = True, stdout=PIPE, universal_newlines=True) as wmctrlg:
            winout = wmctrlg.stdout.read().splitlines()
        wincontainer = []
        for line in winout:
            winline = line.split(' ')
            windict = {}
            windict['hexid'] = winline[0]
            windict['desktop'] = winline[1]
            windim = {}
            windim['xpos'] = winline[2]
            windim['ypos'] = winline[3]
            windim['width'] = winline[4]
            windim['height'] = winline[5]
            windict['dimensions'] = windim
            wincontainer.append(windict)
        return wincontainer
        
    def movewin(windata,  newsizestrng):
        winhxid = windata['hexid']
        subprocess.call('wmctrl',  '-i',  '-r',  winhxid, '-e',  newsizstrng)
        
    def sortwindos(screendictlist, shift):
        listlen = len(screendictlist)
        movedwinlist = []
        
    
def get_active_screen():
    
    with Popen(['wmctrl', '-d'], stdout=PIPE, universal_newlines=True) as wmctrld:
        wmctrlout = wmctrld.stdout.read().splitlines()
        for line in wmctrlout:
            if "*" in line:
                values = line.split(' ')
                deskid = values[0]
                screensize = values[11]
                try:
                    screenx, screeny = screensize.split('x')
                    return deskid, screenx, screeny
                except:
                    print('Not Running and EWMH compliant Window Manager')
                    continue
    

AllScreenDictList = windo.getwindata()
ActiveDeskNum,  ScreenXDim,  ScreenYDim = get_active_screen()
for windo in AllScreenDictList:
    if windo['desktop'] == ActiveDeskNum:
        print(windo['hexid'])

    
