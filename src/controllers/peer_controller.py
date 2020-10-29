#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import errno
from hashlib import md5
import json
import os
import socket
from socket import timeout
from threading import (
    Thread,
    Event
)

from uuid import uuid4

# external dependencies
import requests
from requests import Response

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class PeerController:
    """
    Controller for peer communication
    """

    def __init__(self, peer_ip: str, server_ip: str, peer_port: str, thread_port: str):
        self.server_ip = server_ip
        self.peer_ip = peer_ip
        self.thread_port = int(thread_port)
        self.peer_id = str(uuid4())

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((peer_ip, int(peer_port)))

        self.download_thread = PeerDownloadThread(peer_ip, thread_port)
        self.__create_downloads_dir()

    @staticmethod
    def __create_downloads_dir() -> None:
        if not os.path.exists(os.path.dirname("downloads/")):
            try:
                os.makedirs(os.path.dirname("downloads/"))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    @staticmethod
    def __generate_hash(resource_name: str) -> str:
        """
        Generates a MD5 hash over resource's content

        :param resource_name: Resource provided by this peer
        :return: MD5 hash over resource's content
        """

        hash_md5 = md5()

        with open(resource_name, "rb") as r:
            for chunk in iter(lambda: r.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()

    def __upload(self, resource_name: str) -> Response:
        """
        Call server to register resource and assign to this peer

        :param resource_name: Resource provided by this peer
        :return: Central server's response
        """

        body = {
            "peer_id": self.peer_id,
            "peer_ip": self.peer_ip,
            "peer_port": self.thread_port,
            "resource_name": os.path.basename(resource_name),
            "resource_hash": self.__generate_hash(resource_name)
        }
        header = {
            "content-type": "application/json; charset=utf-8"
        }
        return requests.post(
            f"http://{self.server_ip}:5000/resource",
            data=json.dumps(body),
            headers=header
        )

    def __download(self, resource_name: str) -> Response:
        """
        Call server to search peer ips that contains this resource

        :param resource_name: Resource provided by this peer
        :return: Central server's response
        """

        body = {
            "resource_name": resource_name
        }
        header = {
            "content-type": "application/json; charset=utf-8"
        }
        return requests.get(
            f"http://{self.server_ip}:5000/resource",
            data=json.dumps(body),
            headers=header
        )

    def upload(self, resource_name: str) -> str:
        """
        Uploads a local resource

        :param resource_name: Local resource name to be published
        :return: Central server's response
        """

        return self.__upload(resource_name).json()

    def download(self, resource_name) -> str:
        """
        Downloads a resource

        :param resource_name: Name of the desired resource
        :return String identifying the operation's success
        """

        peers = json.loads(self.__download(resource_name).json())

        if peers:
            peer_ip = peers[0].get("peer_ip")
            peer_port = peers[0].get("peer_port")

            try:
                self.socket.settimeout(10)
                self.socket.sendto(resource_name.encode("utf-8"), (peer_ip, peer_port))
                resource_data, client = self.socket.recvfrom(1024)
            except timeout:
                return f"it looks like peer {peer_ip}:{peer_port} is not responding, interrupting connection!"

            file_path = f"downloads/{peer_ip}_{resource_name}"
            resource_file = open(file_path, "wb")
            resource_file.write(resource_data)
            return f"resource '{resource_name}' downloaded at path '{file_path}'!"

        else:
            return f"no peers found for resource '{resource_name}'!"


class PeerDownloadThread(Thread):
    """
    Peer thread for local file download
    """

    def __init__(self, peer_ip, peer_port, *args, **kwargs):
        super(PeerDownloadThread, self).__init__(*args, **kwargs)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((peer_ip, int(peer_port)))
        self._stop_event = Event()

    def run(self) -> None:
        """
        Overrides the default thread's behaviour to
        send a local file content through UDP socket
        """

        while not self._stop_event.is_set():
            try:
                self.socket.settimeout(1)
                msg, client = self.socket.recvfrom(1024)
                resource = open(msg, "rb")
                resource_data = resource.read(1024)
                self.socket.sendto(resource_data, client)
            except timeout:
                pass

    def stop(self) -> None:
        """
        Kills the running
        """

        self._stop_event.set()
