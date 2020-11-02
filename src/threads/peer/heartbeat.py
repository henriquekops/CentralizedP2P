#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines peer's heart beat thread
"""

# built-in dependencies
import json
import queue
import time

# external dependencies
import requests

# project dependencies
from threads.base import BaseThread


__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "31/10/2020"


class PeerHeartBeatThread(BaseThread):
    """
    Peer's heart beat thread
    """

    def __init__(self, peer_id: str, server_ip: str, exceptions: queue.Queue, *args, **kwargs):
        super(PeerHeartBeatThread, self).__init__(*args, **kwargs)

        # arguments
        self.server_ip = server_ip
        self.peer_id = peer_id
        self.exceptions = exceptions

    def run(self) -> None:
        """
        Overrides the base thread's behaviour to consume a heartbeat route at central server
        """

        body = {
            "peer_id": self.peer_id
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            while not self.stop_event.is_set():
                requests.post(
                    f"http://{self.server_ip}:5000/heartbeat",
                    data=json.dumps(body),
                    headers=headers
                )
                time.sleep(5)

        except requests.exceptions.ConnectionError as err:
            self.exceptions.put_nowait(err)
