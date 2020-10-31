#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import sys

# project dependencies
from controllers.peer_controller import PeerController

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "25/10/2020"

if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage: python src/peer.py <peer_ip:ipv4> <server_ip:ipv4> <peer_port:int> <thread_port:int>")
        sys.exit(2)

    peer_ip = sys.argv[1]
    server_ip = sys.argv[2]
    peer_port = sys.argv[3]
    thread_port = sys.argv[4]

    print("peer running!")
    print("commands:\n\t-u <resource_name> = upload\n\t-d <resource_name> = download \n\t-q = quit")

    peer = PeerController(peer_ip, server_ip, peer_port, thread_port)

    commands = {
        "-u": peer.upload,
        "-d": peer.download,
    }

    try:
        peer.heartbeat_thread.start()
        peer.download_thread.start()

        while True:
            entry = input("> ")
            args = entry.split()

            if len(args) == 0:
                print("input [-q, -d <resource_name>, -u <resource_name>]")

            elif args[0] == "-q":
                print("bye...")
                break

            elif len(args) != 2 or args[0] not in commands.keys():
                print("input [-q, -d <resource_name>, -u <resource_name>]")

            else:
                print(commands.get(args[0])(args[1]))

    finally:
        peer.heartbeat_thread.stop()
        peer.download_thread.stop()

        peer.heartbeat_thread.join()
        peer.download_thread.join()
