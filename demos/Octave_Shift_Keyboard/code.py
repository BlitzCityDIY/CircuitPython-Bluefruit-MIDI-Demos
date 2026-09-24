# SPDX-FileCopyrightText: 2026 Liz Clark
#
# SPDX-License-Identifier: MIT

# Circuit Playground Bluefruit Capacitive Touch MIDI Keyboard
# Change scale octave with onboard buttons

import time
import board
import digitalio
import touchio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on          import NoteOn
from adafruit_midi.note_off         import NoteOff
from adafruit_debouncer import Debouncer

#  midi setup
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

#  midi note numbers
BASE_NOTES = [60, 62, 64, 65, 67, 69, 71] # C scale from middle C
midi_notes = BASE_NOTES
MIN_OCTAVE = -4   # C0 (MIDI 12)
MAX_OCTAVE = 3    # C7 (MIDI 96)
octave = 0

pins = [board.A1, board.A2, board.A3, board.A4, board.A5, board.A6, board.TX]
touch_inputs = []
touch_states = []
for touch in pins:
    touch_pin = touchio.TouchIn(touch)
    touch_inputs.append(touch_pin)
    state = False
    touch_states.append(state)

buttona = digitalio.DigitalInOut(board.BUTTON_A)
buttona.switch_to_input(pull=digitalio.Pull.DOWN)
octave_down = Debouncer(buttona)

buttonb = digitalio.DigitalInOut(board.BUTTON_B)
buttonb.switch_to_input(pull=digitalio.Pull.DOWN)
octave_up = Debouncer(buttonb)

def shifted_notes():
    return [n + octave * 12 for n in BASE_NOTES]
    # list = []
    # for n in BASE_NOTES:
    #   note = n + octave * 12
    #   list.append(note)
    # midi_notes = array

while True:
    octave_down.update()
    octave_up.update()
    for i in range(len(touch_inputs)):
        inputs = touch_inputs[i]
        #  if touch is pressed...
        if inputs.value and touch_states[i] is False:
            #  update touch state
            touch_states[i] = True
            #  send NoteOn for corresponding MIDI note
            midi.send(NoteOn(midi_notes[i], 120))

        #  if the touch is released...
        if not inputs.value and touch_states[i] is True:
            #  send NoteOff for corresponding MIDI note
            midi.send(NoteOff(midi_notes[i], 120))
            #  reset touch state
            touch_states[i] = False
    if octave_down.fell and octave > MIN_OCTAVE:
        octave -= 1
        midi_notes = shifted_notes()
        print(octave, midi_notes)
    if octave_up.fell and octave < MAX_OCTAVE:
        octave += 1
        midi_notes = shifted_notes()
        print(octave, midi_notes)
