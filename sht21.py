import time
class SHT21:
    address = 0x40

    cmd_measure_temp = b'\xf3'
    cmd_measure_humd = b'\xf5'
    cmd_reset = b'\xfe'

    def __init__(self, i2c):
        self.i2c = i2c

        self.soft_reset()
        # Should not take longer than 15ms, but we wait a little bit longer
        time.sleep_ms(50)

    def soft_reset(self):
        self._command(self.cmd_reset)

    def get_temp(self):
        return (-46.85 + 175.72 / 65536.0 * self._command(self.cmd_measure_temp))

    def get_humd(self):
        return (-6.0 + 125.0 / 65536.0 * self._command(self.cmd_measure_humd))

    def _command(self, cmd):
        self.i2c.writeto(self.address, cmd)

        # Poll after 100ms
        time.sleep_ms(100)

        buf = self.i2c.readfrom(self.address, 2)

        return ((buf[0] << 8) | buf[1]) & 0xFFFC

