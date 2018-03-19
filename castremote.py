#!/usr/bin/env python3

import pychromecast
import time
import os

import RPi.GPIO as GPIO

# Class definitions
class Pin:
    def __init__(self, name, pin, action):
        # Set attributes
        self.name = name
        self.pin = pin
        self.action = action

        # Initialize GPIO pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    @property
    def pinValue(self):
        # Returns the input value of the GPIO pin
        return GPIO.input(self.pin)


class Configuration:
    # Default values
    def __init__(self, cast_name, seek_increment=10, volume_increment=0.1):
        # Set attributes
        self.cast_name = cast_name
        self.seek_increment = seek_increment
        self.volume_increment = volume_increment
        self.pins = []

    def add_pin(name, pin, action):
        # Add a GPIO pin configuration to the pins array
        self.pins.append(Pin(name, pin, action))


class Controls:
    @property
    def getCurrentTime():
        return mc.status.adjusted_current_time()

    def incVolume():
        # Increase current volume to get new volume
        newVol = cast.status.volume_level + VOLUMEINCREMENT

        # Make sure newvol has maximum value of 0
        if newVol > 1: newVol = 1

        # Set the volume if it's not at 1 already
        if cast.status.volume_level != 1: cast.set_volume(newVol)
        return

    def decVolume():
        # Decrease current volume to get new volume
        newVol = cast.status.volume_level - VOLUMEINCREMENT

        # Make sure newvol has minimum value of 0
        if newVol > 1: newVol = 1

        # Set the volume if it's not at 0 already
        if cast.status.volume_level != 0: cast.set_volume(newVol)
        return

    def castPause():
        mc.pause()
        return

    def castPlay():
        mc.play()
        return

    def togglePlay():
        if mc.status.player_state == 'PLAYING':
            castPause()
        else:
            castPlay()
        time.sleep(.8)
        return

    def toggleMute():
        cast.set_volume_muted(not cast.status.volume_muted)
        time.sleep(.8)
        return

    def rewind():
        seek(getCurrentTime() - SEEKINCREMENT)
        time.sleep(.8)
        return

    def fastforward():
        seek(getCurrentTime() + SEEKINCREMENT)
        time.sleep(.8)
        return

    def seek(newTime):
        mc.seek(newTime)
        return

    def stop_casting():
        cast.quit_app()
        time.sleep(1)
        return


# Functions
def start(pins):
    print("Listening...")
    while True: # Infinite loop
        for pin in pins:
            # False is pressed
            if pin.pinValue() == False:
                print("Doing " & pin.name)
                pin.action()
    end()

def end():
    GPIO.cleanup() # Ensures clean exit


# Requrire sudo
if os.getuid() != 0:
    print("Requires sudo privileges")
    raise SystemExit(0)


# GPIO Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# Get chromecasts
chromecasts = pychromecast.get_chromecasts()

# Get friendly names of chromecasts
[cc.device.friendly_name for cc in chromecasts]

# Set the chromecast based on cast_name
cast = next(cc for cc in chromecasts if cc.device.friendly_name == MYCAST)

# Wait for the cast to load in
cast.wait()

# Set media contoller
mc = cast.media_controller
