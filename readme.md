
# Simbox

![Image](https://github.com/mihkelbaranov/simbox/raw/main/assets/1.jpg)

## Overview

This project uses a WeAct RP2040 microcontroller to build a simbox with 13 buttons and an ignition switch. Each button is mapped to a function key (F12 through F25) and the ignition switch triggers an F key press both when it is activated and deactivated. The setup uses CircuitPython and the `adafruit_hid` library for keyboard functionality.

## Components

- **WeAct RP2040** microcontroller
- **13 push buttons**
- **1 ignition switch**
- **Resistors** (internal pull-up resistors used in this setup)

## Wiring

- **Buttons**: Connect each button to one of the GPIO pins (GP0 to GP12) and to GND.
- **Ignition Switch**: Connect the ignition switch to GPIO pin GP13 and to GND.

### GPIO Pin Mapping

- Buttons: GP0, GP1, GP2, ..., GP12
- Ignition Switch: GP13

## Software Requirements

- **CircuitPython** for WeAct RP2040 (latest version recommended)
- **Adafruit HID Library** (for keyboard functionality)

## Installation

1. **Flash CircuitPython:**
   - Download the latest CircuitPython firmware for the RP2040 from the [CircuitPython website](https://circuitpython.org/board/weact_rp2040/).
   - Follow the instructions to flash the firmware onto the WeAct RP2040.

2. **Install the Adafruit HID Library:**
   - Download the `adafruit_hid` library from the [CircuitPython bundle](https://circuitpython.org/libraries).
   - Copy the `adafruit_hid` folder into the `lib` directory on your CIRCUITPY drive.

3. **Upload the Code:**
   - Save the provided Python code as `code.py` and copy it to the root of the CIRCUITPY drive on the WeAct RP2040.

## Code

```python
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
```

## Usage

- **Buttons**: Press any of the 13 buttons to send function key presses (F12 to F24) to the computer.
- **Ignition Switch**: Toggle the ignition switch to trigger the F25 key press both when turning it ON and OFF.

## Troubleshooting

- **Button Not Working**: Ensure each button is correctly wired to the specified GPIO pin and GND.
- **Ignition Switch Issue**: Verify the ignition switch wiring and confirm the correct pin is used for detection.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
