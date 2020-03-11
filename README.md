# SSD1306OLED 1.0.0 #

A hardware driver for the [Adafruit 128x32 OLED](https://www.adafruit.com/product/931) and [Adafruit 128x64 OLED](https://www.adafruit.com/product/326) panels, which are based on the Solomon SSD1306 controller. The OLEDs communicate over any I&sup2;C bus.

### Character Set ###

The driver contains a full, proportionally spaced Ascii character set.

### I2C Addressing ###

The displays have the following default I2C addresses:

- 128x32 — `0x3C`
- 128x64 — `0x3D`

The first of these is the constructor default, so you will need to pass in the second value if you are using the larger panel. You will need to pass in an alternative address if you have changed it at the board level.

## Class Usage ##

### Constructor: SSD1306OLED(*reset_pin, i2c[, address][, height][, width]*) ###

To instantiate an SSD1306OLED object pass the reset pin and I&sup2;C bus to which the display is connected, and, optionally, its I&sup2;C address, pixel height and pixel width. If no address is passed, the default value, `0x3C` will be used. The default pixel dimensions are 128 x 32.

The passed reset pin and I&sup2;C bus must be configured before the SSD1306OLED object is created.

#### Example ####

```python
# Set up I2C on the FT232H Breakout
i2c = busio.I2C(board.SCL, board.SDA)

# Set up the RST pin
reset = digitalio.DigitalInOut(board.D7)
reset.direction = digitalio.Direction.OUTPUT

# Set up OLED display as the default address
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

This method moves the text cursor to the specified co-ordinates.

### home() ###

This method moves the text cursor to the home position: the top left of the screen (co-ordinates (0,0).

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

*circle()* does not update the display, only the buffer. Call *update()* to refresh the LED.

#### Example ####

```python
# Draw two filled circles side by side
display.circle(47, 16, 14, 0, True).circle(81, 16, 14, 0, True).draw();
```

## Release Notes ##

- 1.0.0 *11 march 2020*
    - Initial public release

## License ##

The SSD1306OLED library is licensed under the [MIT License](LICENSE).
