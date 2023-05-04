import machine
import time
import network
import socket

# test DRV8833
D4 = 2  # LED_pin
D3 = 0
D2 = 4
D5 = 14
D6 = 12

AIN1 = machine.Pin(D5, machine.Pin.OUT)
AIN1.off()

AIN2 = machine.Pin(D6, machine.Pin.OUT)
AIN2.off()

BIN1 = machine.Pin(D3, machine.Pin.OUT)
BIN1.off()

BIN2 = machine.Pin(D2, machine.Pin.OUT)
BIN2.off()

LED_pin = machine.Pin(D4, machine.Pin.OUT)

# note
# BOUT1 = MOTOR 2 -
# BOUT2 = MOTOR 2 +

# AOUT2 = MOTOR 1 -
# AOUT1 = MOTOR 1 +


def forward():
    AIN1.value(1)
    AIN2.value(0)
    print("going forward")
    time.sleep_ms(3000)

    AIN1.value(0)
    AIN2.value(0)
    BIN1.value(0)
    BIN2.value(0)
    print("forward done")


def reverse():
    AIN1.value(0)
    AIN2.value(1)
    print("going reversed...")
    time.sleep_ms(3000)

    AIN1.value(0)
    AIN2.value(0)
    BIN1.value(0)
    BIN2.value(0)
    print("reverse done")


def stop():
    # stop
    AIN1.value(0)
    AIN2.value(0)
    BIN1.value(0)
    BIN2.value(0)
    print("stop...")
    time.sleep(3)


def left_forward():
    AIN1.value(1)
    AIN2.value(0)
    BIN1.value(1)
    BIN2.value(0)
    print("going left forward")
    time.sleep_ms(3000)

    AIN1.value(0)
    AIN2.value(0)
    BIN1.value(0)
    BIN2.value(0)
    print("left done")


def right_forward():
    AIN1.value(1)
    AIN2.value(0)
    BIN1.value(0)
    BIN2.value(1)
    print("going right forward")
    time.sleep_ms(3000)

    AIN1.value(0)
    AIN2.value(0)
    BIN1.value(0)
    BIN2.value(0)
    print("right done")


print("\n--- from main.py ---")
station = network.WLAN(network.STA_IF)
if station.isconnected() == True:
    print("Connected to WiFi! yeah")
    print(station.ifconfig())
else:
    raise RuntimeError("network connection failed")

# set the IP address of the ESP
# ESP is server
status = station.ifconfig()
IP_ADDRESS = status[0]  # replace with a unique IP address on your network

# create a socket object
sock = socket.socket()

# bind the socket to the ESP's IP address and port
sock.bind((IP_ADDRESS, 58707))
# listen for incoming connections
sock.listen(1)
print("listening on address " + IP_ADDRESS)

# wait for a client to connect
conn, addr = sock.accept()
print("start sock.accept")

# loop forever
while True:
    command = conn.recv(1024).decode()
    print(f"receive command {command} from {addr}")
    if command == "push":
        forward()
        response = "forward processed successfully"
        conn.sendall(response.encode())

    elif command == "right":
        right_forward()
        response = "forward from right successfully"
        conn.sendall(response.encode())

    elif command == "left":
        left_forward()
        response = "forward from left successfully"
        conn.sendall(response.encode())

    elif command == "stop":
        stop()
        response = "stop processed successfully"
        conn.sendall(response.encode())

    elif command == "pull":
        reverse()
        response = "reverse processed successfully"
        conn.sendall(response.encode())

    else:
        stop()
        break

conn.close()
stop()
print("Connection Close!")
