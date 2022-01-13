#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# Midi controller
#

import json
import os
from tkinter import *
import pygame.midi

def resolve_path(parent_dir, p):
    if not os.path.isabs(p):
        p = os.path.join(parent_dir, p)
    return p

class Skin:
    
    def __init__(self):
        self.resource_dir = None
        self.path = None
        self.height = None
        self.width = None
        self.background = None


    def get(self, data, key, required = True, def_val = None):
        r = def_val
        if key in data:
            r = data[key]
        elif required:
            raise ValueError('required value {} not specified'.format(key))
        return r


    def load(self, path):
        self.path = path
        self.resource_dir = os.path.dirname(os.path.realpath(path))
        with open(path) as f:
            d = json.load(f)
        root = self.get(d, 'root')
        self.title = self.get(root, 'title')
        self.height = self.get(root, 'height')
        self.width = self.get(root, 'width')
        self.background = resolve_path(self.resource_dir, self.get(root, 'background'))

    def loadImage(self, path, zoom = 0):
        i = PhotoImage(file = path)
        if zoom:
            i.zoom(zoom)
        return i

    def resolve(self):
        self.background_img = self.loadImage(self.background)


class MidiController:

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.midi.init()
        self.instrument_id = 0
        self.channel = 0
        self.output = pygame.midi.get_default_output_id()
        self.player = pygame.midi.Output(self.output)
        self.player.set_instrument(self.instrument_id, self.channel)
        self.note = None

    def silence(self):
        if self.note:
            self.player.note_off(self.note, 127, self.channel)

    def playNote(self, note):
        self.silence()
        self.note = note
        self.player.note_on(note, 127, self.channel)

    def terminate(self):
        self.silence()

class App:

    def __init__(self, skin):
        self.skin = skin
        self.midi = MidiController()

    def terminate(self):
        self.midi.terminate()
        self.root.destroy()

    def start(self):
        self.root = Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.terminate)
        self.build_ui()
        self.root.focus()
        self.root.mainloop()

    def buttonHit(self, event):
        self.midi.playNote(60)

    def build_ui(self):
        self.skin.resolve()
        self.root.title(self.skin.title)
        self.root.geometry('{}x{}'.format(self.skin.width, self.skin.height))
        self.background = Label(self.root, image = self.skin.background_img)
        self.background.pack()
        bi = PhotoImage(file = 'button.png')
        l = Label(self.root, width = 53, height = 53, bg='black', image=bi)
        l.photo = bi
        l.bind('<Button-1>', self.buttonHit)
        self.root.bind('<Up>', self.buttonHit)
        #l.grid(column=2,row=2)
        l.place(x=300,y=200)

        
    
if __name__ == '__main__':

    import argparse
    import configparser
    
    script_home = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='{}/makey_midi.cfg'.format(script_home))
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    if not 'version' in config['DEFAULT']:
        raise ValueError('Could not read {}'.format(args.config))

    cfg_dir = os.path.dirname(os.path.realpath(args.config))
    skin_path = resolve_path(cfg_dir, config['DEFAULT']['skin'])

    skin = Skin()
    skin.load(skin_path)
    
    app = App(skin)
    app.start()

