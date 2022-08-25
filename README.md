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

## Documentation ##

You can find full details of the driver’s methods [at my documentation site](https://smittytone.net/docs/ssd1306.html).

## Release Notes ##

- 2.0.0 *Unreleased*
    - Combine MicroPython and CircuitPython versions into a single class.
    - Update examples.
- 1.0.0 *25 August 2020*
    - Initial public release

## License ##

The SSD1306OLED library is licensed under the [MIT License](LICENSE).
