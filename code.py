import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
import time

# Initialize the keyboard object
keyboard = Keyboard(usb_hid.devices)

# Define GPIO pins for buttons and the ignition switch
button_pins = [
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, 
    board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, 
    board.GP10, board.GP11, board.GP12
]
ignition_pin = board.GP13

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

# Define HID usage codes for F12 to F25
F_KEYS = {
    12: 0x3A,  # F12
    13: 0x68,  # F13
    14: 0x69,  # F14
    15: 0x6A,  # F15
    16: 0x6B,  # F16
    17: 0x6C,  # F17
    18: 0x6D,  # F18
    19: 0x6E,  # F19
    20: 0x6F,  # F20
    21: 0x70,  # F21
    22: 0x71,  # F22
    23: 0x72,  # F23
    24: 0x73,  # F24
    25: 0x74   # F25
}

# Function to send an F key press
def press_f_key(f_key, f_key_number):
    print(f"Pressed F{f_key_number}")
    keyboard.press(f_key)
    keyboard.release_all()

# Initialize the previous state of the ignition switch
previous_ignition_state = True  # Assume the switch starts in the OFF state (True for pulled-up)

# Main loop
while True:
    # Check button states
    for i, button in enumerate(buttons):
        if not button.value:  # Check if the button is pressed (LOW when pressed)
            f_key_number = 12 + i  # Calculate F key number (F12, F13, F14, ...)
            if f_key_number <= 25:  # Handle up to F25
                press_f_key(F_KEYS[f_key_number], f_key_number)
                time.sleep(0.2)  # Debounce delay

    # Check ignition switch state
    current_ignition_state = not ignition_switch.value  # LOW when pressed

    if current_ignition_state and not previous_ignition_state:  # Detect state change from OFF to ON
        press_f_key(F_KEYS[25], 25)  # Trigger F25 with the ignition switch ON

    elif not current_ignition_state and previous_ignition_state:  # Detect state change from ON to OFF
        press_f_key(F_KEYS[25], 25)  # Trigger F25 with the ignition switch OFF

    # Update previous state
    previous_ignition_state = current_ignition_state

    # Add a small delay to reduce the CPU load
    time.sleep(0.1)