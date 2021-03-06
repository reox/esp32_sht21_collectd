super cheap collectd interface for SHT21 temperature / humidity sensor, running
on an ESP32 micropython enabled board.
Because SHT21 can not measure air pressure, a Bosch BMP280 was added to get that
value. However, as it can also measure temperature, you will get that value
twice.

As an addition, a SH1106 based OLED was added to print out the measurements.

The LOLIN32 board I used has no direct way of measuring the battery level.
What you can do though is to add a resistor divider between the ADC and the
battery and measure the voltage. Or better: get a decent board which allows for
that directly.

**NOTE** that this is rather a pile of breadboard based test scripts than a
finished project ;)

![Projekt](board_small.jpg)


config.py
=========

should look like this:

```
essid = "<your essid>"
passphrase = "<your passphrase>"

host = "Hostname_that_has_NTP_and_Collectd"
hostname = "hostname of this device"
```

Wiring
======

Attach GND, SDA, SCL, VCC from the ESP32 board to the two sensors.


MicroPython
===========

tested with

```
esp32-20181110-v1.9.4-683-gd94aa577a.bin
```

