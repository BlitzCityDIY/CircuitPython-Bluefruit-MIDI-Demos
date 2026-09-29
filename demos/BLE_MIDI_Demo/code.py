# SPDX-FileCopyrightText: 2026 Liz Clark
#
# SPDX-License-Identifier: MIT

# Circuit Playground Bluefruit BLE MIDI

import time
import board
import touchio
import adafruit_ble
import adafruit_midi
import adafruit_ble_midi
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_midi.note_on          import NoteOn
from adafruit_midi.note_off         import NoteOff

#  BLE MIDI setup
midi_service = adafruit_ble_midi.MIDIService()
advertisement = ProvideServicesAdvertisement(midi_service)

ble = adafruit_ble.BLERadio()
if ble.connected:
    for c in ble.connections:
        c.disconnect()

#  midi setup
midi = adafruit_midi.MIDI(midi_out=midi_service, out_channel=0)

print("advertising")
ble.start_advertising(advertisement)

#  midi note numbers
midi_notes = [60, 62, 64, 65, 67, 69, 71] # C scale from middle C

pins = [board.A1, board.A2, board.A3, board.A4, board.A5, board.A6, board.TX]
touch_inputs = []
touch_states = []
for touch in pins:
    touch_pin = touchio.TouchIn(touch)
    touch_inputs.append(touch_pin)
    state = False
    touch_states.append(state)

while True:
    #  BLE connection
    print("Waiting for connection")
    while not ble.connected:
        pass
    print("Connected")
    time.sleep(1.0)

    #  while BLE is connected...
    while ble.connected:
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
    #  BLE connection
    print("Disconnected")
    print()
    ble.start_advertising(advertisement)
