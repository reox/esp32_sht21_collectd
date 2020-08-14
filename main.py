import machine
import sht21
import bmp280
import time
import collectd
import uos
import weather
import sh1106

# Start up I2C
i2c = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22), freq=400000)

sens = sht21.SHT21(i2c)
bmp = bmp280.BMP280(i2c=i2c)
adc = machine.ADC(machine.Pin(35))

disp = sh1106.SH1106_I2C(128, 64, i2c)

led = machine.Pin(5, machine.Pin.OUT)
led.value(1)

disp.init_display()
disp.invert(False)
disp.rotate(True)
disp.fill(0)
disp.show()

send_adc = False
send_collectd = False


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

    if send_collectd:
        collectd.send_value("humidity", "Humidity", hum)
        collectd.send_value("temperature", "Temperature", tem)
        collectd.send_value("temperature", "Temperature BMP280", tem_bmp)
        collectd.send_value("pressure", "Pressure statniv.", pres_bmp)
        ## Actually this is quite wrong, when we use the indoor value...
        ## Weather measurements are hard ;)
        # collectd.send_value("pressure", "Pressure red.", weather.reduced_pressure(pres_bmp, tem_bmp, hum))

        # send_df()
        # send_mem()

    bat = 0
    if send_adc:
        bat = (105 + 27) * 1.1 / (27 * 2**12) * adc.read()
        if send_collectd:
            collectd.send_value("voltage", "V_Bat", bat)


    print("Temperature: {} / {} °C, Humidity: {} %RH, Air pressure: {}hPa, battery: {}".format(tem, tem_bmp, hum, pres_bmp, bat))

    disp.fill(0)
    disp.text("{:=6.1f} °C".format(tem), 8, 10, 1)
    disp.text("{:=6.1f} %RH".format(hum), 8, 20, 1)
    disp.text("{:=6.1f} hPa".format(pres_bmp), 8, 30, 1)

    if sta_if.isconnected():
        disp.text(sta_if.ifconfig()[0], 8, 56, 1)
    else:
        disp.text("WLAN NC", 8, 56, 1)
    disp.show()

    led.value(1)

timer = machine.Timer(4)
timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=sensesend)

