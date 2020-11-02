#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines server's heart beat thread
"""

# built-in dependencies
import time
import typing

# project dependencies
from controllers.database.database import get_database_resource_table_controller
from threads.base import BaseThread

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "30/10/2020"


class ServerHeartBeatThread(BaseThread):
    """
    Server's heart beat thread
    """

    def __init__(self, peer_id: str, my_queue: typing.List, *args, **kwargs):
        super(ServerHeartBeatThread, self).__init__(*args, **kwargs)

        # arguments
        self.peer_id = peer_id
        self.my_queue = my_queue

        # database access
        self.db_access = get_database_resource_table_controller()

    def run(self) -> None:
        """
        Overrides the base thread's behaviour to check peer's heart beat
        """

        while not self.stop_event.is_set():
            if self.my_queue:
                # if heartbeat received at '/heartbeat' route from the monitored peer,
                # sleep until next
                self.my_queue.clear()
                time.sleep(7)

            else:
                # else drop peer data from database and inform central server appending '0'
                # to my queue
                self.db_access.drop_peer(self.peer_id)
                self.my_queue.append(0)
                break
