import machine
import sht21
import bmp280
import time
import collectd
import uos

# Start up I2C
i2c = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22), freq=400000)

sens = sht21.SHT21(i2c)
bmp = bmp280.BMP280(i2c=i2c)

adc = machine.ADC(machine.Pin(35))


led = machine.Pin(5, machine.Pin.OUT)
led.value(1)


def send_df():
    f_bsize, f_frsize, f_blocks, f_bfree, f_bavail, f_files, f_ffree, f_favail, f_flag, f_namemax = uos.statvfs("/")

    collectd.send_value("df_complex", "free", f_bavail * f_bsize, plugin="df", plugin_instance="root")
    collectd.send_value("df_complex", "used", (f_blocks - f_bavail) * f_bsize, plugin="df", plugin_instance="root")
    collectd.send_value("df_complex", "reserved", (f_bfree - f_bavail) * f_bsize, plugin="df", plugin_instance="root")

def send_mem():
    collectd.send_value("memory", "free", gc.mem_free(),  plugin="memory", plugin_instance=None)
    collectd.send_value("memory", "used", gc.mem_alloc(),  plugin="memory", plugin_instance=None)


def sensesend(tmr):
    # For debugging, blink the LED...
    led.value(0)

    hum = sens.get_humd()
    tem = sens.get_temp()

    tem_bmp, pres_bmp = bmp.values

    bat = (105 + 27) * 1.1 / (27 * 2**12) * adc.read()
    collectd.send_value("humidity", "Humidity", hum)
    collectd.send_value("temperature", "Temperature", tem)
    collectd.send_value("temperature", "Temperature BMP280", tem_bmp)
    collectd.send_value("pressure", "Pressure statniv.", pres_bmp)
    collectd.send_value("voltage", "V_Bat", bat)

    send_df()
    send_mem()

    print("Temperature: {} / {} °C, Humidity: {} %RH, Air pressure: {}hPa, battery: {}".format(tem, tem_bmp, hum, pres_bmp, bat))
    led.value(1)

timer = machine.Timer(4)

timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=sensesend)

