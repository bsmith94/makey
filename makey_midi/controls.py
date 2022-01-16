#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# UI widgets.
#

from tkinter import *


class TkTwoStateButton(Label):

    def __init__(self, parent, width = None, height = None, bg = None, images = None):
        super().__init__(parent, width = width, height = height, bg = bg,
                         image = (None, images[0])[images != None])
        self.images = images
        self.active = False

    def set_active(self, active):
        img = self.images[active]
        self.active = active
        self.config(image = img)
        self.photo = img
