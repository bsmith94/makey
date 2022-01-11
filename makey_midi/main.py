#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# Midi controller
#

from tkinter import *

from playsound import playsound
import threading
import argparse
import configparser
import os
import pygame.midi

last_note = None
def onKey(event):
    global active_button
    global player
    global midi_ch
    global scale
    global base_note
    global modifier
    global note_name
    global last_note

    if event.keysym in buttons:
        if active_button:
            active_button['button'].configure(width=active_button['width'], height=active_button['height'])
        b = buttons[event.keysym]
        b['button'].configure(width=b['width']+1, height=b['height']+1)
        active_button = b
        n = base_note + scale[b['index']] + modifier
        silence()
        player.note_on(n, 127, midi_ch)
        last_note = n
        modifier = 0
        note_name.config(text = pygame.midi.midi_to_ansi_note(n))

def silence():
    global last_note
    global player
    global midi_ch

    if last_note:
        player.note_off(last_note, 127, midi_ch)
        last_note = None

def onSilence(event):
    silence()

def onModifyOctaveDown(event):
    global modifier
    modifier -= 12

def onModifyOctaveUp(event):
    global modifier
    modifier += 12

def onModifyFlat(event):
    global modifier
    modifier -= 1

def onModifySharp(event):
    global modifier
    modifier += 1

def onModifyOctave(event):
    global base_note
    base_note = int(event.keysym) * 12 + 12

def loadScale(idx):
    global scale
    global scales
    global scale_name
    scale = scales[idx]['notes']
    scale_name.config(text = scales[idx]['name'])
    
def onIonian(event):
    loadScale(0)

def onDorian(event):
    loadScale(1)

def onPhrygian(event):
    loadScale(2)

def onMixolydian(event):
    loadScale(3)

def onAeolian(event):
    loadScale(4)


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

def terminate():
    global root

    silence()
    pygame.midi.quit()
    root.destroy()

def init_midi(midi_ch, instrument):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.midi.init()
    output = pygame.midi.get_default_output_id()
    player = pygame.midi.Output(output)
    player.set_instrument(instrument, midi_ch)
    return player

script_home = os.path.dirname(os.path.realpath(__file__))
buttons = {}
active_button = None

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='{}/makey_midi.cfg'.format(script_home))
args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.config)
if not 'version' in config['DEFAULT']:
    raise ValueError('Could not read {}'.format(args.config))

midi_ch=0
player = init_midi(midi_ch, 0)
scales = [
    {
        'name' : 'Ionian',
        'notes' : (0, 2, 4, 7, 9)
    },
    {
        'name' : 'Dorian',
        'notes' : (0, 2, 5, 7, 10)
    },
    {
        'name' : 'Phrygian',
        'notes' : (0, 3, 5, 8, 10)
    },
    {
        'name' : 'Mixolydian',
        'notes' : (0, 2, 5, 7, 9)
    },
    {
        'name' : 'Aeolian',
        'notes' : (0, 3, 5, 7, 10)
    }
]


scale = scales[0]['notes']
base_note = 60
modifier = 0

root = Tk()
root.protocol('WM_DELETE_WINDOW', terminate)
a = Label(root, text="MIDI Controller")
a.pack()
p = PanedWindow(root)
p.pack()

index = 0
for bd in button_defs['buttons']:
    b = Button(p, text=bd['text'], bg=bd['color'], highlightbackground=bd['color'],
               height=button_defs['height'], width=button_defs['width'])
    buttons[bd['keysym']] = {
        'def' : bd,
        'button' : b,
        'width' : button_defs['width'],
        'height' : button_defs['height'],
        'index' : index
    }
    root.bind(bd['keybind'], onKey)
    b.pack(side=LEFT)
    index += 1

note_name = Label(root, text='  ')
note_name.pack()
scale_name = Label(root, text=scales[0]['name'])
scale_name.pack()


root.bind('a', onModifyOctaveDown)
root.bind('s', onModifyOctaveUp)
root.bind('z', onModifyFlat)
root.bind('x', onModifySharp)
for i in range(1,10):
    root.bind('{}'.format(i), onModifyOctave)
root.bind('y', onIonian)
root.bind('u', onDorian)
root.bind('i', onPhrygian)
root.bind('o', onMixolydian)
root.bind('p', onAeolian)
root.bind('q', onSilence)

root.geometry('400x400')
root.focus()
root.mainloop()
