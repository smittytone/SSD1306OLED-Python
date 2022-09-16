"""
Runs on a Raspberry Pi Pico or similar with MicroPython installed
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
OLED_WIDTH = 128
OLED_HEIGHT = 32
PAUSE = 3

"""
RUNTIME START
"""
if __name__ == '__main__':
    # Set up I2C
    i2c = I2C(0, scl=Pin(9), sda=Pin(8)) # Raspberry Pi Pico

    # Set up the RST pin
    reset = Pin(19, Pin.OUT) # Raspberry Pi Pico

    # Set up OLED display for a 128x32 panel
    display = SSD1306OLED(reset, i2c, 0x3C, OLED_WIDTH, OLED_HEIGHT)

    while True:
        # Write some random text
        display.clear().home().text_2x("CPU: 45%").move(0,16).text_("MEM: 15%")
        display.move(63, 16).text("DISK: 88%").move(0, 24).text("NET: 1Gbps").draw()
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
        for i in range(0, OLED_HEIGHT, 4):
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
