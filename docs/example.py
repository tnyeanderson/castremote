import castremote
import time

print("Setting up chromecast...")

# With a chromecast named "Caster the Friendly Host"
castremote.setup("Caster the Friendly Host")

# GPIO Pins
# Pin actions are found in castremote.controls
# button(PIN_ID, PIN_NAME, PIN_ACTION)
castremote.button(16, "STOP", castremote.controls.stop_casting)
castremote.button(21, "PLAYPAUSE", castremote.controls.toggle_play)
castremote.button(18, "REWIND", castremote.controls.rewind)
castremote.button(23, "FASTFORWARD", castremote.controls.fastforward)
castremote.button(24, "VOLUMEDOWN", lambda *_: castremote.repeat_while_held(24, castremote.controls.volume_dec))
castremote.button(25, "VOLUMEUP", lambda *_: castremote.repeat_while_held(25, castremote.controls.volume_inc))
castremote.button(20, "MUTE", castremote.controls.toggle_mute)

# Start listening for input on the pins
castremote.start()

# Keep the script running indefinitely
while True:
	time.sleep(120)
