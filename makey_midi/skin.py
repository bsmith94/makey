#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# UI definitions.
#

import os
import json
from util import *

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

if __name__ == '__main__':
    pass


