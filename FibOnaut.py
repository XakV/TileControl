#!/usr/env/python3

# FibOnaut uses the golden ratio to split and tile windows
# Layouts can be split to the right or left
# Windows can be pushed to or pop out of stack
# Stack order can be advanced or reversed
# Meant for use with a DE for killing and spawning new windows
# Combine with sxhkd key event daemon

import subprocess


#base class - a workspace or a window will inherit these attributes
#focus is a synonym for master and master window will always have focus
#master workspace will always be active

class rectangle:
    def __init__(self, xpos, ypos, xdim, ydim, name, focus):
        self.xpos = xpos
        self.ypos = ypos
        self.xdim = xdim
        self.ydim = ydim
        self.name = name
        self.focus = False

class window:
    def __init__(self, win_id, rectangle):
        self.win_id = win_id
        self.rectangle = rectangle
        

class workspace:
    def __init__(self, ws_num, rectangle, winstack):
        self.ws_num = ws_num
        self.ws_rectangle = rectangle
        self.ws_winstack = winstack
        self.ws_tiled = "Float"

#class winstack:
#  def __init__(self, window_dict{}):
#        self.window_dict =
# TODO - is a stack of windows a list, a dict, or a tuple?
# this object should be attached to a workspace as ws_winstack
# a window stack needs to be able to pop a window out of the stack and send it to another?

#TODO def tile():
#TODO - review gathering arguments, take one arg for float, one for tile, one for reverse_tile
#Will always operate on focused workspace
#defaults to stack_ord[0] is master and focused
#TODO - move this to after get_environ call

def get_environ():
    d_env = []
    with subprocess.Popen(['wmctrl', '-d'], stdout=subprocess.PIPE, universal_newlines=True) as wmctrld:
        desktop_scrape = wmctrld.stdout.read().splitlines()
        for line in desktop_scrape:
            deskline = line.split(' ')
            print(deskline)
            ws_num = deskline[0]
            if deskline[2] == '*':
                rectangle.focus = True
            else:
                rectangle.focus = False
            ws_ordinal = deskline[10]
            rectangle.xpos, rectangle.ypos = ws_ordinal.split(',')
            dimension = deskline[11]
            rectangle.xdim, rectangle.ydim = dimension.split('x')
            rectangle.name = deskline[13]
            d_env.append(workspace(ws_num, rectangle))
    return d_env


def get_ws_info():
    win_stack = []
    with subprocess.Popen(['wmctrl', '-l'], stdout=subprocess.PIPE, universal_newlines=True) as wmctrlg:
#TODO Refactor to deal with changing from wmctrl -lG to wmctrl -l
        ws_scrape = wmctrlg.stdout.read().splitlines()
        for line in ws_scrape:
            ws_line = line.split(' ')
            win_id, rectangle.name = ws_line[0]
            win_ws = ws_line[1]
            rectangle.xpos = ws_line[2]
            rectangle.ypos = ws_line[3]
            rectangle.xdim = ws_line[4]
            rectangle.ydim = ws_line[5]
            win_stack.append(window(win_id, win_ws, rectangle))       
    return win_stack

d_env = get_environ()
for x in d_env:
    print(x.ws_name)
win_stack = get_ws_info()
for y in win_stack:
    print(y.win_xdim)

