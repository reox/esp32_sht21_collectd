import network
import config
import time
import machine

led = machine.Pin(5, machine.Pin.OUT)
# LED is off if value==1 and on if value==0
led.value(1)

for _ in range(5):
    led.value(0)
    time.sleep_ms(50)
    led.value(1)
    time.sleep_ms(50)

sta_if = network.WLAN(network.STA_IF)
