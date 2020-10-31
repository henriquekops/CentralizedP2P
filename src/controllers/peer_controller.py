#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import errno
import hashlib
import json
import os
import socket
import uuid

# external dependencies
import requests

# project dependencies
from threads.download_thread import PeerDownloadThread
from threads.heart_beat_thread import PeerHeartBeatThread

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class PeerController:
    """
    Controller for peer communication
    """

    def __init__(self, peer_ip: str, server_ip: str, peer_port: str, thread_port: str):
        self.server_ip = str(server_ip)

        self.peer_ip = str(peer_ip)
        self.peer_id = str(uuid.uuid4())

        self.thread_port = int(thread_port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((peer_ip, int(peer_port)))

        self.download_thread = PeerDownloadThread(self.peer_ip, self.thread_port)
        self.heartbeat_thread = PeerHeartBeatThread(self.peer_id, self.server_ip)

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

        hash_md5 = hashlib.md5()

        with open(resource_name, "rb") as r:
            for chunk in iter(lambda: r.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()

    def __upload(self, resource_path: str, resource_name: str) -> requests.Response:
        """
        Call server to register resource and assign to this peer

        :param resource_path: Provided resource's path
        :param resource_name: Resource provided by this peer
        :return: Central server's response
        """

        body = {
            "peer_id": self.peer_id,
            "peer_ip": self.peer_ip,
            "peer_port": self.thread_port,
            "resource_path": resource_path,
            "resource_name": resource_name,
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

    def __download(self, resource_name: str) -> requests.Response:
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

    def upload(self, resource: str) -> str:
        """
        Uploads a local resource

        :param resource: Local resource name to be published
        :return: Central server's response
        """

        try:
            resource_path = os.path.dirname(resource)
            resource_name = os.path.basename(resource)
            return f"uploaded: {self.__upload(resource_path, resource_name).json()}"
        except FileNotFoundError:
            return f"resource '{resource}' not found!"

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
            peer_resource_path = peers[0].get("resource_path")
            peer_resource_name = peers[0].get("resource_name")

            file = f"{peer_resource_path}/{peer_resource_name}".encode("utf-8")

            try:
                self.socket.settimeout(10)
                self.socket.sendto(file, (peer_ip, peer_port))
                resource_data, client = self.socket.recvfrom(1024)

            except socket.timeout:
                return f"it looks like peer '{peer_ip}:{peer_port}' is not responding, interrupting connection!"

            file_path = f"downloads/{peer_ip}_{resource_name}"
            resource_file = open(file_path, "wb")
            resource_file.write(resource_data)

            return f"resource '{resource_name}' downloaded at path '{file_path}'!"

        else:
            return f"no peers found for resource '{resource_name}'!"
