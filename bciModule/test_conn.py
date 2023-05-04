import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "172.20.10.8"  # replace with your ESP's IP address

port = 58707

s.connect((host, port))


def send_command(command):
    s.sendall(command.encode())
    print(f"Send Command {command}")
    response = s.recv(1024).decode()
    print(response)


def main():
    while True:
        send_command("push")
        time.sleep(3)
        send_command("stop")
        time.sleep(3)
        send_command("left")
        time.sleep(3)
        send_command("stop")
        time.sleep(3)
        send_command("right")
        time.sleep(3)
        send_command("stop")
        time.sleep(3)


main()
