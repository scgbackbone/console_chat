import socket
from _thread import *
import time

def rcving(socket):
    while True:
        data = socket.recv(2048)
        if not data:
            break
        data = data.decode("utf-8")
        print(data)
    socket.close()

def snding(socket):
    while True:
        w = input("=> ")
        if w == "quit":
            break
        w = w.encode("utf-8")
        socket.send(w)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("", 5559))
    except socket.error as e:
        print(str(e))

    start_new_thread(rcving, (s,))
    #start_new_thread(snding, (s,))
    alias = input()
    alias = alias.strip().upper()
    s.send(str.encode(alias))
    while True:
        w = input()
        if w == "quit":
            break
        w = alias + " ==>  " + w
        w = w.encode("utf-8")
        s.send(w)
    s.close()
