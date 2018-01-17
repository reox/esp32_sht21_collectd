import network
import config
import time
import machine

led = machine.Pin(5, machine.Pin.OUT)
led.value(1)

for _ in range(5):
    led.value(0)
    time.sleep_ms(50)
    led.value(1)
    time.sleep_ms(50)


import network
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(config.essid, config.passphrase)
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())
