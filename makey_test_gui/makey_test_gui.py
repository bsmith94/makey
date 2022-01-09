#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# Demonstration of using Makey Makey HID to control a GUI.
# Events come in as keypresses.
#

from tkinter import *
from playsound import playsound
import threading
import argparse
import configparser
import os


def onKeyPress(event):
    global active_button
    global sound_queue
    global sound_cv
    if event.keysym in buttons:
        if active_button:
            active_button['button'].configure(width=active_button['width'], height=active_button['height'])
        b = buttons[event.keysym]
        b['button'].configure(width=b['width']+1, height=b['height']+1)
        if b['sound']:
            with sound_cv:
                sound_queue.append(b['sound'])
                sound_cv.notify()
        active_button = b        


button_defs = {
    'width' : 4,
    'height' : 4,
    'buttons' : [
        {
            'color' : 'green',
            'text'  : 'P',
            'keybind' : '<Left>',
            'keysym' : 'Left',
        },
        {
            'color' : 'yellow',
            'text'  : 'R',
            'keybind' : '<Up>',
            'keysym' : 'Up',
        },
        {
            'color' : 'cyan',
            'text'  : 'M',
            'keybind' : '<Right>',
            'keysym' : 'Right',
        },
        {
            'color' : 'orange',
            'text'  : 'I',
            'keybind' : '<Down>',
            'keysym' : 'Down',
        },
        {
            'color' : 'red',
            'text'  : 'I2',
            'keybind' : '<space>',
            'keysym' : 'space',
        },
    ]    
}

def sound_thread(name):
    global quit_sound
    global sound_queue
    global sound_cv

    done = False
    while not done:
        s = None
        with sound_cv:
            while not len(sound_queue) > 0 and not quit_sound:
                sound_cv.wait()
            if quit_sound:
                done = True
                break                
            s = sound_queue.pop(0)
        if s :
            playsound(s, block=False)

def terminate():
    global quit_sound
    global sound_queue
    global sound_cv

    with sound_cv:
        quit_sound = True
        sound_cv.notify()
    root.destroy()

script_home = os.path.dirname(os.path.realpath(__file__))
quit_sound = False
sound_queue = []
sound_cv = threading.Condition()
buttons = {}
active_button = None
sounds = None

parser = argparse.ArgumentParser()
parser.add_argument('--sounds')
parser.add_argument('--config', default='{}/makey_test_gui.cfg'.format(script_home))
args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.config)
if not 'version' in config['DEFAULT']:
    raise ValueError('Could not read {}'.format(args.config))

if args.sounds:
    sounds = config[args.sounds]

root = Tk()
st = threading.Thread(target=sound_thread, args=('sound',))
st.start()

root.protocol('WM_DELETE_WINDOW', terminate)
a = Label(root, text="Makey Makey Demo")
a.pack()
p = PanedWindow(root)
p.pack()

for bd in button_defs['buttons']:
    b = Button(p, text=bd['text'], bg=bd['color'], highlightbackground=bd['color'],
               height=button_defs['height'], width=button_defs['width'])
    sound = None
    if sounds and bd['text'] in sounds:
        sound = '{}/../media/sounds/{}'.format(script_home, sounds[bd['text']])
    buttons[bd['keysym']] = {
        'def' : bd,
        'button' : b,
        'width' : button_defs['width'],
        'height' : button_defs['height'],
        'sound' : sound
    }
    root.bind(bd['keybind'], onKeyPress)
    b.pack(side=LEFT)
root.geometry('400x400')
root.focus()
root.mainloop()
