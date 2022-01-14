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

class ButtonDef:

    def __init__(self, width, height, x, y, image_path, key):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.image_path = image_path
        self.key = key
        self.image = None
        self.index = None

class Skin:
    
    def __init__(self):
        self.resource_dir = None
        self.path = None
        self.height = None
        self.width = None
        self.background = None
        self.pads = []

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
        self.loadRoot(d)
        self.loadPads(d)

    def loadRoot(self, data):
        root = self.get(data, 'root')
        self.title = self.get(root, 'title')
        self.height = self.get(root, 'height')
        self.width = self.get(root, 'width')
        self.background = resolve_path(self.resource_dir, self.get(root, 'background'))

    def loadPads(self, data):
        pads = self.get(self.get(data, 'buttons'), 'pads')
        instances = self.get(pads, 'instances')
        idx = 0
        for p in instances:
            d = ButtonDef(pads['width'], pads['height'],
                                       p['x'], p['y'],
                                       pads['image'], p['key'])
            d.index = idx
            idx += 1
            self.pads.append(d)
            
    def loadImage(self, path, zoom = 0):
        i = PhotoImage(file = path)
        if zoom:
            i.zoom(zoom)
        return i

    def resolve(self):
        self.background_img = self.loadImage(self.background)
        for p in self.pads:
            p.image = self.loadImage(resolve_path(self.resource_dir, p.image_path))

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

class View:

    def __init__(self, skin):
        self.skin = skin
        self.root = None
        self.pads = []


    def build(self):
        self.root = Tk()
        self.buildUi()

    def start(self):
        self.root.focus()
        self.root.mainloop()

    def destroy(self):
        self.root.destroy()

    def buildRoot(self):
        self.root.title(self.skin.title)
        self.root.geometry('{}x{}'.format(self.skin.width, self.skin.height))
        self.background = Label(self.root, image = self.skin.background_img)
        self.background.pack()

    def buildPads(self):
        for p in self.skin.pads:
            l = Label(self.root, width = p.width, height = p.height,
                       bg='black', image=p.image)
            self.pads.append(l)
            l.photo = p.image
            l.defn = p
            l.place(x=p.x, y=p.y)
        
    def buildUi(self):
        # skin.resolve() must be invoked after Tk is created
        self.skin.resolve()
        self.buildRoot()
        self.buildPads()

class UiController:

    def __init__(self, app, view, model):
        self.app = app
        self.view = view
        self.model = model
        self.key_map = {}

    def wire(self):
        self.view.root.protocol('WM_DELETE_WINDOW', self.terminate)
        for p in self.view.pads:
            p.bind('<Button-1>', self.padHit)
            self.view.root.bind('<{}>'.format(p.defn.key), self.keyHit)
            self.key_map[p.defn.key] = {
                'widget' : p,
                'handler' : self._padHit
            }

    def terminate(self):
        self.view.destroy()
        self.model.terminate()

    def keyHit(self, event):
        if event.keysym in self.key_map:
            b = self.key_map[event.keysym]
            b['handler'](event, b['widget'])

    def _padHit(self, event, pad):
        self.model.playNote(60 + pad.defn.index)

    def padHit(self, event):
        self._padHit(event, event.widget)


        class App:

    def __init__(self, skin):
        self.skin = skin
        self.midi = MidiController()
        self.view = View(skin)
        self.ctl = UiController(self, self.view, self.midi)

    def start(self):
        self.view.build()
        self.ctl.wire()
        self.view.start()

    
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

