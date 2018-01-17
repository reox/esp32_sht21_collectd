import socket
import struct
from config import host, hostname


# https://stackoverflow.com/a/29138806/446140
NTP_DELTA = 2208988800

def getntptime():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA


def _pack_str(t, s):
    return struct.pack("!HH{}ss".format(len(s)), t, len(s) + 5, s, '\x00')


def send_value(plug_type, plug_inst, value, plugin="sensors", plugin_instance="0"):
    package = b""
    # Host
    package += _pack_str(0x0000, hostname)
    # Time
    package += struct.pack("!HHQ", 0x0001, 12, getntptime())
    # Plugin
    package += _pack_str(0x0002, plugin)
    # Plugin instance
    package += _pack_str(0x0003, plugin_instance)
    # Type
    package += _pack_str(0x0004, plug_type)
    # Type instance
    package += _pack_str(0x0005, plug_inst)

    # Interval
    package += struct.pack("!HHQ", 0x0007, 12, 10)

    # Value
    package += struct.pack("!HHHB", 0x0006, 15, 1, 1) + struct.pack("<d", value)


    addr = socket.getaddrinfo(host, 25826)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(package, addr)
    s.close()

if __name__ == "__main__":
    import time
    for i in range(100):
        send_value("temperature", 23.222 + i)
        time.sleep(2)

