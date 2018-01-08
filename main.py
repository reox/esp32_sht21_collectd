import machine
import sht21
import time
import collectd

# Start up I2C
i2c = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22), freq=400000)

sens = sht21.SHT21(i2c)

def sensesend(tmr):
    hum = sens.get_humd()
    tem = sens.get_temp()
    collectd.send_value("humidity", "Humidity", hum)
    collectd.send_value("temperature", "Temperature", tem)
    print("Temperature: {} °C, Humidity {} %RH".format(tem, hum))

timer = machine.Timer(4)

timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=sensesend)

