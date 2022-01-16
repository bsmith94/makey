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

    MIN_VALUE = 0
    MAX_VALUE = 127

    def __init__(self, number, velocity, channel, expiration):
        self.number = number
        self.velocity = velocity
        self.channel = channel
        self.expiration = expiration

class Silencer:

    def __init__(self, midi, period):
        self.midi = midi
        self.cv = None
        self.icoming_vc = None
        self.thread = None
        self.active_notes = None
        self.incoming_active_notes = None
        self.quit_thread = False
        self.period = period

    def start(self):
        self.active_notes = {}
        self.incoming_active_notes = {}
        self.quit_thread = False
        self.cv = threading.Condition()
        self.incoming_cv = threading.Condition()
        self.thread = threading.Thread(target = self.run)
        self.thread.start()

    def run(self):
        done = False
        while not done:
            with self.cv:
                self.silence(self.period)
                self.cv.wait(self.period)
                done = self.quit_thread
        self.silence(0)
        with self.cv:
            self.cv.notify_all()

    def _duration_nanos(self, d):
        return int(d * 1000000000)

    def silence(self, period):
        with self.cv:
            now = time.time_ns()
            when = now + self._duration_nanos(period / 2)
            with self.incoming_cv:
                self.active_notes.update(self.incoming_active_notes)
                self.incoming_active_notes.clear()
            for k in list(self.active_notes):
                n = self.active_notes[k]
                if period == 0 or (n.expiration != None and n.expiration <= when):
                    self.midi.player.note_off(n.number, n.velocity, n.channel)
                    del self.active_notes[k]

    def note_on(self, notes):
        with self.incoming_cv:
            for n in notes:
                self.incoming_active_notes[(n.channel, n.number)] = n

    def quit(self):
        with self.cv:
            self.quit_thread = True
            self.cv.wait()
        self.thread.join()
        self.cv = None
        self.incoming_cv = None
        self.thread = None
        self.active_notes = None
        self.incoming_active_notes = None


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
        self.silencer = Silencer(self, 0.1)
        self.silencer.start()

    def set_instrument(self, instrument, channel):
        self.player.set_instrument(instrument, channel)

    def set_pitch_bend(self, v):
        v = min(p, max(p, MidiController.MIN_PITCH_BEND), MidiController.MAX_PITCH_BEND)
        self.player.pitch_bend(v)

    def play_note(self, numbers, velocity, duration, channel):
        if not type(numbers) is list:
            numbers = [numbers]
        [self.player.note_on(n, velocity, channel) for n in numbers]
        now = time.time_ns()
        if duration != None:
            exp = now + int(duration * 1000000000)
        else:
            exp = None
        notes = [Note(n, velocity, channel, exp) for n in numbers]
        self.silencer.note_on(notes)

    def midi_to_ansi_note(self, number):
        return pygame.midi.midi_to_ansi_note(number)

    def terminate(self):
        self.silencer.quit()
        self.silencer = None
        self.player = None
        self.active_notes = None
        pygame.midi.quit()

if __name__ == '__main__':
    pass
