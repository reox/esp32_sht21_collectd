import machine
import sht21
import time
import collectd
import uos

# Start up I2C
i2c = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22), freq=400000)

sens = sht21.SHT21(i2c)

adc = machine.ADC(machine.Pin(35))


def send_df():
    f_bsize, f_frsize, f_blocks, f_bfree, f_bavail, f_files, f_ffree, f_favail, f_flag, f_namemax = uos.statvfs("/")

    collectd.send_value("df_complex", "free", f_bavail * f_bsize, plugin="df", plugin_instance="root")
    collectd.send_value("df_complex", "used", (f_blocks - f_bavail) * f_bsize, plugin="df", plugin_instance="root")
    collectd.send_value("df_complex", "reserved", (f_bfree - f_bavail) * f_bsize, plugin="df", plugin_instance="root")


def sensesend(tmr):
    hum = sens.get_humd()
    tem = sens.get_temp()
    bat = (105 + 27) * 1.1 / (27 * 2**12) * adc.read()
    collectd.send_value("humidity", "Humidity", hum)
    collectd.send_value("temperature", "Temperature", tem)
    collectd.send_value("voltage", "V_Bat", bat)

    send_df()

    print("Temperature: {} °C, Humidity: {} %RH, battery: {}".format(tem, hum, bat))

timer = machine.Timer(4)

timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=sensesend)

