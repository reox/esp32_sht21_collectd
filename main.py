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
disp.fill(1)
disp.show()
time.sleep_ms(200)
disp.fill(0)
disp.show()

send_adc = False
send_collectd = False


# The display has a height of 64 pixel
# Chars are 8x8 and it does not require a pixel space between.
LINES = {i + 1: i * 8 for i in range(8)}



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

    # Text in Framebuffer has size 8x8 per character and the coordinate is at the top left corner.
    # Argument: s, x, y, [c] (color is 1 by default)
    # The framebuf font in micropython is font_petme128_8x8.h.
    # Unfortunately, it only supports chars between 0x20 (space) and 0x7f. ° is 0xb0
    #
    # 128x64 pixel --> 16x8 chars
    disp.textline("{:=6.1f} C".format(tem), 0)
    disp.textline("{:=6.1f} %RH".format(hum), 1)
    disp.textline("{:=6.1f} hPa (st)".format(pres_bmp), 2)
    disp.textline("{:=6.1f} hPa (rd)".format(weather.reduced_pressure(pres_bmp, tem_bmp, hum)), 3)
    disp.textline("{:=6.1f} V".format(bat), 4)
    disp.show()

    led.value(1)


WIFI_MESSAGE = {
    network.STAT_IDLE:           "idle",
    network.STAT_CONNECTING:     "connecting",
    network.STAT_WRONG_PASSWORD: "wrong pw",
    network.STAT_NO_AP_FOUND:    "no AP found",
    network.STAT_GOT_IP:         "connected"
}

def wifistate(tmr):
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(config.essid, config.passphrase)
        print('network config:', sta_if.ifconfig())
    state = sta_if.status()
    if state not in WIFI_MESSAGE:
        statestr = 'state {}'.format(state)
    else:
        statestr = WIFI_MESSAGE[state]
    disp.textline(statestr, 6)
    disp.textline(sta_if.ifconfig()[0], 7)
    disp.show()


sensesend(None)
timer = machine.Timer(4)
timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=sensesend)

wifistate(None)
timer = machine.Timer(3)
timer.init(period=60000, mode=machine.Timer.PERIODIC, callback=wifistate)

