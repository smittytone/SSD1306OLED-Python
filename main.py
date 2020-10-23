# IMPORTS
import utime as time
from urandom import getrandbits
from machine import I2C, Pin
from ssd1306_micropython import SSD1306OLED


# FUNCTIONS
def randint(start, stop=None):
    if stop is None:
        stop = start
        start = 0
    upper = stop - start
    bits = 0
    pwr2 = 1
    while upper > pwr2:
        pwr2 <<= 1
        bits += 1
    while True:
        r = getrandbits(bits)
        if r < upper: break
    return r + start

def make_rect():
    return (randint(-10, 137), randint(-10, 53), randint(10, 80), randint(10, 50))


# START
if __name__ == '__main__':
    # Set up I2C on the FT232H Breakout
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

    # Set up the RST pin
    reset = Pin(2, Pin.OUT)

    # Set up the display
    display = SSD1306OLED(reset, i2c, 0x3D, 128, 64)

    display.text_2x("supercallifragilisticexpiallidocious").draw()