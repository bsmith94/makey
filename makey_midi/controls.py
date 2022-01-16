#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# UI widgets.
#

from tkinter import *


class TkTwoStateButton(Label):

    def __init__(self, parent, images = None, **kwargs):
        super().__init__(parent, image = (None, images[0])[images != None], **kwargs)
        self.images = images
        self.active = False

    def set_active(self, active):
        active =(False,True)[active]
        img = self.images[active]
        self.active = active
        self.config(image = img)
        self.photo = img
