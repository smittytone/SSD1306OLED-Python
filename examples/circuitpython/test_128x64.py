"""
Runs on a Raspberry Pi Pico or similar with MicroPython installed
"""

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
    i2c = busio.I2C(board.GP9, board.GP8)
    while not i2c.try_lock():
        pass

    # Set up the RST pin
    reset = digitalio.DigitalInOut(board.GP19)
    reset.direction = digitalio.Direction.OUTPUT

    # Set up OLED display for a 128x64 panel
    display = SSD1306OLED(reset, i2c, 0x3D, OLED_WIDTH, OLED_HEIGHT)

    while True:
        # Write some random text
        display.clear().home().text_2x("CPU: 45%").move(0,16).text_2x("MEM: 15%")
        display.move(0,32).text_2x("DISK: 88%").move(0,48).text("NET: 1Gbps")
        display.move(0,56).text("WLAN: 802.11ac").draw()
        sleep(PAUSE * 5)

        # Draw some patterns:
        # Lines
        display.clear().draw()
        for i in range(0, 31, 4):
            display.line(0, 0, 120 - i * 4, OLED_HEIGHT - 1)
        display.draw()
        sleep(PAUSE)

        display.clear().draw()
        for i in range(0, 31, 4):
            display.line(i * 4, OLED_HEIGHT - 1, 120, 0)
        display.draw()
        sleep(PAUSE)

        # Circles
        display.clear().draw()
        fill = True
        for i in range(0, 11):
            display.circle(randint(0, OLED_WIDTH), randint(0, OLED_HEIGHT), randint(4, OLED_HEIGHT // 2 - 1), 1, fill).draw()
            fill = not fill
            sleep(PAUSE / 2)
        
        # Rectangles
        display.clear().draw()
        fill = True
        for i in range(0, 11):
            display.rect(randint(0, OLED_WIDTH), randint(0, OLED_HEIGHT), randint(0, OLED_HEIGHT), randint(0, OLED_HEIGHT // 2), 1, fill).draw()
            fill = not fill
            sleep(PAUSE / 2)
        sleep(PAUSE * 5)

        # Draw a chart
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
            sleep(PAUSE)

        pixel_length = display.length_of_string("Growth")
        display.move(127 - pixel_length, 40).text("Growth").draw()
        sleep(PAUSE * 5)
