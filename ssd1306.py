class SSD1306OLED:
    """
    A simple driver for the I2C-connected Solomon SSD1306 controller chip and an OLED display.
    For example: https://www.adafruit.com/product/931
    This release is written for MicroPython and CircuitPython

    Version:   2.0.0
    Author:    smittytone
    Copyright: 2022, Tony Smith
    Licence:   MIT
    """

    # *********** CONSTANTS **********

    SSD1306_MEMORYMODE = 0x20
    SSD1306_COLUMNADDR = 0x21
    SSD1306_PAGEADDR = 0x22
    SSD1306_WRITETOBUFFER = 0x40
    SSD1306_SETSTARTLINE = 0x40
    SSD1306_SETCONTRAST = 0x81
    SSD1306_CHARGEPUMP = 0x8D
    SSD1306_SEGREMAP = 0xA1
    SSD1306_DISPLAYALLON_RESUME = 0xA4
    SSD1306_DISPLAYALLON = 0xA5
    SSD1306_NORMALDISPLAY = 0xA6
    SSD1306_INVERTDISPLAY = 0xA7
    SSD1306_SETMULTIPLEX = 0xA8
    SSD1306_DISPLAYOFF = 0xAE
    SSD1306_DISPLAYON = 0xAF
    SSD1306_COMSCANDEC = 0xC8
    SSD1306_SETDISPLAYOFFSET = 0xD3
    SSD1306_SETDISPLAYCLOCKDIV = 0xD5
    SSD1306_SETPRECHARGE = 0xD9
    SSD1306_SETCOMPINS = 0xDA
    SSD1306_SETVCOMDETECT = 0xDB
    #SSD1306_SETLOWCOLUMN = 0x00
    #SSD1306_EXTERNALVCC = 0x01
    #SSD1306_SWITCHCAPVCC = 0x02
    #SSD1306_SETHIGHCOLUMN = 0x10
    #SSD1306_RIGHT_HORIZONTAL_SCROLL = 0x26
    #SSD1306_LEFT_HORIZONTAL_SCROLL = 0x27
    #SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
    #SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = 0x2A
    #SSD1306_DEACTIVATE_SCROLL = 0x2E
    #SSD1306_ACTIVATE_SCROLL = 0x2F
    #SSD1306_SET_VERTICAL_SCROLL_AREA = 0xA3
    #SSD1306_COMSCANINC = 0xC0

    CHARSET = [
        b"\x00\x00",                # space - Ascii 32
        b"\xfa",                    # !
        b"\xe0, 0xc0\x00\xe0\xc0",  # "
        b"\x24\x7e\x24\x7e\x24",    # #
        b"\x24\xd4\x56\x48",        # $
        b"\xc6\xc8\x10\x26\xc6",    # %
        b"\x6c\x92\x6a\x04\x0a",    # &
        b"\xc0",                    # '
        b"\x7c\x82",                # (
        b"\x82\x7c",                # )
        b"\x10\x7c\x38\x7c\x10",    # *
        b"\x10\x10\x7c\x10\x10",    # +
        b"\x06\x07",                # ,
        b"\x10\x10\x10\x10\x10",    # -
        b"\x06\x06",                # .
        b"\x04\x08\x10\x20\x40",    # /
        b"\x7c\x8a\x92\xa2\x7c",    # 0 - Ascii 48
        b"\x42\xfe\x02",            # 1
        b"\x46\x8a\x92\x92\x62",    # 2
        b"\x44\x92\x92\x92\x6c",    # 3
        b"\x18\x28\x48\xfe\x08",    # 4
        b"\xf4\x92\x92\x92\x8c",    # 5
        b"\x3c\x52\x92\x92\x8c",    # 6
        b"\x80\x8e\x90\xa0\xc0",    # 7
        b"\x6c\x92\x92\x92\x6c",    # 8
        b"\x60\x92\x92\x94\x78",    # 9
        b"\x36\x36",                # : - Ascii 58
        b"\x36\x37",                # ;
        b"\x10\x28\x44\x82",        # <
        b"\x24\x24\x24\x24\x24",    # =
        b"\x82\x44\x28\x10",        # >
        b"\x60\x80\x9a\x90\x60",    # ?
        b"\x7c\x82\xba\xaa\x78",    # @
        b"\x7e\x90\x90\x90\x7e",    # A - Ascii 65
        b"\xfe\x92\x92\x92\x6c",    # B
        b"\x7c\x82\x82\x82\x44",    # C
        b"\xfe\x82\x82\x82\x7c",    # D
        b"\xfe\x92\x92\x92\x82",    # E
        b"\xfe\x90\x90\x90\x80",    # F
        b"\x7c\x82\x92\x92\x5c",    # G
        b"\xfe\x10\x10\x10\xfe",    # H
        b"\x82\xfe\x82",            # I
        b"\x0c\x02\x02\x02\xfc",    # J
        b"\xfe\x10\x28\x44\x82",    # K
        b"\xfe\x02\x02\x02\x02",    # L
        b"\xfe\x40\x20\x40\xfe",    # M
        b"\xfe\x40\x20\x10\xfe",    # N
        b"\x7c\x82\x82\x82\x7c",    # O
        b"\xfe\x90\x90\x90\x60",    # P
        b"\x7c\x82\x92\x8c\x7a",    # Q
        b"\xfe\x90\x90\x98\x66",    # R
        b"\x64\x92\x92\x92\x4c",    # S
        b"\x80\x80\xfe\x80\x80",    # T
        b"\xfc\x02\x02\x02\xfc",    # U
        b"\xf8\x04\x02\x04\xf8",    # V
        b"\xfc\x02\x3c\x02\xfc",    # W
        b"\xc6\x28\x10\x28\xc6",    # X
        b"\xe0\x10\x0e\x10\xe0",    # Y
        b"\x86\x8a\x92\xa2\xc2",    # Z - Ascii 90
        b"\xfe\x82\x82",            # [
        b"\x40\x20\x10\x08\x04",    # \
        b"\x82\x82\xfe",            # "
        b"\x20\x40\x80\x40\x20",    # ^
        b"\x02\x02\x02\x02\x02",    # _
        b"\xc0\xe0",                # '
        b"\x04\x2a\x2a\x2a\x1e",    # a - Ascii 97
        b"\xfe\x22\x22\x22\x1c",    # b
        b"\x1c\x22\x22\x22",        # c
        b"\x1c\x22\x22\x22\xfc",    # d
        b"\x1c\x2a\x2a\x2a\x10",    # e
        b"\x10\x7e\x90\x90\x80",    # f
        b"\x18\x25\x25\x25\x3e",    # g
        b"\xfe\x20\x20\x20\x1e",    # h
        b"\xbe\x02",                # i
        b"\x02\x01\x01\x21\xbe",    # j
        b"\xfe\x08\x14\x22",        # k
        b"\xfe\x02",                # l
        b"\x3e\x20\x18\x20\x1e",    # m
        b"\x3e\x20\x20\x20\x1e",    # n
        b"\x1c\x22\x22\x22\x1c",    # o
        b"\x3f\x22\x22\x22\x1c",    # p
        b"\x1c\x22\x22\x22\x3f",    # q
        b"\x22\x1e\x22\x20\x10",    # r
        b"\x12\x2a\x2a\x2a\x04",    # s
        b"\x20\x7c\x22\x22\x04",    # t
        b"\x3c\x02\x02\x3e",        # u
        b"\x38\x04\x02\x04\x38",    # v
        b"\x3c\x06\x0c\x06\x3c",    # w
        b"\x22\x14\x08\x14\x22",    # x
        b"\x39\x05\x06\x3c",        # y
        b"\x26\x2a\x2a\x32",        # z - Ascii 122
        b"\x10\x7c\x82\x82",        # {
        b"\xee",                    # |
        b"\x82\x82\x7c\x10",        # }
        b"\x40\x80\x40\x80",        # ~
        b"\x60\x90\x90\x60"         # Degrees sign - Ascii 127
    ]

    COS_TABLE = [
        0.000,0.035,0.070,0.105,0.140,0.174,0.208,0.243,0.276,0.310,0.343,0.376,0.408,0.439,0.471,0.501,0.531,0.561,0.589,0.617,0.644,
        0.671,0.696,0.721,0.745,0.768,0.790,0.810,0.830,0.849,0.867,0.884,0.900,0.915,0.928,0.941,0.952,0.962,0.971,0.979,0.985,0.991,
        0.995,0.998,1.000,1.000,0.999,0.997,0.994,0.990,0.984,0.977,0.969,0.960,0.949,0.938,0.925,0.911,0.896,0.880,0.863,0.845,0.826,
        0.806,0.784,0.762,0.739,0.715,0.690,0.664,0.638,0.610,0.582,0.554,0.524,0.494,0.463,0.432,0.400,0.368,0.335,0.302,0.268,0.234,
        0.200,0.166,0.131,0.096,0.062,0.027,-0.008,-0.043,-0.078,-0.113,-0.148,-0.182,-0.217,-0.251,-0.284,-0.318,-0.351,-0.383,-0.415,
        -0.447,-0.478,-0.508,-0.538,-0.567,-0.596,-0.624,-0.651,-0.677,-0.702,-0.727,-0.750,-0.773,-0.795,-0.815,-0.835,-0.854,-0.872,
        -0.888,-0.904,-0.918,-0.931,-0.944,-0.955,-0.964,-0.973,-0.981,-0.987,-0.992,-0.996,-0.998,-1.000,-1.000,-0.999,-0.997,-0.993,
        -0.988,-0.982,-0.975,-0.967,-0.957,-0.947,-0.935,-0.922,-0.908,-0.893,-0.876,-0.859,-0.840,-0.821,-0.801,-0.779,-0.757,-0.733,
        -0.709,-0.684,-0.658,-0.631,-0.604,-0.575,-0.547,-0.517,-0.487,-0.456,-0.424,-0.392,-0.360,-0.327,-0.294,-0.260,-0.226,-0.192,
        -0.158,-0.123,-0.088,-0.053,-0.018]

    SIN_TABLE = [
        1.000,0.999,0.998,0.994,0.990,0.985,0.978,0.970,0.961,0.951,0.939,0.927,0.913,0.898,0.882,0.865,0.847,0.828,0.808,0.787,
        0.765,0.742,0.718,0.693,0.667,0.641,0.614,0.586,0.557,0.528,0.498,0.467,0.436,0.404,0.372,0.339,0.306,0.272,0.238,0.204,
        0.170,0.135,0.101,0.066,0.031,-0.004,-0.039,-0.074,-0.109,-0.144,-0.178,-0.213,-0.247,-0.280,-0.314,-0.347,-0.379,-0.412,
        -0.443,-0.474,-0.505,-0.535,-0.564,-0.593,-0.620,-0.647,-0.674,-0.699,-0.724,-0.747,-0.770,-0.792,-0.813,-0.833,-0.852,
        -0.870,-0.886,-0.902,-0.916,-0.930,-0.942,-0.953,-0.963,-0.972,-0.980,-0.986,-0.991,-0.995,-0.998,-1.000,-1.000,-0.999,
        -0.997,-0.994,-0.989,-0.983,-0.976,-0.968,-0.959,-0.948,-0.936,-0.924,-0.910,-0.895,-0.878,-0.861,-0.843,-0.823,-0.803,
        -0.782,-0.759,-0.736,-0.712,-0.687,-0.661,-0.635,-0.607,-0.579,-0.550,-0.520,-0.490,-0.459,-0.428,-0.396,-0.364,-0.331,
        -0.298,-0.264,-0.230,-0.196,-0.162,-0.127,-0.092,-0.057,-0.022,0.013,0.048,0.083,0.117,0.152,0.187,0.221,0.255,0.288,
        0.322,0.355,0.387,0.419,0.451,0.482,0.512,0.542,0.571,0.599,0.627,0.654,0.680,0.705,0.730,0.753,0.776,0.797,0.818,0.837,
        0.856,0.874,0.890,0.906,0.920,0.933,0.945,0.956,0.966,0.974,0.981,0.988,0.992,0.996,0.999,1.000]


    # *********** CONSTRUCTOR **********

    def __init__(self, reset_pin, i2c, address=0x3C, width=128, height=32):
        assert 0x00 <= address < 0x80, "ERROR - Invalid I2C address in HT16K33()"

        # Just in case it hasn't been imported by the caller
        import time

        # Determine whether we're on MicroPython or CircuitPython
        try:
            import machine
            self.is_micropython = True
        except:
            self.is_micropython = False

        # Set up instance properties
        self.i2c = i2c
        self.address = address
        self.rst = reset_pin
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.buffer = bytearray(width * int(height / 8))

        # Toggle the RST pin over 1ms + 10ms
        self._set_rst()
        time.sleep(0.001)
        self._set_rst(False)
        time.sleep(0.01)
        self._set_rst()

        # Write the display settings
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_DISPLAYOFF]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETDISPLAYCLOCKDIV, 0x80]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETMULTIPLEX, self.height - 1]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETDISPLAYOFFSET, 0x00]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETSTARTLINE]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_CHARGEPUMP, 0x14]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_MEMORYMODE, 0x00]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SEGREMAP]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_COMSCANDEC]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETCOMPINS, 0x02 if self.height in (16, 32) else 0x12]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETCONTRAST, 0x8F]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETPRECHARGE, 0xF1]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_SETVCOMDETECT, 0x40]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_DISPLAYALLON_RESUME]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_NORMALDISPLAY]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_DISPLAYON]))

        pages = (self.height // 8) - 1 # 0x03 if self.height == 64 else 0x07
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_COLUMNADDR, 0x00, self.width - 1]))
        self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_PAGEADDR, 0x00, pages]))

        # Clear the display
        self.clear()
        self.draw()

    # *********** PUBLIC METHODS **********

    def set_inverse(self, is_inverse=True):
        """
        Set the entire display to black-on-white or white-on-black

        Args:
            is_inverse (bool): should the display be black-on-white (True) or white-on-black (False).
        """
        if is_inverse:
            self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_INVERTDISPLAY]))
        else:
            self.i2c.writeto(self.address, bytes([0x00, self.SSD1306_NORMALDISPLAY]))

    def home(self):
        """
        Set the cursor to the home position, (0, 0), at the top left of the screen

        Returns:
            The display object
        """
        return self.move(0, 0)

    def move(self, x, y):
        """
        Set the cursor to the specified position

        Args:
            x (int) The X co-ordinate in the range 0 - 127
            y (int) The Y co-ordinate in the range 0 - 32 or 64, depending on model

        Returns:
            The instance (self)
        """
        assert (0 <= x < self.width) and (0 <= y < self.height), "ERROR - Out-of-range co-ordinate(s) passed to move()"
        self.x = x
        self.y = y
        return self

    def plot(self, x, y, colour=1):
        """
        Plot a point (or clear) the pixel at the specified co-ordinates

        Args:
            x      (int) The X co-ordinate in the range 0 - 127
            y      (int) The Y co-ordinate in the range 0 - 32 or 64, depending on model
            colour (int) The colour of the pixel: 1 for set, 0 for clear. Default: 1

        Returns:
            The instance (self)
        """
        # Bail if any co-ordinates are off the screen
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return self
        if colour not in (0, 1): colour = 1
        byte = self._coords_to_index(x, y)
        bit = y - ((y >> 3) << 3)
        if colour == 1:
            # Set the pixel
            self.buffer[byte] |= (1 << bit)
        else:
            # Clear the pixel
            self.buffer[byte] &= ~(1 << bit)
        return self

    def line(self, x, y, tox, toy, thick=1, colour=1):
        """
        Draw a line between the specified co-ordnates

        Args:
            x      (int) The start X co-ordinate in the range 0 - 127
            y      (int) The start Y co-ordinate in the range 0 - 32 or 64, depending on model
            tox    (int) The end X co-ordinate in the range 0 - 127
            toy    (int) The end Y co-ordinate in the range 0 - 32 or 64, depending on model
            think  (int) The thickness of the line in pixels. Default: 1
            colour (int) The colour of the pixel: 1 for set, 0 for clear. Default: 1

        Returns:
            The instance (self)
        """
        # Make sure we have a thickness of at least one pixel
        thick = max(thick, 1)
        if colour not in (0, 1): colour = 1
        # Look for vertical and horizontal lines
        track_by_x = True
        if x == tox: track_by_x = False
        if (toy == y) and (track_by_x is False): return self
        #assert (y != toy) and (track_by_x is False), "ERROR - Bad co-ordinates passed to line()"

        # Swap start and end values for L-R raster
        if track_by_x:
            if x > tox:
                a = x
                x = tox
                tox = a
            start = x
            end = tox
            m = float(toy - y) / float(tox - x)
        else:
            if y > toy:
                a = y
                y = toy
                toy = a
            start = y
            end = toy
            m = float(tox - x) / float(toy - y)

        # Run for 'thick' times to generate thickness
        for j in range(thick):
            # Run from x to tox, calculating the y offset at each point
            for i in range(start, end):
                if track_by_x:
                    dy = y + int(m * (i - x)) + j
                    if (0 <= i < self.width) and (0 <= dy < self.height):
                        self.plot(i, dy, colour)
                else:
                    dx = x + int(m * (i - y)) + j
                    if (0 <= i < self.height) and (0 <= dx < self.width):
                        self.plot(dx, i, colour)
        return self

    def circle(self, x, y, radius, colour=1, fill=False):
        """
        Draw a circle at the specified co-ordinates

        Args:
            x (int)      The centre X co-ordinate in the range 0 - 127
            y (int)      The centre Y co-ordinate in the range 0 - 32 or 64, depending on model
            radius (int) The radius of the circle
            colour (int) The colour of the pixel: 1 for set, 0 for clear. Default: 1
            fill (bool)  Should the circle be solid (true) or outline (false). Default: false

        Returns:
            The instance (self)
        """
        for i in range(180):
            a = x - int(radius * self.SIN_TABLE[i])
            b = y - int(radius * self.COS_TABLE[i])
            # plot() handles off-screen plotting
            self.plot(a, b, colour)
            if fill:
                if a > x:
                    j = x
                    while j < a and j < self.width:
                        self.plot(j, b, colour)
                        j += 1
                else:
                    j = a + 1
                    while j <= x:
                        self.plot(j, b, colour)
                        j += 1
        return self

    def rect(self, x, y, width, height, colour=1, fill=False):
        """
        Draw a rectangle at the specified co-ordinates

        Args:
            x      (int)  The start X co-ordinate in the range 0 - 127
            y      (int)  The start Y co-ordinate in the range 0 - 32 or 64, depending on model
            width  (int)  The width of the rectangle
            height (int)  The height of the rectangle
            fill   (bool) Should the rectangle be solid (true) or outline (false). Default: false

        Returns:
            The instance (self)
        """
        # Make sure we only draw on the screen
        x = max(x, 0)
        y = max(y, 0)
        if x + width > self.width: width = self.width - x
        if y + height > self.height: height = self.height - y
        if colour not in (0, 1): colour = 1
        for i in range(y, y + height):
            for j in range(x, x + width):
                self.plot(j, i, colour)
                if fill is False and x < j < x + width - 1 and y < i < y + height - 1:
                    self.plot(j, i, 0)
        return self

    def text(self, print_string, do_wrap=True):
        """
        Write a line of text at the current cursor co-ordinates

        Args:
            print_string (string) The text to print

        Returns:
            The display object
        """
        assert len(print_string) > 0, "ERROR - Zero-length string passed to text()"
        return self._draw_text(print_string, do_wrap, False)


    def text_2x(self, print_string, do_wrap=True):
        """
        Write a line of double-size text at the current cursor co-ordinates

        Args:
            print_string (string) The text to print

        Returns:
            The display object
        """
        assert len(print_string) > 0, "ERROR - Zero-length string passed to text_2x()"
        return self._draw_text(print_string, do_wrap, True)

    def length_of_string(self, print_string):
        """
        Calculate the length in pixels of a proportionally spaced string

        Args:
            print_string (string) The text to print

        Returns:
            The string's length in pixels
        """
        length = 0
        if len(print_string) > 0:
            for i in range(0, len(print_string)):
                asc = ord(print_string[i]) - 32
                glyph = self.CHARSET[asc]
                length += (len(glyph) + 1)
        return length

    def clear(self):
        """
        Clears the display buffer by creating a new one

        Returns:
            The display object
        """
        for i in range(len(self.buffer)): self.buffer[i] = 0x00
        return self

    def draw(self):
        """
        Draw the current buffer contents on the screen
        """
        self._render()

    # ********** PRIVATE METHODS **********

    def _render(self):
        """
        Write the display buffer out to I2C
        """
        buffer = bytearray(len(self.buffer) + 1)
        buffer[1:] = self.buffer
        buffer[0] = self.SSD1306_WRITETOBUFFER
        self.i2c.writeto(self.address, bytes(buffer))

    def _coords_to_index(self, x, y):
        """
        Convert pixel co-ordinates to a bytearray index
        Calling function should check for valid co-ordinates first
        """
        return ((y >> 3) * self.width) + x

    def _index_to_coords(self, idx):
        """
        Convert bytearray index to pixel co-ordinates
        """
        y = idx >> 4
        x = idx - (y << 4)
        return (x, y)

    def _draw_text(self, the_string, do_wrap, do_double):
        """
        Generic text rendering routine
        """
        x = self.x
        y = self.y
        space_size = 4 if do_double else 1
        bit_max = 16 if do_double else 8

        for i in range(0, len(the_string)):
            glyph = self.CHARSET[ord(the_string[i]) - 32]
            col_0 = self._flip(glyph[0])

            if do_wrap:
                if x + len(glyph) * (2 if do_double else 1) >= self.width:
                    if y + bit_max < self.height:
                        x = 0
                        y += bit_max
                    else:
                        return self

            for j in range(1, len(glyph) + 1):
                if j == len(glyph):
                    if do_double: break
                    col_1 = self._flip(glyph[j - 1])
                else:
                    col_1 = self._flip(glyph[j])

                if do_double:
                    col_0_right = self._stretch(col_0)
                    col_0_left = col_0_right
                    col_1_right = self._stretch(col_1)
                    col_1_left = col_1_right

                    for a in range(6, -1, -1):
                        for b in range(1, 3):
                            if (col_0 >> a & 3 == 3 - b) and (col_1 >> a & 3 == b):
                                col_0_right |= (1 << ((a * 2) + b))
                                col_1_left |= (1 << ((a * 2) + 3 - b))

                z = (y - ((y >> 3) << 3)) - 1

                for k in range(0, bit_max):
                    if ((y + k) % 8) == 0 and k > 0:
                        z = 0
                    else:
                        z += 1

                    if do_double:
                        if x < self.width: self._char_plot(x, y, k, col_0_left, z)
                        if x + 1 < self.width: self._char_plot(x + 1, y, k, col_0_right, z)
                        if x + 2 < self.width: self._char_plot(x + 2, y, k, col_1_left, z)
                        if x + 3 < self.width: self._char_plot(x + 3, y, k, col_1_right, z)
                    else:
                        if x < self.width: self._char_plot(x, y, k, col_0, z)

                x += (2 if do_double else 1)
                if x >= self.width:
                    if not do_wrap: return self
                    if y + bit_max < self.height:
                        x = 0
                        y += bit_max
                    else:
                        break
                col_0 = col_1

            # Add spacer if we can
            if i < len(the_string) - 1:
                x += space_size
                if x >= self.width:
                    if not do_wrap: return self
                    if y + bit_max < self.height:
                        x = 0
                        y += bit_max
                    else:
                        break
        return self

    def _flip(self, value):
        """
        Rotates the character array from the saved state
        to that required by the screen orientation
        """
        flipped = 0
        for i in range (0, 8):
            if (value & (1 << i)) > 0:
                flipped += (1 << (7 - i))
        return flipped

    def _char_plot(self, x, y, k, c, a):
        """
        Write a pixel from a character glyph to the buffer
        """
        b = self._coords_to_index(x, y + k)
        if c & (1 << k) != 0: self.buffer[b] |= (1 << a)

    def _stretch(self, x):
        """
        Pixel-doubles an 8-bit value to 16 bits
        """
        x = (x & 0xF0) << 4 | (x & 0x0F)
        x = (x << 2 | x) & 0x3333
        x = (x << 1 | x) & 0x5555
        x = x | x << 1
        return x

    def _set_rst(self, is_on=True):
        """
        Select GPIO pin setting mechanism by Python type.

        Args:
            is_on (Bool) Are we toggling RST on?
        """
        if self.is_micropython:
            if is_on:
                self.rst.on()
            else:
                self.rst.off()
        else:
            self.rst.value = is_on
