#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# UI views.
#

from tkinter import *
from util import *
from controls import *
from collections.abc import Sequence

class TkImages:

    def __init__(self, skin):
        self.skin = skin
        self.background = None
        self.pads = []
        self.tonics = []
        self.octaves = []
        self.patterns = []

    def load_two_state_buttons(self, defs, images):
        for d in defs:
            image = self.load_image(d.image_path)
            active_image = self.load_image(d.active_image_path)
            images.append((image, active_image))

    def load(self):
        self.background = self.load_image(self.skin.background)
        self.load_two_state_buttons(self.skin.pads, self.pads)
        self.load_two_state_buttons(self.skin.tonics, self.tonics)
        self.load_two_state_buttons(self.skin.octaves, self.octaves)
        self.load_two_state_buttons(self.skin.patterns, self.patterns)

    def load_image(self, path, zoom = 0):
        path = resolve_path(self.skin.resource_dir, path)
        i = PhotoImage(file = path)
        if zoom:
            i.zoom(zoom)
        return i

class TkButtonGroup(Sequence):

    def __init__(self, buttons):
        self.buttons = buttons
        self.active = None

    def set_active(self, button):
        if (self.active):
            self.active.set_active(False)
        self.active = button
        button.set_active(True)

    def __getitem__(self, index):
        return self.buttons[index]

    def __len__(self):
        return len(self.buttons)

class TkView:

    def __init__(self):
        self.skin = None
        self.root = None
        self.pads = []
        self.tonics = []
        self.octaves = []
        self.patterns = []
        self.images = None
        self.pattern_name = None
        self.active_pad = None

    def create(self, skin):
        self.skin = skin
        self.images = TkImages(skin)
        self.root = Tk()
        self.create_ui()

    def start(self):
        self.root.focus()
        self.root.mainloop()

    def destroy(self):
        self.root.destroy()
        self.root = None
        self.pads = None
        self.tonics = None
        self.octaves = None
        self.patterns = None
        self.images = None
        self.pattern_name = None

    def create_root(self):
        self.root.title(self.skin.title)
        self.root.geometry('{}x{}'.format(self.skin.width, self.skin.height))
        self.background = Label(self.root, image = self.images.background)
        self.background.pack()

    def create_two_state_buttons(self, defs, images):
        buttons = []
        idx = 0
        for p in defs:
            imgs = images[idx]
            b = TkTwoStateButton(self.root, width = p.width, height = p.height,
                                 bg = 'black',
                                 images = imgs)
            idx += 1
            buttons.append(b)
            b.photo = imgs[0]
            b.defn = p
            b.place(x = p.x, y = p.y)
        return buttons

    def create_pads(self):
        b = self.create_two_state_buttons(self.skin.pads, self.images.pads)
        self.pads = TkButtonGroup(b)

    def create_tonics(self):
        b = self.create_two_state_buttons(self.skin.tonics, self.images.tonics)
        self.tonics = TkButtonGroup(b)

    def create_octaves(self):
        b = self.create_two_state_buttons(self.skin.octaves, self.images.octaves)
        self.octaves = TkButtonGroup(b)

    def create_patterns(self):
        b = self.create_two_state_buttons(self.skin.patterns, self.images.patterns)
        self.patterns = TkButtonGroup(b)

    def create_text_label(self, defn):
        r = None
        if defn:
            attrs = defn.attrs.copy()
            align = attrs['align']
            if align == 'left':
                attrs['anchor'] = 'w'
            elif align == 'right':
                attrs['anchor'] = 'e'
            attrs['justify'] = align
            del attrs['align']
            attrs['bg'] = attrs['background']
            del attrs['background']
            attrs['fg'] = attrs['color']
            del attrs['color']
            attrs['font'] = (attrs['font'], attrs['font-size'])
            del attrs['font-size']
            x = attrs['x']
            del attrs['x']
            y = attrs['y']
            del attrs['y']

            r = Label(self.root, text = "", **attrs)
            r.place(x = x, y = y)
        return r

    def create_pattern_name(self):
        self.pattern_name = self.create_text_label(self.skin.pattern_name)

    def create_ui(self):
        self.images.load()
        self.create_root()
        self.create_pads()
        self.create_tonics()
        self.create_octaves()
        self.create_patterns()
        self.create_pattern_name()

    def set_active_pad(self, pad):
        self.pads.set_active(pad)

    def set_active_octave(self, button):
        self.octaves.set_active(button)

    def set_active_tonic(self, button):
        self.tonics.set_active(button)

    def set_active_pattern(self, button):
        self.patterns.set_active(button)

    def update_button_group(self, buttons, active, setter):
        if active >= 0 and active < len(buttons):
            setter(buttons[active])

    def update_octave(self, index):
        self.update_button_group(self.octaves, index, self.set_active_octave)

    def update_tonic(self, index):
        self.update_button_group(self.tonics, index, self.set_active_tonic)

    def update_pattern(self, index, name):
        self.update_button_group(self.patterns, index, self.set_active_pattern)
        self.update_pattern_name(name)

    def update_pattern_name(self, name):
        if self.pattern_name:
            self.pattern_name.configure(text = " " + name)

    def update(self, model):
        self.update_octave(model.octave)
        self.update_tonic(model.tonic)
        self.update_pattern(model.pattern, model.get_pattern_name())

if __name__ == '__main__':
    pass
