import machine
import time
import network

##LED ON/OFF
# led_pin = machine.Pin(2, machine.Pin.OUT)
# while True:
#     led_pin.value(1)
#     print("Turning on")
#     time.sleep(1)
#     led_pin.value(0)
#     print("Turning off")
#     time.sleep(1)

#test DRV8833
D4= 2
D2 = 4
D5 = 14
D6 = 12

AIN1 = machine.Pin(D4, machine.Pin.OUT)
AIN1.off()

AIN2 = machine.Pin(D2, machine.Pin.OUT)
AIN2.off()

BIN1 = machine.Pin(D6, machine.Pin.OUT)
BIN1.off()

BIN2 = machine.Pin(D5, machine.Pin.OUT)
BIN2.off()

def forward():
    AIN1.value(1)
    AIN2.value(0)
    print("forward...")

    time.sleep(5)


def reverse():
    AIN1.value(0)
    AIN2.value(1)
    print("reversed...")

    time.sleep(5)


def stop():
    AIN1.value(0)
    AIN2.value(0)
    BIN1.value(0)
    BIN2.value(0)
    print('stop...')

    time.sleep(2)


def left_forward():
    #forward
    AIN1.value(1)
    AIN2.value(0)

    #turn left
    BIN1.value(1)
    BIN2.value(0)
    print("left forward...")
    
    time.sleep(5)


def right_forward():
    #forward
    AIN1.value(0)
    AIN2.value(1)

    #turn right
    BIN1.value(0)
    BIN2.value(1)
    print("right forward...")

    time.sleep(5)


def left_reverse():
    #reverse
    AIN1.value(0)
    AIN2.value(1)

    #turn right
    BIN1.value(0)
    BIN2.value(1)
    print("left reverse...")

    time.sleep(5)

    
def right_reverse():
    #reverse
    AIN1.value(0)
    AIN2.value(1)

    #turn right
    BIN1.value(1)
    BIN2.value(0)
    print("right reverse...")

    time.sleep(5)
print('\n--- from main.py ---')
station = network.WLAN(network.STA_IF)
if station.isconnected() == True:
  print('Connected to WiFi!')
  print(station.ifconfig())  



# while True:
    # forward()
    # stop()
    # reverse()
    # stop()
    # left_forward()
    # stop()
    # right_forward()
    # stop()
    # left_reverse()
    # stop()
    # right_reverse()
    # stop()

print('(╯°□°)╯︵ ┻━┻')