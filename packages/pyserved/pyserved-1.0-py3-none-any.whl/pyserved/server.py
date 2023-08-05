"""
________________________________
|                              |
| pyserved                     |
|                              |
| Only works with utf-8        |
| files. (for now.)            |
|                              |
| By:                          |
| Shaurya Pratap Singh         |
| 2021 ©                       |
|______________________________|
"""


# import base64
import readline
import platform
import pathlib
import socket
import threading
import os
import getpass
import random
import errno
# import netifaces as ni

# TODO: Need to have support for files in next version

username = getpass.getuser()


def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


class OSNotRecognized(Exception):
    pass


osofmachine = platform.system().lower()

if osofmachine == "windows":
    SAVE_DIR = r"C:\Users\{username}\pyserved".format(username=username)
elif osofmachine == "darwin":
    SAVE_DIR = f"/Users/{username}/pyserved"
elif osofmachine == "linux":
    SAVE_DIR = f"/Users/{username}/pyserved"
else:
    raise OSNotRecognized(
        "This OS can't be used, sorry amigo. (Future support for all linux distros will be added by 15/8/2021)"
    )

    # SAVE_DIR = f'/Users/{username}/pyserved'


def make_dir():
    pathlib.Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)


make_dir()

random_num = random.randint(1000, 9999)
name = f"copiedfile{random_num}"

# # ni.ifaddresses('eth0')
print("______________________________________________________")
print("")
# if osofmachine == 'darwin' or osofmachine == 'linux':
#     print("You can find out the ip address by typing\n \n $ ifconfig en1 \n\n or \n\n $ ifconfig en0\n\n or you can search google for it.\n\n")
# elif osofmachine == "windows":
#     print("You can find out the ip address by using \n \n $ ipconfig \n\n")
# else:
#     pass

host_name = socket.gethostname()
host_addr = socket.gethostbyname(host_name)

SERVER = get_internal_ip()

# SERVER = socket.gethostbyname(socket.getfqdn())

clients = []
HEADER = 64
PORT = 5673
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!q"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr[0]}:{addr[1]} connected")

    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            # print(msg_length)
            msg_length = float(msg_length)
            msg = conn.recv(100000000).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[{addr[0]}:{addr[1]}] has disconnected")
                conn.send("You have been disconnected".encode(FORMAT))

            print(f"[{addr[0]}:{addr[1]}] Sent a file to {SERVER}:{PORT}")

            # print()

            filetype = msg.split("*-*/")[0].split(".")[1]
            content = msg.split("*-*/")[1]
            if osofmachine == 'windows':
                f = open(f'{SAVE_DIR}\{name}.{filetype}', 'w+')
                SAVE_DIR_XYZ = f'{SAVE_DIR}\{name}.{filetype}'
                f.write(content)
                f.close()
            else:
                f = open(f'{SAVE_DIR}/{name}.{filetype}', 'w+')
                SAVE_DIR_XYZ = f'{SAVE_DIR}/{name}.{filetype}'
                f.write(content)
                f.close()

            print(f"[{addr[0]}:{addr[1]}] File has been saved on {SAVE_DIR_XYZ}")
            conn.send("200".encode(FORMAT))

    conn.close()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        clients.append((conn, addr))
        # print(clients)
        # print(f"[NEW CONNECTION] Client with ip {addr[0]}:{addr[1]} has connected to your server.")

        if threading.activeCount() - 1 > 3:
            print("[ERROR] More than 2 clients are not allowed.")
            # raise Exception("There cant be more than tw")

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def startserver():
    print(f"[STARTING] SERVER is starting on {str(SERVER)}:{str(PORT)}")
    print(f"[RUNNING] Server is succesfully running....")
    print(
        f"[RUNNING] The files which will be sent to you will be saved on {SAVE_DIR} directory.")
    start()


print("______________________________________________________")
startserver()
