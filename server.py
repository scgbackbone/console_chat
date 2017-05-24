import sys
import socket
from _thread import *
from socket import error as SocketError
import time

import sys
print(sys.executable)
print(sys.version)

def gener_sender(conn, alias, aliases, peers, introsent=1, data=""):
    if introsent == 1:
        for x in peers:
            if len(peers) == 1:
                x.send(str.encode("You are the only connected peer yet.\nWaiting for connections..."))
                break
            if x == conn:
                connected_peers ="all connected peers {}".format(aliases)
                x.send(str.encode(connected_peers))
                continue
            connected_peers ="{} has just connected. ||| all connected peers {}".format(alias, aliases)
            x.send(str.encode(connected_peers))
            continue
    if introsent == 0:
        if command_checker(conn, data, alias, aliases) == True:
            pass
        else:
            for x in peers:
                if x == conn:
                    continue
                reply = str(time.ctime(time.time())) + ":: " + data
                x.sendall(str.encode(reply))
    if introsent == 2:
        for x in peers:
            if x == conn:
                continue
            else:
                message = "{} has left the chat".format(alias)
                x.send(str.encode(message))
                continue
                
def command_checker(conn, data, alias, aliases):
    if data == alias + " ==>  " + "$connP":
        connected_peers ="all connected peers {}".format(aliases)
        conn.send(str.encode(connected_peers))
        return True
    return False

def alias_grabber(connection):
    try:
        conn.send(str.encode("\nwelcome, type in your alias: "))
        data = connection.recv(1024)
        data = data.decode("utf-8")
        return str(data)
    except SocketError as e:
        print("ERROR")

def threaded_client(conn, addr, peers, aliases, alias, functionen):
    while True:
        try:
            data = conn.recv(2048)
            data = data.decode("utf-8")
            if not data:
                peers.remove(conn)
                aliases.remove(alias)
                break
            functionen(conn, alias, aliases, peers, introsent=0, data=data)
        except SocketError as e:
            print(e)
            print("ERROR")
    functionen(conn, alias, aliases, peers, introsent=2)
    conn.close()
    print("DISSCONNECT: client from: {}:{} left!".format(addr[0], addr[1]))
    if peers == []:
        print("No clients connected")
    else:
        print(peers)

if __name__ == "__main__":
    host = ""
    port = 5559

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peers = []
    peers_addr = []
    aliases = []
    functionen = gener_sender
    try:
        s.bind((host, port))
    except socket.error as e:
        print(str(e))

    s.listen(5)
    print("SERVER STARTED, status=listening...")
    # print(socket.gethostbyname(socket.gethostname()))
    # print(socket.gethostbyaddr(host))

    while True:
        conn, addr = s.accept()
        print("connected to: " + addr[0] + ":" + str(addr[1]))
        peers.append(conn)
        print("number of connected peers = {}".format(len(peers)))
        peers_addr.append(addr)
        alias = alias_grabber(conn)
        aliases.append(alias)
        print("connected peers {}".format(aliases))
        gener_sender(conn, alias, aliases, peers, introsent=1)

        start_new_thread(threaded_client, (conn, addr, peers, aliases, alias, functionen))
