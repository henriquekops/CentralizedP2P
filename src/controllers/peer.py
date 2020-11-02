#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import errno
import json
import os
import queue
import socket
import uuid

# project dependencies
from controllers.rest.peer.peer import PeerRESTController
from threads.peer.download import PeerDownloadThread
from threads.peer.heartbeat import PeerHeartBeatThread

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class PeerController:

    def __init__(self, peer_ip: str, server_ip: str, peer_port: str, thread_port: str):
        # arguments
        self.peer_ip = str(peer_ip)
        self.server_ip = str(server_ip)
        self.thread_port = int(thread_port)
        self.peer_id = str(uuid.uuid4())

        # socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((peer_ip, int(peer_port)))

        # threads
        self.thread_exceptions = queue.Queue()
        self.download_thread = PeerDownloadThread(self.peer_ip, self.thread_port, self.thread_exceptions)
        self.heartbeat_thread = PeerHeartBeatThread(self.peer_id, self.server_ip, self.thread_exceptions)

        # rest
        self.rest_controller = PeerRESTController()

        # method calls
        self.__create_downloads_dir()

    @staticmethod
    def __create_downloads_dir() -> None:
        """
        Creates 'downloads' directory if not exists
        """

        if not os.path.exists(os.path.dirname("downloads/")):
            try:
                os.makedirs(os.path.dirname("downloads/"))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def upload(self, resource: str) -> str:
        """
        Uploads a local resource

        :param resource: Local resource name to be published
        :return: String response for the client
        """

        try:
            resource_path = os.path.dirname(resource)
            resource_name = os.path.basename(resource)

            response = self.rest_controller.call_server_post_resource(
                peer_id=self.peer_id,
                peer_ip=self.peer_ip,
                thread_port=self.thread_port,
                resource_path=resource_path,
                resource_name=resource_name,
                server_ip=self.server_ip
            )
            return f"uploaded: '{response.json()}'"

        except FileNotFoundError:
            return f"resource '{resource}' not found!"

    def download(self, resource_name) -> str:
        """
        Downloads a resource

        :param resource_name: Name of the desired resource
        :return String response for the client
        """

        response = self.rest_controller.call_server_get_resource(
            resource_name=resource_name,
            server_ip=self.server_ip
        )
        peers = json.loads(response.json())

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

    def list(self) -> str:
        """
        Lists all resources

        :return String response for the client
        """

        response = self.rest_controller.call_server_get_all_resources(
            server_ip=self.server_ip
        )

        peers = json.loads(response.json())

        return peers
