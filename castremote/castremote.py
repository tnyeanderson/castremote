import sys
import pychromecast
import time
import os

from EmulatorGUI import GPIO
# import RPi.GPIO as GPIO

# Set module to `this`
this = sys.modules[__name__]

# Is the module ready
this.ready = False

# Initialize config to None
this.config = None

# Initialize cast and mc to None
this.cast = None
this.mc = None

# Class definitions
class CastError(Exception):
    pass

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
    def __init__(self, device_name=None, seek_increment=10, volume_increment=0.1):
        # Set attributes
        self.device_name = device_name
        self.seek_increment = seek_increment
        self.volume_increment = volume_increment
        self.pins = []

    def add_pin(self, name, pin, action):
        # Add a GPIO pin configuration to the pins array
        self.pins.append(Pin(name, pin, action))


class Controls:
    @property
    def get_current_time():
        return mc.status.adjusted_current_time()

    def volume_inc():
        # Increase current volume to get new volume
        newVol = cast.status.volume_level + VOLUMEINCREMENT

        # Make sure newvol has maximum value of 0
        if newVol > 1: newVol = 1

        # Set the volume if it's not at 1 already
        if cast.status.volume_level != 1: cast.set_volume(newVol)
        return

    def volume_dec():
        # Decrease current volume to get new volume
        newVol = cast.status.volume_level - VOLUMEINCREMENT

        # Make sure newvol has minimum value of 0
        if newVol > 1: newVol = 1

        # Set the volume if it's not at 0 already
        if cast.status.volume_level != 0: cast.set_volume(newVol)
        return

    def cast_pause():
        mc.pause()
        return

    def cast_play():
        mc.play()
        return

    def toggle_play():
        if mc.status.player_state == 'PLAYING':
            castPause()
        else:
            castPlay()
        time.sleep(.8)
        return

    def toggle_mute():
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
def setup(device_name=""):
    # Set device name in config if it is passed
    if device_name:
        config.device_name = device_name

    # Abort if config.device_name is not set
    if config.device_name is None:
        raise CastError("Cast device name not set")

    # Get chromecasts
    chromecasts = pychromecast.get_chromecasts()

    # If no chromecasts are found, raise an error
    if not chromecasts:
        raise CastError("No cast devices were found")

    # Get friendly names of chromecasts
    [cc.device.friendly_name for cc in chromecasts]

    # Set the global cast variable based on device_name
    this.cast = next(
        (cc for cc in chromecasts if cc.device.friendly_name == config.device_name),
        None
    )

    if cast is None:
        raise CastError("Cast device not found: " + config.device_name)

    # Wait for the cast to load in
    cast.wait()

    # Set global media contoller
    this.mc = cast.media_controller

    this.ready = True

def start(pins):
    print("Listening...")
    while True: # Infinite loop
        for pin in pins:
            # False is pressed
            if pin.pinValue() == False:
                print("Doing " + pin.name)
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

this.config = Configuration()
this.controls = Controls()
