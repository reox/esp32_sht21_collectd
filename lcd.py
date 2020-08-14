# HD44780 class for micropython board (http://micropython.org)
# Written by Will Pimblett, based on http://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/
# http://github.com/wjdp/micropython-lcd
# http://wjdp.co.uk

import machine
import time

class HD44780(object):
    # Pinout, change within or outside class for your use case
    PINS = [23, 19, 18, 4, 16, 17]
    # Pin names, don't change
    PIN_NAMES = ['RS','E','D4','D5','D6','D7']

    # Pin mode, push-pull control
    PIN_MODE = machine.Pin.OUT

    # Define some device constants
    LCD_WIDTH = 16    # Maximum characters per line
    # Designation of T/F for character and command modes
    LCD_CHR = 1
    LCD_CMD = 0

    LINES = {
        # DDRAM_ADDRESS_CMD = 0x80
        0: 0x80, # LCD RAM address for the 1st line
        1: 0xc0, # LCD RAM address for the 2nd line
        # Add more if desired
    }

    # Timing constants
    E_PULSE = 1
    E_DELAY = 50

    def __init__(self):
        # Initialise pins
        for pin, pin_name in zip(self.PINS, self.PIN_NAMES):
            setattr(self, 'LCD_'+pin_name, machine.Pin(pin, self.PIN_MODE))

        self._lcd_nibble(0b0011, self.LCD_CMD)  # normal 8 bit..
        self.udelay(38)

        # Switch to 4 bit mode, set functions
        self.lcd_byte(0b00101000, self.LCD_CMD)

        # display control
        self.lcd_byte(0b00001100, self.LCD_CMD)

        # blank
        self.lcd_byte(1, self.LCD_CMD)
        self.udelay(1600)
        # entry mode set
        self.lcd_byte(0b00000110, self.LCD_CMD)
        self.udelay(38)

        self.lcd_byte(0xFF, self.LCD_CHR)
        self.lcd_byte(0b00110000, self.LCD_CHR)
        self.lcd_byte(0b00110001, self.LCD_CHR)

        for x in range(0, 10):
            self.lcd_byte(0b00110000 + x, self.LCD_CHR)

    def clear(self):
        # Clear the display
        self.lcd_byte(0x01,self.LCD_CMD)

    def set_line(self, line):
        # Set the line that we're going to print to
        self.lcd_byte(self.LINES[line], self.LCD_CMD)

    def set_string(self, message):
        # Pad string out to LCD_WIDTH
        # message = message.ljust(LCD_WIDTH," ")
        m_length = len(message)
        if m_length < self.LCD_WIDTH:
            short = self.LCD_WIDTH - m_length
            blanks=str()
            for i in range(short):
                blanks+=' '
            message+=blanks
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data
        # High nibble first
        self._lcd_nibble(bits >> 4, mode)
        # Then low nibble
        self._lcd_nibble(bits, mode)

    def _lcd_nibble(self, bits, mode):
        # mode = True  for character
        #        False for command
        # Toggle 'Enable' pin
        self.LCD_E.value(0)

        self.LCD_RS.value(mode)  # RS
        self.LCD_D4.value(bits >> 0 & 1)
        self.LCD_D5.value(bits >> 1 & 1)
        self.LCD_D6.value(bits >> 2 & 1)
        self.LCD_D7.value(bits >> 3 & 1)

        self.LCD_E.value(1)
        self.udelay(self.E_PULSE)
        self.LCD_E.value(0)
        self.udelay(self.E_DELAY)

    def udelay(self, us):
        # Delay by us microseconds, set as function for portability
        time.sleep_us(us)
