#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import socket

# project dependencies
from threads.base_thread import BaseThread


__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "31/10/2020"


class PeerDownloadThread(BaseThread):
    """
    Peer thread for local file download
    """

    def __init__(self, peer_ip: str, peer_port: int, *args, **kwargs):
        super(PeerDownloadThread, self).__init__(*args, **kwargs)

        self.peer_ip = peer_ip
        self.peer_port = peer_port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.peer_ip, int(self.peer_port)))

    def run(self) -> None:
        """
        Overrides the default thread's behaviour to
        send a local file content through UDP socket
        """

        while not self.stop_event.is_set():
            try:
                self.socket.settimeout(1)
                msg, client = self.socket.recvfrom(1024)
                resource = open(msg, "rb").read(1024)
                self.socket.sendto(resource, client)
            except socket.timeout:
                pass
