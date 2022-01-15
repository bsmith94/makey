#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# UI views.
#

from tkinter import *
from util import *

class TkImages:

    def __init__(self, skin):
        self.skin = skin
        self.background = None
        self.pads = []

    def load(self):
        self.background = self.loadImage(self.skin.background)
        for p in self.skin.pads:
            image = self.loadImage(p.image_path)
            self.pads.append(image)

    def loadImage(self, path, zoom = 0):
        path = resolve_path(self.skin.resource_dir, path)
        i = PhotoImage(file = path)
        if zoom:
            i.zoom(zoom)
        return i

class TkView:

    def __init__(self):
        self.skin = None
        self.root = None
        self.pads = []
        self.images = None

    def create(self, skin):
        self.skin = skin
        self.images = TkImages(skin)
        self.root = Tk()
        self.createUi()

    def start(self):
        self.root.focus()
        self.root.mainloop()

    def destroy(self):
        self.root.destroy()
        self.root = None
        self.pads = None
        self.images = None

    def createRoot(self):
        self.root.title(self.skin.title)
        self.root.geometry('{}x{}'.format(self.skin.width, self.skin.height))
        self.background = Label(self.root, image = self.images.background)
        self.background.pack()

    def createPads(self):
        idx = 0
        for p in self.skin.pads:
            img = self.images.pads[idx]
            l = Label(self.root, width = p.width, height = p.height,
                       bg='black', image=img)
            idx += 1
            self.pads.append(l)
            l.photo = img
            l.defn = p
            l.place(x=p.x, y=p.y)

    def createUi(self):
        # skin.resolve() must be invoked after Tk is created
        self.images.load()
        self.createRoot()
        self.createPads()

if __name__ == '__main__':
    pass
