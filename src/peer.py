#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
from pprint import pprint
import socket
from socket import timeout
import sys
import threading

# project dependencies
from controllers.peer_controller import PeerController

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "25/10/2020"


class PeerThread(threading.Thread):

    def __init__(self, peer_ip, peer_port, *args, **kwargs):
        super(PeerThread, self).__init__(*args, **kwargs)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((peer_ip, int(peer_port)))
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            try:
                self.socket.settimeout(1)
                msg, client = self.socket.recvfrom(1024)
                resource = open(msg, "rb")
                resource_data = resource.read(1024)
                self.socket.sendto(resource_data, client)
            except timeout:
                pass

    def stop(self):
        self._stop_event.set()


class Peer:

    def __init__(self, peer_ip, server_ip, peer_port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((peer_ip, int(peer_port)))
        self.controller = PeerController(peer_ip, server_ip)

    def upload(self, resource_name):
        pprint(self.controller.register_resource(resource_name).json())

    def download(self, resource_name):
        peer_ips = self.controller.get_resource(resource_name).json()

        if peer_ips:
            socket_ip = peer_ips[0][0]
            socket_port = input("socket listen port: ")

            resource_file = open(resource_name + "_received.txt", "wb")
            self.socket.sendto(resource_name.encode("utf-8"), (socket_ip, int(socket_port)))
            resource_data, client = self.socket.recvfrom(1024)

            resource_file.write(resource_data)
        else:
            print(f"no IPs found for resource {resource_name}!")


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage: python src/peer.py <peer_ip> <server_ip> <peer_port> <thread_port>")
        sys.exit(2)

    peer_ip = sys.argv[1]
    server_ip = sys.argv[2]
    peer_port = sys.argv[3]
    thread_port = sys.argv[4]

    peer = Peer(peer_ip, server_ip, peer_port)
    thread = PeerThread(peer_ip, thread_port)
    thread.start()

    print("peer running!\n'-q' to quit...")
    print("commands:\n\t-u = upload\n\t-d = download")

    commands = {
        "-u": peer.upload,
        "-d": peer.download
    }

    while True:
        entry = input("input: ")
        if entry == "-q":
            break
        resource_name = input("resource name: ")
        commands.get(entry)(resource_name)

    thread.stop()
    thread.join()
