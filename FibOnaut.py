#!/usr/env/python3

# FibOnaut uses the golden ratio to split and tile windows
# Layouts can be split to the right or left
# Windows can be pushed to or pop out of stack
# Stack order can be advanced or reversed
# Meant for use with a DE for killing and spawning new windows
# Combine with sxhkd key event daemon

import subprocess
import sys


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
    def __init__(self, win_id, win_ws):
        self.win_id = win_id
        self.win_ws = win_ws
        

class workspace():
    def __init__(self, ws_num, rectangle, winstack):
        self.ws_num = ws_num
        self.ws_rectangle = rectangle
        self.ws_winstack = winstack
        self.ws_tiled = "Float"
        
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
            ws_rectangle = rectangle
            xpos_chr, ypos_chr = ws_ordinal.split(',')
            dimension = deskline[11]
            xdim_chr, ydim_chr = dimension.split('x')
            chr_dim = [xpos_chr,  ypos_chr,  xdim_chr,  ydim_chr]
            ws_rectangle.xpos, ws_rectangle.ypos, ws_rectangle.xdim, ws_rectangle.ydim = [ int(dim) for dim in chr_dim ]
            ws_rectangle.name = deskline[13]
            win_stack = get_win_stack(ws_num)
            d_env.append(workspace(ws_num, ws_rectangle, win_stack))
    return d_env


def get_win_stack(ws_num):
    win_stack = []
    with subprocess.Popen(['wmctrl', '-l'], stdout=subprocess.PIPE, universal_newlines=True) as wmctrlg:
#TODO Refactor to deal with changing from wmctrl -lG to wmctrl -l
        ws_scrape = wmctrlg.stdout.read().splitlines()
        for line in ws_scrape:
            ws_line = line.split(' ')
            win_id = ws_line[0]
            win_ws = ws_line[1]
            if win_ws == ws_num:
                win_stack.append(window[win_id, win_ws])
    return win_stack


#screen is the root window found in get_environ
#returns the geometry of the first split and the remaining screen
def calculate_split(screen):
    vsplit_pos = ((screen.xdim / 5 ) * 3 )
    hsplit_pos = ((screen.ydim / 5 ) * 3 )
    screen_remnt = rectangle
    screen_remnt.xdim = screen.xdim - vsplit_pos
    screen_remnt.ydim = screen.ydim - hsplit_pos
    screen_remnt.xpos = vsplit_pos
    screen_remnt.ypos = hsplit_pos
    screen_remnt.name = screen.name + "sub"
    return vsplit_pos, hsplit_pos, screen, screen_remnt


#takes a window rectangle and a new geometry for the window
#returns stdout
def move_rectangle(win_id, new_geom):
    move_call_prefix = 'wmctrl -i -r'
    move_call_args = win_id + ' ' + new_geom
    with subprocess.Popen([move_call_prefix, move_call_args],  stdout=subprocess.PIPE) as win_move_call:
        mv_call_retval = win_move_call.std.read()
    return mv_call_retval


def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
    import termios
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    try:
        result = sys.stdin.read(1)
    except IOError:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    return result


'''My first use of recursion. I', sure this will be just fine!'''
'''I borrowed a wait algorithm from somewhere, what could go wrong?'''

def init_FibTile():
    desktop_init = get_environ()
    print(desktop_init)
    print(type(desktop_init))
    
    for werkspace in desktop_init:
        split_vpos, split_hpos, screen, split_rmnt = calculate_split(werkspace.ws_rectangle)
        for window in werkspace:
            new_geom = '0' + ',' + screen.xpos + ',' + screen.ypos + ',' + split_vpos + ',' + split_hpos
            move_rectangle(window.id, new_geom)
            workspace.ws_rectangle = split_rmnt
        if workspace.focus == True:
            wait_key()
    

init_FibTile()

