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

class Silencer:

    def __init__(self, midi):
        self.midi = midi
        self.cv = None
        self.thread = None
        self.active_notes = {}
        self.quit_thread = False

    def start(self):
        self.quit_thread = False
        self.cv = threading.Condition()
        self.thread = threading.Thread(target = self.run)
        self.thread.start()

    def run(self):
        done = False
        period = 0.1
        while not done:
            with self.cv:
                self.silence(period)
                self.cv.wait(period)
                done = self.quit_thread
        with self.cv:
            self.cv.notify_all()

    def _duration_nanos(self, d):
        return int(d * 1000000000)

    def silence(self, period):
        with self.cv:
            now = time.time_ns()
            when = now + self._duration_nanos(period / 2)
            for k in list(self.active_notes):
                n = self.active_notes[k]
                if period == 0 or (n.expiration >= 0 and n.expiration <= when):
                    self.midi.player.note_off(n.number, n.volume, n.channel)
                    del self.active_notes[k]

    def note_on(self, note):
        with self.cv:
            self.active_notes[(note.channel, note.number)] = note

    def quit(self):
        with self.cv:
            self.quit_thread = True
            self.cv.wait()
        self.silence(0)
        self.cv = None
        self.thread = None
        self.active_notes = None


class MidiController:

    MIN_PITCH_BEND = -8192
    MAX_PITCH_BEND = 8191

    def __init__(self, cfg):
        self.cfg = cfg
        self.output = None
        self.player = None
        self.silencer = None

    def start(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.midi.init()
        self.output = pygame.midi.get_default_output_id()
        self.player = pygame.midi.Output(self.output)
        self.silencer = Silencer(self)
        self.silencer.start()

    def set_instrument(self, instrument, channel):
        self.player.set_instrument(instrument, channel)

    def set_pitch_bend(self, v):
        v = min(p, max(p, MidiController.MIN_PITCH_BEND), MidiController.MAX_PITCH_BEND)
        self.player.pitch_bend(v)

    def play_note(self, number, volume, duration, channel):
        now = time.time_ns()
        if duration != None:
            exp = now + duration
        else:
            exp = -1
        note = Note(number, volume, channel, exp)
        self.silencer.note_on(note)
        self.player.note_on(number, volume, channel)

    def terminate(self):
        self.silencer.quit()
        self.silencer = None
        self.player = None
        self.active_notes = None
        pygame.midi.quit()

if __name__ == '__main__':
    pass
