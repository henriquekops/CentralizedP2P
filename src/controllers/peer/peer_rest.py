#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines a controller for peer's REST operations
"""

# built-in dependencies
import json

# external dependencies
import requests

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "30/10/2020"


class PeerRESTController:
    """
    Controller for peer's communication with central server through REST
    """

    @staticmethod
    def call_server_post_resource(peer_id: str, peer_ip: str, thread_port: int, resource_path: str,
                                  resource_name: str, resource_hash: str,  server_ip: str) -> requests.Response:
        """
        Call central server to register a resource and assign to the caller peer

        :param peer_id: Peer's UUID
        :param peer_ip: Peer's IPV4
        :param thread_port: Peer's listen port
        :param resource_path: Resource's path provided by the caller peer
        :param resource_name: Resource's name provided by the caller peer
        :param resource_hash: Resource's hash provided by the caller peer
        :param server_ip: Central server's IPV4
        :return: Central server's response
        """

        body = {
            "peer_id": peer_id,
            "peer_ip": peer_ip,
            "peer_port": thread_port,
            "resource_path": resource_path,
            "resource_name": resource_name,
            "resource_hash": resource_hash,
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
        Call central server to search peer ips that contains a resource through its name

        :param resource_name: Resource provided by the caller peer
        :param server_ip: Central server's IPV4
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
        Call central server to list all available resources

        :param server_ip: Central server's IPV4
        :return: Central server's response
        """

        return requests.get(f"http://{server_ip}:5000/resource")
