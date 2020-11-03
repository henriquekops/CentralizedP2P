#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines a peer's listen thread
"""

# built-in dependencies
import queue
import socket

# project dependencies
from threads.base import BaseThread


__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "31/10/2020"


class PeerListenSocketThread(BaseThread):
    """
    Peer's listen thread for socket communications
    """

    def __init__(self, peer_ip: str, listen_port: int, exceptions: queue.Queue, *args, **kwargs):
        super(PeerListenSocketThread, self).__init__(*args, **kwargs)

        # arguments
        self.peer_ip = peer_ip
        self.listen_port = listen_port
        self.exceptions = exceptions

        # sockets
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.peer_ip, int(self.listen_port)))

    def run(self) -> None:
        """
        Overrides the base thread's behaviour to send a local file content through UDP socket
        when a connection is received
        """

        try:
            while not self.stop_event.is_set():
                try:
                    # wait for connection with timeout (check for thread interruption)
                    self.socket.settimeout(1)
                    msg, client = self.socket.recvfrom(1024)

                    # open resource through received message
                    resource = open(msg, "rb").read(1024)

                    # send back to the caller
                    self.socket.sendto(resource, client)

                except socket.timeout:
                    pass

        except Exception as err:
            self.exceptions.put_nowait(err)

