#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that starts a peer's CLI (peer's main thread)
"""

# built-in dependencies
import pprint
import sys

# project dependencies
from controllers.peer.peer import PeerController

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "25/10/2020"

if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage: python src/peer_rest.py <peer_ip:ipv4> <server_ip:ipv4> <peer_port:int> <thread_port:int>")
        sys.exit(2)

    peer_ip = sys.argv[1]
    server_ip = sys.argv[2]
    peer_port = int(sys.argv[3])
    thread_port = int(sys.argv[4])

    print("peer running!")
    print("commands:\n\t"
          "-u <resource_name> = upload\n\t"
          "-d <resource_name> = download\n\t"
          "-l = list all resources \n\t"
          "-q = quit")

    peer = PeerController(peer_ip, server_ip, peer_port, thread_port)

    # start heartbeat and socket listen threads
    peer.heartbeat_thread.start()
    peer.listen_thread.start()

    commands = ["-u", "-d", "-l"]

    try:
        # peer's CLI loop
        while True:
            entry = input("> ")

            if entry == "-q":
                print("bye...")
                break

            if not peer.thread_exceptions.empty():
                exception = peer.thread_exceptions.get_nowait()
                print(f'error: {exception}')
                sys.exit(2)

            args = entry.split()

            if len(args) == 0:
                print("input [-q, -l, -d <resource_name>, -u <resource_name>]")

            elif args[0] not in commands or len(args) > 2 or len(args) == 0:
                print("input [-q, -l, -d <resource_name>, -u <resource_name>]")

            elif args[0] == "-l":
                result = peer.list()
                pprint.pprint(result, indent=4)

            elif args[0] == "-d":
                print(peer.download(args[1]))

            elif args[0] == "-u":
                print(peer.upload(args[1]))

    finally:
        # stop heartbeat and socket listen threads
        peer.heartbeat_thread.stop()
        peer.listen_thread.stop()

        peer.heartbeat_thread.join()
        peer.listen_thread.join()
