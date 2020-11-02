#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import hashlib
import json

# external dependencies
import requests

# project dependencies
from utils.hash import generate_hash

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class PeerRESTController:
    """
    Controller for peer communication through REST
    """

    def call_server_post_resource(self, peer_id: str, peer_ip: str, thread_port: int,
                                  resource_path: str, resource_name: str, server_ip: str) -> requests.Response:
        """
        Call server to register resource and assign to this peer

        :param peer_id: Peer's uuid
        :param peer_ip: Peer's ipv4
        :param thread_port: Peer's download port
        :param resource_path: Provided resource's path
        :param resource_name: Resource provided by this peer
        :param server_ip: Central server's ipv4
        :return: Central server's response
        """

        body = {
            "peer_id": peer_id,
            "peer_ip": peer_ip,
            "peer_port": thread_port,
            "resource_path": resource_path,
            "resource_name": resource_name,
            "resource_hash": generate_hash(resource_path, resource_name)
        }
        header = {
            "content-type": "application/json; charset=utf-8"
        }
        return requests.post(
            f"http://{server_ip}:5000/resource",
            data=json.dumps(body),
            headers=header
        )

    @staticmethod
    def call_server_get_resource(resource_name: str, server_ip: str) -> requests.Response:
        """
        Call server to search peer ips that contains this resource

        :param resource_name: Resource provided by this peer
        :param server_ip: Central server's ipv4
        :return: Central server's response
        """
        body = {
            "resource_name": resource_name
        }
        header = {
            "content-type": "application/json; charset=utf-8"
        }
        return requests.get(
            f"http://{server_ip}:5000/resource",
            data=json.dumps(body),
            headers=header
        )

    @staticmethod
    def call_server_get_all_resources(server_ip: str) -> requests.Response:
        """
        Call server to list all available resources

        :param server_ip: Central server's ipv4
        :return: Central server's response
        """

        return requests.get(
            f"http://{server_ip}:5000/resource"
        )
