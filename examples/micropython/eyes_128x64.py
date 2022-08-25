"""
Runs on a Raspberry Pi Pico with MicroPython installed
"""

"""
IMPORTS
"""
from utime import sleep
from machine import I2C, Pin
from random import randint
from ssd1306 import SSD1306OLED

"""
CONSTANTS
"""
DELAY = 0.5
CENTRE_SEP = 12
EYE_STATE_OPEN = 0
EYE_STATE_CLOSED = 1
EYE_MOOD_NORMAL = 0
EYE_MOOD_CROSS = 1
EYE_MOOD_SAD = 2
PUPIL_SIZE_SMALL = 0
PUPIL_SIZE_NORMAL = 1
PUPIL_SIZE_BIG = 2

# Set up eye data
PUPIL_SIZES = [2, 6, 10];
PUPIL_POSNS = [
    47, 16, 81, 16,     # Face on      0
    40, 16, 74, 16,     # Left         1
    54, 16, 88, 16,     # Right        2
    47, 9, 81, 9,       # Up           3
    47, 24, 81, 24,     # Down         4
    43, 12, 77, 12,     # Up left      5
    51, 12, 85, 12,     # Up right     6
    51, 20, 85, 20,     # Down right   7
    43, 20, 77, 20,     # Down left    8
    51, 20, 77, 20      # Doh!         9
]

"""
FUNCTIONS
"""
def eyes_open(oled, pupil_size, pupil_dir):
    # Draw blank open eyes
    eyes_clear(oled)

    # Draw in the pupils
    a = pupil_dir << 2;
    oled.circle(PUPIL_POSNS[a] - CENTRE_SEP, PUPIL_POSNS[a + 1], PUPIL_SIZES[pupil_size], 0, True)
    oled.circle(PUPIL_POSNS[a + 2] + CENTRE_SEP, PUPIL_POSNS[a + 3], PUPIL_SIZES[pupil_size], 0, True);

def eyes_closed(oled):
    # Draw blank closed eyes
    oled.circle(47 - CENTRE_SEP , 16, 14, 0, True).circle(81 + CENTRE_SEP, 16, 14, 0, True);

def eyes_clear(oled):
    # Draw blank open eyes
    oled.circle(47 - CENTRE_SEP, 16, 16, 1, True).circle(81 + CENTRE_SEP, 16, 16, 1, True)

def mouth_open(oled, is_wide=False):
    # Draw the teeth: two close rows or open wide in anger
    x = 29
    y = 44
    g = 5 if is_wide is False else 16

    # Clear the space
    oled.rect(x, y, 80, 20, 0)
    for i in range(14):
        oled.rect(x, y, 4, 4, 1, True)
        oled.rect(x, y + g, 4, 4, 1, True)
        x += 5
    if is_wide:
        # Fangs!
        oled.rect(34, 44, 4, 13, 1, True)
        oled.rect(89, 44, 4, 13, 1, True)

"""
ENTRY POINT
"""
if __name__ == '__main__':
    # Set up I2C
    i2c = I2C(0, scl=Pin(9), sda=Pin(8)) # Raspberry Pi Pico

    # Set up the RST pin
    reset = Pin(19, Pin.OUT) # Raspberry Pi Pico

    # Set up OLED display for a 128x64 panel
    width = 128
    height = 64
    display = SSD1306OLED(reset, i2c, 0x3D, width, height)

    mood_changed = False
    mood = 0
    eye_state = EYE_STATE_OPEN
    next_state = EYE_STATE_CLOSED
    pupil_direction = randint(0, 8)
    blink_count = 0
    mood_count = 0
    mouth_open(display)

    while True:
        blink_count += 1
        mood_count += 1
        next_state = -1

        if mood_changed is True:
            mood = new_mood
            mood_changed = False
            mood_count = 0

        if eye_state == EYE_STATE_CLOSED:
            # Draw the closed eyes
            eyes_closed(display);

            blink_count = 0
            next_state = EYE_STATE_OPEN
        else:
            # Only adjust eye direction if they eyes are open
            r = randint(0, 100)
            if pupil_direction > 0:
                if r > 20: pupil_direction = 0
            else:
                if r > 60: pupil_direction = randint(0, 8)
                if r == 3: pupil_direction = 9

            # Draw eyes open
            eyes_open(display, PUPIL_SIZE_NORMAL, pupil_direction)

        # Should we close next time?
        if blink_count > 5 and randint(0, 10) > 6:
            next_state = EYE_STATE_CLOSED

        # Add eyebrows if necessary
        if mood == EYE_MOOD_CROSS:
            # Clear the space above each eye
            display.line(38 - CENTRE_SEP, -10, 64 - CENTRE_SEP, 0, 10, 0).line(66 + CENTRE_SEP, 0, 92 + CENTRE_SEP, -10, 10, 0)
            mouth_open(display, True)

            if eye_state == EYE_STATE_CLOSED:
                # Eye is closed, so close the outline
                display.line(42 - CENTRE_SEP, 1, 60 - CENTRE_SEP, 9, 2, 1).line(68 + CENTRE_SEP, 9, 86 + CENTRE_SEP, 1, 2, 1)
        elif mood == EYE_MOOD_SAD:
            # Clear the space above each eye
            display.line(32 - CENTRE_SEP, 0, 56 - CENTRE_SEP, -10, 10, 0).line(72 + CENTRE_SEP , -10, 96 + CENTRE_SEP, 0, 10, 0)

            if eye_state == EYE_STATE_CLOSED:
                # Eye is closed, so close the outline
                display.line(34 - CENTRE_SEP, 9, 53 - CENTRE_SEP, 1, 2, 1).line(75 + CENTRE_SEP, 1, 94 + CENTRE_SEP, 9, 2, 1)

        # Gob
        mouth_open(display, (mood == EYE_MOOD_CROSS))

        # Did the eye state change? Set the new state now for the next iteration
        if next_state != -1: eye_state = next_state
        display.draw()

        # Look for a change of mood every 60s
        if mood_count > 60 / DELAY:
            r = randint(0, 1000)
            if r >= 950 and mood != EYE_MOOD_CROSS:
                mood_changed = True
                new_mood = EYE_MOOD_CROSS
            elif r <= 50 and mood != EYE_MOOD_SAD:
                mood_changed = True
                new_mood = EYE_MOOD_SAD
            elif mood != EYE_MOOD_NORMAL:
                mood_changed = True
                new_mood = EYE_MOOD_NORMAL

        # Pause for breath
        sleep(DELAY)
