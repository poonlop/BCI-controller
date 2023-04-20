import machine
import time
import network
import socket

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
  print('Connected to WiFi! yeah')
  print(station.ifconfig())  

# set the IP address of the ESP 
# ESP is server
status = station.ifconfig()
IP_ADDRESS = status[0]  # replace with a unique IP address on your network

# create a socket object
sock = socket.socket()

# bind the socket to the ESP's IP address and port
sock.bind((IP_ADDRESS, 80))
# listen for incoming connections
sock.listen(1)
print("listening on address " + IP_ADDRESS)

# wait for a client to connect
conn, addr = sock.accept()

# loop forever
while True:
    command = conn.recv(1024).decode()
    print(f'receive command {command} from {addr}')
    if command == 'forward' : 
        forward()
        response = 'forward processed successfully'
        conn.sendall(response.encode())
    elif command == 'right_forward' :
        right_forward()
        response = 'Command processed successfully'
        conn.sendall(response.encode())
    elif command == 'left_forward' :
        left_forward()
        response = 'Command processed successfully'
        conn.sendall(response.encode())
    elif command == 'stop' :
        stop()
        response = 'stop processed successfully'
        conn.sendall(response.encode())
    else: 
        break

conn.close()
print("Connection Close !!!")
   #  print(raw_request)


    # request_parts = raw_request.split()
    # http_method = request_parts[0]
    # request_url = request_parts[1]
    #print(request_url)
    # if request_url.find("/forward") != -1:
    #     # drive rc car forward
    #     # print("exceuting forward")
    #     forward()
    # elif request_url.find("/right_forward") != -1:
    #     right_forward()
    # elif request_url.find("/left_forward") != -1:
    #     left_forward()
    # else : 
    #     stop()
    # conn.close()
    # send a response to the client
    # conn.send("OK\n".encode("utf-8"))

# close the connection

# print('(╯°□°)╯︵ ┻━┻')



