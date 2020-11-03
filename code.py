"""
IMPORTS
"""
import board
import busio
import digitalio
from random import randint
from time import sleep
from ssd1306 import SSD1306OLED

"""
CONSTANTS
"""
OLED_WIDTH = 128
OLED_HEIGHT = 64
PAUSE = 3


"""
RUNTIME START
"""
if __name__ == '__main__':
    # Set up I2C
    i2c = busio.I2C(board.SCL, board.SDA)
    while not i2c.try_lock():
        pass

    # Set up the RST pin
    reset = digitalio.DigitalInOut(board.D5)
    reset.direction = digitalio.Direction.OUTPUT

    # Set up OLED display
    display = SSD1306OLED(reset, i2c, 0x3D, OLED_WIDTH, OLED_HEIGHT)
    """
    # Write some random text
    display.home().text_2x("CPU: 45%").move(0,16).text_2x("MEM: 15%")
    display.move(0,32).text_2x("DISK: 88%").move(0,48).text("NET: 1Gbps")
    display.move(0,56).text("WLAN: 802.11ac").draw()
    sleep(PAUSE)

    display.clear().draw()
    for i in range(0,21,4):
        display.line(0, 0, 80 - i * 4, 63)
    display.draw()
    sleep(PAUSE)

    for i in range(0,21,4):
        display.line(i * 4, 63, 80, 0)
    display.draw()
    sleep(PAUSE)
    """
    display.clear().draw()
    for i in range(0,64,4):
        display.plot(0, i).plot(1, i)
    for i in range(3,128,4):
        display.plot(i, 63).plot(i, 62)
    display.line(2,61,2,0).line(2,61,128,61).draw()

    x = 3
    y = 60
    state = True
    for i in range(0,10):
        k = 4 if state else 1
        display.line(x, y, x + 10, y - i * k).draw()
        state = not state
        x += 10
        y = y - i * k
        #sleep(PAUSE)