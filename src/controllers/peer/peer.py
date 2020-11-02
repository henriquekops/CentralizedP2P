#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines a controller for peer's operations
"""

# built-in dependencies
import errno
import hashlib
import json
import os
import queue
import socket
import uuid

# project dependencies
from controllers.peer.peer_rest import PeerRESTController
from threads.peer.listen import PeerListenSocketThread
from threads.peer.heartbeat import PeerHeartBeatThread

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class PeerController:

    def __init__(self, peer_ip: str, server_ip: str, peer_port: int, thread_port: int):
        # arguments
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.server_ip = server_ip
        self.thread_port = thread_port

        self.peer_id = str(uuid.uuid4())

        # socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.peer_ip, self.peer_port))

        # threads (will be started at peer's main thread at project's root)
        self.thread_exceptions = queue.Queue()
        self.listen_thread = PeerListenSocketThread(self.peer_ip, self.thread_port, self.thread_exceptions)
        self.heartbeat_thread = PeerHeartBeatThread(self.peer_id, self.server_ip, self.thread_exceptions)

        # rest
        self.rest_controller = PeerRESTController()

        # method calls
        self.__create_downloads_dir()

    @staticmethod
    def __create_downloads_dir() -> None:
        """
        Creates a 'downloads' directory if not exists
        """

        if not os.path.exists(os.path.dirname("downloads/")):
            try:
                os.makedirs(os.path.dirname("downloads/"))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    @staticmethod
    def __generate_hash(resource_path: str, resource_name: str) -> str:
        """
        Generates a MD5 hash over a resource's content
        :param resource_path: Resource's path
        :param resource_name: Resource's name
        :return: MD5 hash over resource's content
        """

        md5_hash = hashlib.md5()

        resource = open(f"{resource_path}/{resource_name}", "rb")
        content = resource.read()
        md5_hash.update(content)

        return md5_hash.hexdigest()

    def list(self) -> str:
        """
        Lists all available resources at central server

        :return String response for the client at peer's main thread
        """

        # call central server
        response = self.rest_controller.call_server_get_all_resources(
            server_ip=self.server_ip
        )

        return json.loads(response.json())

    def upload(self, resource: str) -> str:
        """
        Uploads a local resource to the central server

        :param resource: Local resource to be published with format: [<path>/]<name>
        :return: String response for the client at peer's main thread
        """

        try:
            resource_path = os.path.dirname(resource)
            resource_name = os.path.basename(resource)

            # call central server
            response = self.rest_controller.call_server_post_resource(
                peer_id=self.peer_id,
                peer_ip=self.peer_ip,
                thread_port=self.thread_port,
                resource_path=resource_path,
                resource_name=resource_name,
                resource_hash=self.__generate_hash(resource_path, resource_name),
                server_ip=self.server_ip
            ).json()

            if response.get("success"):
                return f"resource '{resource_name}' uploaded!"
            else:
                return f"could not upload, server said: '{response.get('data')}'!"

        except FileNotFoundError:
            return f"resource '{resource}' not found!"

    def download(self, resource_name) -> str:
        """
        Downloads a resource from another peer discovered through a call to the central server

        :param resource_name: Name of the desired resource to be downloaded
        :return String response for the client at peer's main thread
        """

        # call central server
        response = self.rest_controller.call_server_get_resource(
            resource_name=resource_name,
            server_ip=self.server_ip
        ).json()

        if response.get("success"):

            peer_info = json.loads(response.get("data"))

            if not peer_info:
                return f"no peers found for resource '{resource_name}'!"

            peer_ip = peer_info[0].get("peer_ip")
            peer_port = peer_info[0].get("peer_port")
            peer_resource_path = peer_info[0].get("resource_path")
            peer_resource_name = peer_info[0].get("resource_name")
            peer_resource_hash = peer_info[0].get("resource_hash")

            file = f"{peer_resource_path}/{peer_resource_name}".encode("utf-8")

            try:
                # ask found resource to it's related peer
                self.socket.settimeout(10)
                self.socket.sendto(
                    file,  # data
                    (peer_ip, peer_port)  # address
                )
                resource_data, client = self.socket.recvfrom(1024)

            except socket.timeout:
                return f"it looks like peer '{peer_ip}:{peer_port}' is not responding, " \
                       f"interrupting connection!"

            # write received resource's data to 'downloads' directory
            downloaded_file_path = "downloads"
            downloaded_file_name = f"{peer_ip}_{resource_name}"

            resource_file = open(f"{downloaded_file_path}/{downloaded_file_name}", "wb")
            resource_file.write(resource_data)
            resource_file.close()

            # validate downloaded resource
            downloaded_hash = self.__generate_hash(
                resource_path=downloaded_file_path,
                resource_name=downloaded_file_name
            )

            if peer_resource_hash == downloaded_hash:
                return f"resource '{downloaded_file_name}' downloaded at path " \
                       f"'{downloaded_file_path}'!"

            else:
                return f"resource '{downloaded_file_name}' downloaded at path " \
                       f"'{downloaded_file_path}' but hash is incorrect, file " \
                       f"might be corrupted!"

        else:
            return f"could not download, server said: {response.get('data')}"
