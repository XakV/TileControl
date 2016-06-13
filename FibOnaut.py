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
    def __init__(self, ws_num, ws_rectangle, ws_winstack,  ws_tiled):
        self.ws_num = ws_num
        self.ws_rectangle = ws_rectangle
        self.ws_winstack = ws_winstack
        self.ws_tiled = ws_tiled
        
def get_environ():
    d_env = []
    with subprocess.Popen(['wmctrl', '-d'], stdout=subprocess.PIPE, universal_newlines=True) as wmctrld:
        desktop_scrape = wmctrld.stdout.read().splitlines()
        for line in desktop_scrape:
            deskline = line.split(' ')
            print(deskline)
            wks_num = deskline[0]
            if deskline[2] == '*':
                wksrctngl_focus = True
            else:
                wksrctngl_focus = False
            wks_ordinal = deskline[10]
            xpos_chr, ypos_chr = wks_ordinal.split(',')
            dimension = deskline[11]
            xdim_chr, ydim_chr = dimension.split('x')
            chr_dim = [xpos_chr,  ypos_chr,  xdim_chr,  ydim_chr]
            wks_xpos, wks_ypos, wks_xdim, wks_ydim = [ int(dim) for dim in chr_dim ]
            wks_name = deskline[13]
            wks_winstack = get_win_stack(wks_num)
            wks_rectangle = rectangle(wks_xpos,  wks_ypos,  wks_xdim,  wks_ydim,  wks_name,  wksrctngl_focus)
            enum_ws = workspace(wks_num,  wks_rectangle,  wks_winstack,  "Float")
            d_env.append(enum_ws)
    return d_env


def get_win_stack(ws_num):
    win_stack = []
    with subprocess.Popen(['wmctrl', '-l'], stdout=subprocess.PIPE, universal_newlines=True) as wmctrlg:
#TODO Refactor to deal with changing from wmctrl -lG to wmctrl -l
        ws_scrape = wmctrlg.stdout.read().splitlines()
        for line in ws_scrape:
            ws_line = line.split(' ')
            winid = ws_line[0]
            winws = ws_line[2]
            print(ws_num, winid,  winws)
            win = window(winid, winws)
            if win.win_ws == ws_num:
                win_stack.append(win)
    return win_stack


#screen is the root window found in get_environ
#returns the geometry of the first split and the remaining screen
'''declare all instances correctly'''
def calculate_split(screen):
    vsplit_pos = ((screen.xdim / 5 ) * 3 )
    hsplit_pos = ((screen.ydim / 5 ) * 3 )
    screen_remnt = rectangle  #right here and other places?
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
    for x in enumerate(desktop_init):
        print(x)
    for werkspace in enumerate(desktop_init):
        split_vpos, split_hpos, screen, split_rmnt = calculate_split(werkspace.ws_rectangle)
        for window in werkspace.winstack:
            new_geom = '0' + ',' + screen.xpos + ',' + screen.ypos + ',' + split_vpos + ',' + split_hpos
            move_rectangle(window.id, new_geom)
            werkspace.ws_rectangle = split_rmnt
        if werkspace.focus == True:
            wait_key()
    

init_FibTile()

