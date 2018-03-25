# CircuitPython demo - Keyboard emulator

import time
from digitalio import DigitalInOut, Direction, Pull
import board
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# A simple neat keyboard demo in CircuitPython

# The pins we'll use, each will have an internal pullup
keypress_pins = [board.A1, board.A2]
# Our array of key objects
key_pin_array = []
# The Keycode sent for each button, will be paired with a control key
keys_pressed = [Keycode.A, "Hello World!\n"]
control_key = Keycode.SHIFT

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard()
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

# Make all pin objects inputs with pullups
for pin in keypress_pins:
    key_pin = DigitalInOut(pin)
    key_pin.direction = Direction.INPUT
    key_pin.pull = Pull.UP
    key_pin_array.append(key_pin)

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

print("Waiting for key pin...")

while True:
    # Check each pin
    for key_pin in key_pin_array:
        if not key_pin.value:  # Is it grounded?
            i = key_pin_array.index(key_pin)
            print("Pin #%d grounded." % i)

            # Turn on the red LED
            led.value = True

            while not key_pin.value:
                pass  # Wait for it to be released!
            # Type the Keycode or string
            key = keys_pressed[i]  # Get the corresponding Keycode or string
            # if type(key) is str:
            if isinstance(key, str):
                keyboard_layout.write(key)
            else:
                keyboard.press(control_key, key)  # Press...
                keyboard.release_all()  # ...Release!

            # Turn off the red LED
            led.value = False

    time.sleep(0.01)