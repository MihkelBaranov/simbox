import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time

# Initialize the keyboard object
keyboard = Keyboard(usb_hid.devices)

# Define GPIO pins for buttons and the ignition switch
button_pins = [
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, 
    board.GP5, board.GP6, board.GP7
]
ignition_pin = board.GP13

switch_pins = [board.GP8, board.GP9, 
    board.GP10, board.GP11, board.GP12]

# Create digital input objects for each button with pull-up resistors
buttons = []
for pin in button_pins:
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append(button)
        

# Create digital input object for the ignition switch with pull-up resistor
ignition_switch = digitalio.DigitalInOut(ignition_pin)
ignition_switch.direction = digitalio.Direction.INPUT
ignition_switch.pull = digitalio.Pull.UP


# switch logic on off 
switches = []
for pin in switch_pins:
    switch = digitalio.DigitalInOut(pin)
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP
    switches.append(switch)
i

# Define HID usage codes for F12 to F25
F_KEYS = {
    12: Keycode.F12,  # F12
    13: Keycode.F13,  # F13
    14: Keycode.F14,  # F14
    15: Keycode.F15,  # F15
    16: Keycode.F16,  # F16
    17: Keycode.F17,  # F17
    18: Keycode.F18,  # F18
    19: Keycode.F19,  # F19
    20: Keycode.F20,  # F20
    21: Keycode.F21,  # F21
    22: Keycode.F22,  # F22
    23: Keycode.F23,  # F23
    24: Keycode.F24,  # F24

}

# Function to send an F key press
def press_key(key_code, key_name):
    print(f"Pressed {key_name}")
    keyboard.press(key_code)
    keyboard.release_all()


# Initialize the previous state of the ignition switch
previous_ignition_state = True  # Assume the switch starts in the OFF state (True for pulled-up)
previous_switch_states = [switch.value for switch in switches]  # True when off

switch_states = [False] * len(switches)


# Main loop
while True:
    # Check button states
    for i, button in enumerate(buttons):
        if not button.value:  # Check if the button is pressed (LOW when pressed)
            f_key_number = 12 + i  # Calculate F key number (F12, F13, F14, ...)
            if f_key_number <= 25:  # Handle up to F25
                press_key(F_KEYS[f_key_number], f_key_number)
                time.sleep(0.2)  # Debounce delay

    # Check ignition switch state
    current_ignition_state = not ignition_switch.value  # LOW when pressed

    if current_ignition_state and not previous_ignition_state:  # Detect state change from OFF to ON
        press_key(Keycode.SEMICOLON, ";")  # Trigger F25 with the ignition switch ON

    elif not current_ignition_state and previous_ignition_state:  # Detect state change from ON to OFF
        press_key(Keycode.SEMICOLON, ";")  # Trigger F25 with the ignition switch OFF

    # Update previous state
    previous_ignition_state = current_ignition_state
    
    # Check other switches' states
    for i, switch in enumerate(switches):
        current_switch_state = switch.value  # True when off (pulled-up)
        if current_switch_state != previous_switch_states[i]:  # Detect any state change
            f_key_number = 19 + (i + 1)  # Assign F-keys starting from F21
            if f_key_number in F_KEYS:
                press_key(F_KEYS[f_key_number], f_key_number)
        
        # Update the previous state for this switch
        previous_switch_states[i] = current_switch_state
        
    # Add a small delay to reduce the CPU load
    time.sleep(0.1)