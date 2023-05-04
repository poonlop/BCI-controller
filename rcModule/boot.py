import utime
import network

ssid = "poonL."
password = "20010728"

print("set ssid password")

# set Wi-Fi to station interface
wlan = network.WLAN(network.STA_IF)
# activate the network interface
wlan.active(True)
# connect to Wi-Fi network
wlan.connect(ssid, password)

print("waiting for connection start")

# wait for connection
max_wait = 10
while max_wait > 0:
    """
    0   STAT_IDLE -- no connection and no activity,
    1   STAT_CONNECTING -- connecting in progress,
    2  STAT_WRONG_PASSWORD -- failed due to incorrect password,
    3  STAT_NO_AP_FOUND -- failed because no access point replied,
    4  STAT_CONNECT_FAIL -- failed due to other problems,
    5   STAT_GOT_IP -- connection successful.
    """
    if wlan.status() <= 0 or wlan.status() >= 5:
        # connection successful
        break
    max_wait -= 1
    print("waiting for connection... " + str(max_wait))
    utime.sleep(1)

# check connection
if wlan.status() != 5:
    # No connection
    raise RuntimeError("network connection failed")
else:
    # connection successful
    print("wlan connected")
    status = wlan.ifconfig()
    print("IP address = " + status[0])
    print("subnet mask = " + status[1])
    print("gateway  = " + status[2])
    print("DNS server = " + status[3])
