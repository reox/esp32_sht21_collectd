import network
import config

sta_if = network.WLAN(network.STA_IF)


import network
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(config.essid, config.passphrase)
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())
