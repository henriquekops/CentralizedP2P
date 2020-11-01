#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import time
import typing

# project dependencies
from controllers.database import get_database_resource_table_controller
from threads.base import BaseThread

db_access = get_database_resource_table_controller()


class ServerHeartBeatThread(BaseThread):
    """
    Server's heart beat thread
    """

    def __init__(self, peer_id: str, my_queue: typing.List, *args, **kwargs):
        super(ServerHeartBeatThread, self).__init__(*args, **kwargs)

        self.peer_id = peer_id
        self.my_queue = my_queue

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
                db_access.drop_peer(self.peer_id)
                self.my_queue.append(0)
                break
