import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# oncomputer is client
# get the IP address of the ESP
host = "172.20.10.2"  # replace with your ESP's IP address
    
# set the port number
port = 80
    
# connect to the ESP
s.connect((host, port))

# send the command
#1. receive from cortex
#2. create command
file_name = 'test2.json'
file = open(str(file_name),'r')
data = file.readlines()
# command=''
# You can modify for proper command
command = ''
for x in data :
#convert to dictionary format using json.loads()
    x = json.loads(x.replace("'", '"'))
    if x['action'] == 'push' and  x['power'] > 0.5:
        command = 'forward'
        s.sendall(command.encode())
        print(f'Sent command: {command}')
        response = s.recv(1024).decode()
        print(response)
    elif x['action'] == 'right' and  x['power'] > 0.5:
        command = 'right_forward'
        s.sendall(command.encode())
        print(f'Sent command: {command}')
        response = s.recv(1024).decode()
        print(response) 
    elif x['action'] == 'left' and  x['power'] > 0.5: 
        command = 'left_forward'
        s.sendall(command.encode())
        print(f'Sent command: {command}')
        response = s.recv(1024).decode()
        print(response) 
    elif x['action'] == 'neutral' : 
        command = 'stop'
        s.sendall(command.encode())
        print(f'Sent command: {command}') 
        response = s.recv(1024).decode()
        print(response)

s.close()

