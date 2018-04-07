import sys
import pychromecast
import time
import os

from anygpio import GPIO

# Set module to `this`
this = sys.modules[__name__]

# Is the module ready
this.ready = False

# Initialize cast and mc to None
this.cast = None
this.mc = None

# Class definitions
class CastError(Exception):
	"""
	Generic error class for exceptions related to casting
	"""
	pass

class Configuration:
	"""
	Holds the castremote configuration information
	"""
	# Default values
	def __init__(self, device_name=None, seek_increment=10, volume_increment=0.1):
		# Set attributes
		self.device_name = device_name
		self.seek_increment = seek_increment
		self.volume_increment = volume_increment

class Controls:
	@staticmethod
	def get_current_time(*args):
		"""
		Returns the current seek time in seconds for MediaController
		"""
		return mc.status.adjusted_current_time

	@staticmethod
	def volume_inc(*args):
		"""
		Increases MediaController volume by increment (config.volume_increment)
		"""
		# Increase current volume to get new volume
		newVol = cast.status.volume_level + config.volume_increment

		# Make sure newvol has maximum value of 0
		if newVol > 1: newVol = 1

		# Set the volume if it's not at 1 already
		if cast.status.volume_level != 1: cast.set_volume(newVol)

	@staticmethod
	def volume_dec(*args):
		"""
		Decreases MediaController volume by increment (config.volume_increment)
		"""
		# Decrease current volume to get new volume
		newVol = cast.status.volume_level - config.volume_increment

		# Make sure newvol has minimum value of 0
		if newVol > 1: newVol = 1

		# Set the volume if it's not at 0 already
		if cast.status.volume_level != 0: cast.set_volume(newVol)

	@staticmethod
	def pause(*args):
		"""
		Pauses the MediaController
		"""
		mc.pause()

	@staticmethod
	def play(*args):
		"""
		Plays the MediaController
		"""
		mc.play()

	@staticmethod
	def toggle_play(*args):
		"""
		Runs play() or pause() based on current player_state
		"""
		if mc.status.player_state == 'PLAYING':
			controls.pause()
		else:
			controls.play()

	@staticmethod
	def toggle_mute(*args):
		"""
		Toggles whether MediaController is muted
		"""
		cast.set_volume_muted(not cast.status.volume_muted)

	@staticmethod
	def rewind(*args):
		"""
		Uses seek() to rewind MediaController by increment in seconds (config.seek_increment)
		"""
		controls.seek(controls.get_current_time() - config.seek_increment)

	@staticmethod
	def fastforward(*args):
		"""
		Uses seek() to fast forward MediaController by increment in seconds (config.seek_increment)
		"""
		controls.seek(controls.get_current_time() + config.seek_increment)

	@staticmethod
	def seek(newTime):
		"""
		Seeks MediaController to newTime (seconds)
		"""
		mc.seek(newTime)

	@staticmethod
	def stop_casting(*args):
		"""
		Stops casting
		"""
		cast.quit_app()

# Functions
def setup(device_name):
	"""
	Sets up a chromecast device

	device_name is the friendly name of the Chromecast
	"""
	# Set device name in config
	config.device_name = device_name

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

	# Let the user know
	print("Ready!")

def button(*args, **kwargs):
	"""
	Sets up a pin as input using anygpio

	button(id, name, callback)
	button(18, "STOP", controls.stop)
	"""
	GPIO.setup_pin(*args, **kwargs)

def start():
	"""
	Uses event-driven GPIO to listen for all button presses

	Registers the button's callback to provide Chromecast control
	"""
	GPIO._add_all_events(GPIO._get_input_pins_only())

def repeat_while_held(id, action, interval=0.3):
	"""
	Repeats an action while a button is held down

	Used with lambda functions as a button callback
	"""
	# Run the given action
	action()

	# While the button is held down
	while GPIO.pin(id).test():
		# Wait for interval (similar to bouncetime)
		time.sleep(interval)

		# Run the given action
		action()



# Require sudo
if os.getuid() != 0:
	print("Requires sudo privileges")

# Initialize the config and controls objects
this.config = Configuration()
this.controls = Controls()
