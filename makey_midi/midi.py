#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# MIDI interface.
#

import pygame.midi
import threading
import time

class Note:

    def __init__(self, number, volume, channel, expiration):
        self.number = number
        self.volume = volume
        self.channel = channel
        self.expiration = expiration

class MidiController:

    MIN_PITCH_BEND = -8192
    MAX_PITCH_BEND = 8191

    def __init__(self, cfg):
        self.cfg = cfg
        self.output = None
        self.player = None
        self.duration = None
        self.silencer = None
        self.silencer_cv = None
        self.quit_silencer = False
        self.active_notes = None

    def _duration_nanos(self, d):
        return int(d * 1000000000)

    def start(self):
        self.active_notes = {}

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.midi.init()
        self.output = pygame.midi.get_default_output_id()
        self.player = pygame.midi.Output(self.output)
        self.silencer_cv = threading.Condition()
        self.quit_silencer = False
        self.silencer = threading.Thread(target=self.silencer_thread)
        self.silencer.start()

    def set_instrument(self, instrument, channel):
        print('set ', instrument, channel)
        self.player.set_instrument(instrument, channel)

    def set_pitch_bend(self, v):
        v = min(p, max(p, MidiController.MIN_PITCH_BEND), MidiController.MAX_PITCH_BEND)
        self.player.pitch_bend(v)

    def silencer_thread(self):
        done = False
        period = 0.1
        while not done:
            with self.silencer_cv:
                done = self.quit_silencer
                self.silence(period)
            if not done:
                time.sleep(period)
        with self.silencer_cv:
            self.silencer_cv.notify()

    def silence(self, period):
        now = time.time_ns()
        when = now + self._duration_nanos(period / 2)
        for k in list(self.active_notes):
            n = self.active_notes[k]
            if period == 0 or (n.expiration >= 0 and n.expiration <= when):
                #print('kill {}'.format(n))
                self.player.note_off(n.number, n.volume, n.channel)
                del self.active_notes[k]

    def play_note(self, number, volume, channel):
        with self.silencer_cv:
            now = time.time_ns()
            if self.duration != None:
                exp = now + self.duration
            else:
                exp = -1
            k = (channel, number)
            note = Note(number, volume, channel, exp)
            self.active_notes[k] = note
            self.player.note_on(number, volume, channel)

    def terminate(self):
        with self.silencer_cv:
            self.quit_silencer = True
            self.silencer_cv.wait()
        self.silence(0)
        self.player = None
        self.silencer_cv = None
        self.silencer = None
        self.active_notes = None
        pygame.midi.quit()

if __name__ == '__main__':
    pass
