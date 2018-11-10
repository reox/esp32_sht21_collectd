super cheap collectd interface for SHT21 temperature / humidity sensor, running
on an ESP32 micropython enabled board.


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

