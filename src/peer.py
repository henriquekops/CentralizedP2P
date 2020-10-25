#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import sys
from pprint import pprint
import socket
from socket import timeout
import threading

# project dependencies
from controllers.peer_controller import PeerController

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "25/10/2020"


def listen(peer_ip, peer_listen_port):
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.bind((peer_ip, int(peer_listen_port)))
    while True:
        try:
            listen_socket.settimeout(1)
            msg, client = listen_socket.recvfrom(1024)
            resource_data = open(msg, "rb")
            resource_data = resource_data.read(1024)
            listen_socket.sendto(resource_data, client)
        except timeout:
            pass


if __name__ == "__main__":

    peer_ip = sys.argv[1]
    peer_listen_port = sys.argv[2]
    peer_exchange_port = sys.argv[3]
    server_ip = sys.argv[4]
    resource = sys.argv[5]

    peer = PeerController(peer_ip, server_ip)

    pprint(peer.register_resource(resource).json())

    socket_a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_a.bind((peer_ip, int(peer_exchange_port)))

    t = threading.Thread(target=listen, args=(peer_ip, peer_listen_port))
    t.start()
    resource = ""

    while resource != "no":
        resource = input("resource to retrieve: ")
        peer_ips = peer.get_resource(resource).json()

        print(peer_ips)
        if peer_ips:
            socket_ip = peer_ips[0][0]
            socket_port = input("socket listen port: ")

            resource_file = open(resource + "_received.txt", "wb")
            socket_a.sendto(resource.encode("utf-8"), (socket_ip, int(socket_port)))
            resource_data, client = socket_a.recvfrom(1024)

            resource_file.write(resource_data)
        else:
            print("No IPs found for this resource")

    t.join()
