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

import socket
import pickle
import readline

# import netifaces as ni

# def client():
HEADER = 64

print("______________________________________________________")
print("                                                ")
print("Pyserved CLI Client")
print("")
print("Enter the host and port in the fields below.")

# PORT = 5050

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!q"
# SERVER = "192.168.1.20"
# SERVER = socket.gethostbyname(socket.gethostname())
# host_name = socket.gethostname()
# SERVER = socket.gethostbyname(host_name + ".local")


def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


SERVER = get_internal_ip()
PORT = 5673
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)

    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    recv_msg = client.recv(100000000).decode(FORMAT)

    if recv_msg == "200":
        success = True
    else:
        success = False

    return success


"""

Socket DONE
main coding START

"""


def read(file):

    if file.endswith('.jpg'):
        f = open(file, 'r', encoding="ISO-8859-1", errors='ignore')
    else:
        f = open(file, 'r', encoding="utf8")

    text = f.read()
    f.close()

    # base64.b64decode(text)

    return file+"*-*/"+text

# file_path = input("File path: ")


def clientd(file_path):
    text = read(file_path)
    send(text)


print("Now enter the path of file which you want to send (UTF-8 only)")
path = input("File path:")
clientd(path)

print("")
print("______________________________________________________")
