#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines base implementation for all project's threads
"""

# built-in dependencies
import threading

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "31/10/2020"


class BaseThread(threading.Thread):
    """
    Base thread implementation
    """

    def __init__(self, *args, **kwargs):
        super(BaseThread, self).__init__(*args, **kwargs)

        self.stop_event = threading.Event()

    def stop(self) -> None:
        """
        Kills this thread
        """

        self.stop_event.set()
