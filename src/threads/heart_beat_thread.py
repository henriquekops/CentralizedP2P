#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import json
import time
import typing

# external dependencies
import requests

# project dependencies
from controllers.database_controller import DatabaseResourceTableController
from threads.base_thread import BaseThread


__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "31/10/2020"


class PeerHeartBeatThread(BaseThread):
    """
    Peer's heart beat thread
    """

    def __init__(self, peer_id, server_ip, *args, **kwargs):
        super(PeerHeartBeatThread, self).__init__(*args, **kwargs)

        self.server_ip = server_ip
        self.peer_id = peer_id

    def run(self) -> None:
        """
        Overrides the default thread's behaviour to
        consume a heartbeat route at central server
        """

        body = {
            "peer_id": self.peer_id
        }
        headers = {
            "Content-Type": "application/json"
        }

        while not self.stop_event.is_set():
            requests.post(
                f"http://{self.server_ip}:5000/heartbeat",
                data=json.dumps(body),
                headers=headers
            )
            time.sleep(5)


class ServerHeartBeatThread(BaseThread):
    """
    Server's heart beat thread
    """

    def __init__(self, peer_id: str, my_queue: typing.List,
                 db_access: DatabaseResourceTableController, *args, **kwargs):
        super(ServerHeartBeatThread, self).__init__(*args, **kwargs)

        self.peer_id = peer_id
        self.my_queue = my_queue
        self.db_access = db_access

    def run(self) -> None:
        """
        Overrides the default thread's behaviour to
        check peer's heart beat
        """

        while not self.stop_event.is_set():
            if self.my_queue:
                self.my_queue.clear()
                time.sleep(7)
            else:
                self.db_access.drop_peer(self.peer_id)
                self.my_queue.append(0)
                break



