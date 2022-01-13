#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# Midi controller
#

import json
import os
from tkinter import *

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


class App:

    def __init__(self, skin):
        self.skin = skin

    def terminate(self):
        self.root.destroy()

    def start(self):
        self.root = Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.terminate)
        self.build_ui()
        self.root.focus()
        self.root.mainloop()

    def build_ui(self):
        self.skin.resolve()
        self.root.title(self.skin.title)
        self.root.geometry('{}x{}'.format(self.skin.width, self.skin.height))
        self.background = Label(self.root, image = self.skin.background_img)
        self.background.pack()
        
    
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

