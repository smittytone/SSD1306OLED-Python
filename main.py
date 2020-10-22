# IMPORTS
import time
from machine import I2C, Pin
from ssd1306_micropython import SSD1306OLED

# START
if __name__ == '__main__':
    # Set up I2C on the FT232H Breakout
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

    # Set up the RST pin
    reset = Pin(2, Pin.OUT)

    # Set up the display
    display = SSD1306OLED(reset, i2c, 0x3D, 128, 64)

    # Get initial values
    #display.text("Standard line 1 8px").draw()
    #display.move(0, 8).text("Standard line 2 8px").draw()
    for i in range (0, 64 - 15):
        display.clear().move(0, i).text_2x("Line " + str(i) + " 16px").draw()
        time.sleep(0.05)