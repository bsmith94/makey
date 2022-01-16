#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# UI definitions.
#

import os
import json
from util import *


class WidgetDef:

    def __init__(self, width = None, height = None, x = None, y = None,
                 key = None, image_path = None):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.key = key
        self.image_path = image_path

    def load(self, data):
        self.width = json_get(data, 'width')
        self.height = json_get(data, 'height')
        self.x = json_get(data, 'x')
        self.y = json_get(data, 'y')
        self.key = json_get(data, 'key', required = False )
        self.image_path = json_get(data, 'image', required = False)


class ButtonDef(WidgetDef):

    def __init__(self, width = None, height = None, x = None, y = None,
                 key = None, image_path = None):
        super().__init__(width, height, x, y, key, image_path)

    def load(self, data, width = None, height = None, image_path = None):
        self.width = json_get(data, 'width', def_val = width)
        self.height = json_get(data, 'height', def_val = height)
        self.x = json_get(data, 'x')
        self.y = json_get(data, 'y')
        self.key = json_get(data, 'key')
        self.image_path = json_get(data, self.image_key(), def_val = image_path)

    def image_key(self):
        return 'image'

class TwoStateButtonDef(ButtonDef):
    
    def __init__(self, width = None, height = None, x = None, y = None,
                 key = None, image_path = None):
        super().__init__(width, height, x, y, key, image_path)
        self.active_image_path = None

    def load(self, data, width = None, height = None, image_path = None, active_image_path = None):
        super().load(data, width, height, image_path)
        self.active_image_path = json_get(data, 'image-active', def_val = active_image_path)

    def image_path(self):
        return 'image-inactive'

class Skin:

    def __init__(self):
        self.resource_dir = None
        self.path = None
        self.height = None
        self.width = None
        self.background = None
        self.pads = []


    def load(self, path):
        self.path = path
        self.resource_dir = os.path.dirname(os.path.realpath(path))
        with open(path) as f:
            d = json.load(f)
        self.load_root(d)
        self.load_pads(d)
        self.channels = WidgetDef()
        self.channels.load(json_get(json_get(d, 'controls'), 'channels'))

    def load_root(self, data):
        root = json_get(data, 'root')
        self.title = json_get(root, 'title')
        self.height = json_get(root, 'height')
        self.width = json_get(root, 'width')
        self.background = resolve_path(self.resource_dir, json_get(root, 'background'))

    def load_pads(self, data):
        pads = json_get(json_get(data, 'controls'), 'pads')
        instances = json_get(pads, 'instances')
        idx = 0
        for p in instances:
            d = TwoStateButtonDef()
            d.load(p, pads['width'], pads['height'],
                   json_get(pads, 'image-inactive', required = False),
                   json_get(pads, 'image-active', required = False))
            d.index = idx
            idx += 1
            self.pads.append(d)

if __name__ == '__main__':
    pass
