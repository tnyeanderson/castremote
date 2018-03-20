import castremote

castremote.setup("Castaway")

# GPIO Pins
castremote.config.add_pin("STOP", 16, castremote.controls.stop_casting)
castremote.config.add_pin("PLAYPAUSE", 21, castremote.controls.toggle_play)
castremote.config.add_pin("REWIND", 18, castremote.controls.rewind)
castremote.config.add_pin("FASTFORWARD", 23, castremote.controls.fastforward)
castremote.config.add_pin("VOLUMEDOWN", 24, castremote.controls.volume_dec)
castremote.config.add_pin("VOLUMEUP", 25, castremote.controls.volume_inc)
castremote.config.add_pin("MUTE", 20, castremote.controls.toggle_mute)

castremote.start()