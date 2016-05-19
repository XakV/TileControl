#!/usr/env/python3

# FibOnaut uses the golden ratio to split and tile windows
# Layouts can be split to the right or left
# Windows can be pushed to or pop out of stack
# Stack order can be advanced or reversed
# Meant for use with a DE for killing and spawning new windows
# Combine with sxhkd key event daemon

import subprocess

class workspace(object):
    def __init__(self, ws_num, ws_xpos, ws_ypos, ws_xdim, ws_ydim, ws_name, ws_active):
        self.ws_num = ws_num
        self.ws_xpos = ws_xpos
        self.ws_ypos = ws_ypos
        self.ws_xdim = ws_xdim
        self.ws_ydim = ws_ydim
        self.ws_name = ws_name
        self.ws_active = ws_active
#        self.ws_tiled = ws_tiled
#TODO if all this mess is working then we can create a variable and a function
#TODO for tiled state and master on left or master on right

class window(object):
    def __init__(self, win_id, win_ws, win_xpos, win_ypos, win_xdim, win_ydim, stack_ord):
        self.win_id = win_id
        self.win_ws = win_ws
        self.win_xpos = win_xpos
        self.win_ypos = win_ypos
        self.win_xdim = win_xdim
        self.win_ydim = win_ydim
        self.stack_ord = stack_ord

def get_environ():
    d_env = []
    ws_count = 0
    with subprocess.Popen(['wmctrl', '-d'], stdout=subprocess.PIPE, universal_newlines=True) as wmctrld:
        desktop_scrape = wmctrld.stdout.read().splitlines()
        for line in desktop_scrape:
            deskline = line.split(' ')
            ws_num = deskline[0]
            if deskline[2] == '*':
                ws_active = True
            else:
                ws_active = False
            if deskline[5] != 'N/A':
                ws_ordinal = deskline[8]
                ws_xpos, ws_ypos = ws_ordinal.split(',')
                dimension = deskline[9]
                ws_xdim, ws_ydim = dimension.split('x')
                ws_name = deskline[10]
                d_env[ws_count] = workspace(ws_num, ws_xpos, ws_ypos, ws_xdim, ws_ydim, ws_name, ws_active)
                ws_count += 1
            else:
                pass
        return d_env


def get_ws_info():
    win_stack = []
    with subprocess.Popen(['wmctrl', '-lG'], stdout=subprocess.PIPE, universal_newlines=True) as wmctrlg:
        ws_scrape = wmctrlg.stdout.read().splitlines()
        stack_ord = 0
        win_count = 0
        for line in ws_scrape:
            ws_line = line.split(' ')
            win_id = ws_line[0]
            win_ws = ws_line[1]
            win_xpos = ws_line[2]
            win_ypos = ws_line[3]
            win_xdim = ws_line[4]
            win_ydim = ws_line[5]            else:
                win_stack[win_count] = window(win_id, win_ws, win_xpos, win_ypos, win_xdim, win_ydim, stack_ord)
                win_count += 1

            if win_count >= 1:
                if win_stack[win_count - 1].win_ws == win_ws:            else:
                win_stack[win_count] = w            else:
                win_stack[win_count] = window(win_id, win_ws, win_xpos, win_ypos, win_xdim, win_ydim, stack_ord)
                win_count += 1
indow(win_id, win_ws, win_xpos, win_ypos, win_xdim, win_ydim, stack_ord)
                win_count += 1

                    stack_ord += 1
                    win_stack[win_count] = window(win_id, win_ws, win_xpos, win_ypos, win_xdim, win_ydim, stack_ord)
                    win_count += 1
                else:
                    stack_ord = 0
                    win_stack[win_count] = window(win_id, win_ws, win_xpos, win_ypos, win_xdim, win_ydim, stack_ord)
                    win_count += 1
            else:
                win_stack[win_count] = window(win_id, win_ws, win_xpos, win_ypos, win_xdim, win_ydim, stack_ord)
                win_count += 1
    return win_stack

get_environ()
for x in d_env:
    print(x)
get_ws_info()
for y in win_stack:
    print(y)

