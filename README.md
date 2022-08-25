# SSD1306OLED Python 2.0.0 #

A hardware driver for the [Adafruit 128x32 OLED](https://www.adafruit.com/product/931) and [Adafruit 128x64 OLED](https://www.adafruit.com/product/326) panels, which are based on the Solomon SSD1306 controller. The OLEDs communicate over any I&sup2;C bus.

The driver is compatible with [MicroPython](http://micropython.org) and [CircuitPython](https://circuitpython.org).

### Character Set ###

The driver contains a full, proportionally spaced Ascii character set with Ascii values 32 through 127. Codes 0 through 31 are used for user-defined characters.

### I2C Addressing ###

The displays have the following default I2C addresses:

- 128x32 — `0x3C`
- 128x64 — `0x3D`

The first of these is the constructor default, so you will need to pass in the second value if you are using the larger panel. You will need to pass in an alternative address if you have changed it at the board level.

## Class Usage ##

### Constructor: SSD1306OLED(*reset_pin, i2c[, address][, height][, width]*) ###

To instantiate an SSD1306OLED object pass the reset pin and I&sup2;C bus to which the display is connected, and, optionally, its I&sup2;C address, pixel height and pixel width. If no address is passed, the default value, `0x3C` will be used. The default pixel dimensions are 128 x 32.

The passed reset pin and I&sup2;C bus must be configured before the SSD1306OLED object is created.

#### CircuitPython Example ####

```python
import board
import busio
from ssd1306 import SSD1306

# Set up I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Set up the RST pin (pin 7 on this board)
reset = digitalio.DigitalInOut(board.D7)
reset.direction = digitalio.Direction.OUTPUT

# Set up OLED display using the default settings
display = SSD1306OLED(reset, i2c)
```

#### MicroPython Example ####

```python
from machine import I2C, Pin
from ssd1306 import SSD1306

# Set up I2C
i2c = I2C(0, scl=Pin(9), sda=Pin(8)) # Raspberry Pi Pico

# Set up the RST pin
reset = Pin(7, Pin.OUT)

# Set up OLED display using the default settings
display = SSD1306OLED(reset, i2c)
```

## Class Methods ##

### clear() ###

This method clears the driver’s graphics buffer. It does not update the screen — call [*draw()*](#draw) to do so.

*clear()* returns a reference to the driver instance in order to allow command chaining. For example:

```python
display.clear().text("Hello, World!").draw()
```

### draw() ###

This method is used to write the contents of the driver’s buffer to the display itself.

#### Example ####

```python
# Draw a diagonal line
display.line(0,0,127,31).draw()
```

### set_inverse(*is_inverse*) ###

This method is called to set the display to black-on-white (`True`) or white-on-black (`False`). It defaults to `True`.

### move(*x, y*) ###

This method moves the graphics cursor to the specified co-ordinates.

### home() ###

This method moves the graphics cursor to the home position: the top left of the screen (co-ordinates 0,0).

### plot(*x, y[, colour]*) ###

This sets or clears a single pixel, specified by its co-ordinates, on the display. It does not update the screen — call [*draw()*](#draw) to do so.

By default, *plot()* uses the current ink colour: white for a white-on-black display, or black for black-on-white (see [*set_inverse()*](#set-inverse-is-inverse)), but you can set the ink colour to clear the pixel instead. Pass 1 for the foreground colour (the default) or 0 for the background colour.

*plot()* returns a reference to the driver instance in order to allow command chaining.

#### Example ####

```python
# Put dots in the corners
display.plot(0,0).plot(0,31)
display.plot(127,0).plot(127,31)
display.draw()
```

### line(*x, y, tox, toy[, thick][, colour])* ###

This method draws a line between the co-ordinates (x,y) and (tox,toy) of the required thickness. If no thickness is specified the method defaults to a single pixel. If no ink colour is specified, the method defaults to the current foreground colour.

*line()* returns a reference to the driver instance in order to allow command chaining. It does not update the screen — call [*draw()*](#draw) to do so.

#### Example ####

```python
# Draw two diagonal lines
display.line(0,0,127,31).line(127,0,0,31).draw()
```

### circle(*x, y, radius[, color][, fill]*) ###

This method draws a circle centred on the co-ordinates (x,y) and with the specified radius. If no ink colour is specified, the method defaults to the current foreground colour. You can also opt to pass `True` into the *fill* parameter to create a solid circle; otherwise an outline will be drawn.

*circle()* does not update the screen — call [*draw()*](#draw) to do so.

#### Example ####

```python
# Draw two filled circles side by side
display.circle(47, 16, 14, 1, True).circle(81, 16, 14, 1, True).draw();
```

### text(*the_text[, do_wrap]*) ###

Render the specified text into the buffer at the current co-ordinates, set using [*move()*](#movex-y). If *do_wrap* is `True` (the default), wrap text onto a new line if necessary and possible.

*text()* does not update the screen — call [*draw()*](#draw) to do so.

#### Example ####

```python
for i in range (0, 56):
    display.clear().move(0, i).text("Line " + str(i) + " 8px").draw()
```

### text_2x(*the_text[, do_wrap]*) ###

Render the specified text at double-size into the buffer at the current co-ordinates, set using [*move()*](#movex-y). If *do_wrap* is `True` (the default), wrap text onto a new line if necessary and possible.

*text()* does not update the screen — call [*draw()*](#draw) to do so.

#### Example ####

```python
for i in range (0, 49):
    display.clear().move(0, i).text_2x("Line " + str(i) + " 16px").draw()
```

### length_of_string(*the_string*) ###

Returns the length of the string in pixels. This assumes standard-size (8px) characters and a single-pixel space between adjacent characters.

## Release Notes ##

- 1.0.0 *Unreleased*
    - Initial public release

## License ##

The SSD1306OLED library is licensed under the [MIT License](LICENSE).
