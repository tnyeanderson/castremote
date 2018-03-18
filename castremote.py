#!/usr/bin/env python3

import pychromecast
import time
import keyboard
import os

from EmulatorGUI import GPIO

# GPIO Pins
STOPPIN=20
PLAYPAUSEPIN=21
REWINDPIN=22
FASTFORWARDPIN=23
VOLUMEDOWNPIN=24
VOLUMEUPPIN=25
MUTEPIN=26



# GPIO Configuration
try:
    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(STOPPIN, GPIO.IN) # Stop
    GPIO.setup(PLAYPAUSEPIN, GPIO.IN) # Play/Pause
    GPIO.setup(REWINDPIN, GPIO.IN) # Rewind
    GPIO.setup(FASTFORWARDPIN, GPIO.IN) # Fast Forward
    GPIO.setup(VOLUMEDOWNPIN, GPIO.IN) # Volume Down
    GPIO.setup(VOLUMEUPPIN, GPIO.IN) # Volume Up
    GPIO.setup(MUTEPIN, GPIO.IN) # Mute
except Exception as ex:
    traceback.print_exc()
finally:
    GPIO.cleanup() #this ensures a clean exit



# Chromecast Name
MYCAST = 'Castaway'

# Increments
SEEKINCREMENT = 10
VOLUMEINCREMENT = 0.1




if os.getuid() != 0:
    print("Requires sudo privileges")
    raise SystemExit(0)

# Functions
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
    return

def toggleMute():
    cast.set_volume_muted(not cast.status.volume_muted)
    return

def rewind():
    seek(getCurrentTime() - SEEKINCREMENT)

def fastforward():
    seek(getCurrentTime() + SEEKINCREMENT)

def seek(newTime):
    mc.seek(newTime)
    return


# Get chromecasts
chromecasts = pychromecast.get_chromecasts()

# Friendly Names
[cc.device.friendly_name for cc in chromecasts]

# Set the chromecast based on MYCAST
cast = next(cc for cc in chromecasts if cc.device.friendly_name == MYCAST)

# Wait for the cast to load in
cast.wait()

# Set media contoller
mc = cast.media_controller


print("Listening...")
while True: # Infinite loop
    try: # If user pressed other than the given key error will not be shown
        if GPIO.input(STOPPIN):
            print("Do stop")
            break
            time.sleep(1)
        elif GPIO.input(PLAYPAUSEPIN):
            togglePlay()
            time.sleep(.8)
        elif GPIO.input(REWINDPIN):
            rewind()
            time.sleep(.8)
        elif GPIO.input(FASTFORWARDPIN):
            fastforward()
            time.sleep(.8)
        elif GPIO.input(VOLUMEDOWNPIN):
            decVolume()
            time.sleep(.3)
        elif GPIO.input(VOLUMEUPPIN):
            incVolume()
            time.sleep(.3)
        elif GPIO.input(MUTEPIN):
            toggleMute()
            time.sleep(.8)
        elif keyboard.is_pressed('q'):
            break
        else:
            pass
    except:
        continue
