#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import json
import os
from hashlib import md5
from uuid import uuid4

# external dependencies
import requests

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class PeerController:
    """
    Controller for peer communication
    """

    def __init__(self, peer_ip, server_ip):
        self.server_ip = server_ip
        self.peer_ip = peer_ip
        self.peer_id = str(uuid4())

    @staticmethod
    def __generate_hash(resource):
        """
        Generates a MD5 hash over resource's content

        :param resource: Resource provided by this peer
        :return: MD5 hash over resource's content
        """

        hash_md5 = md5()

        with open(resource, "rb") as r:
            for chunk in iter(lambda: r.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()

    def register_resource(self, resource):
        """
        Call server to register resource and assign to this peer

        :param resource: Resource provided by this peer
        :return: Server's response
        """

        body = {
            "peer_id": self.peer_id,
            "peer_ip": self.peer_ip,
            "resource_name": os.path.basename(resource),
            "resource_hash": self.__generate_hash(resource)
        }
        header = {
            "content-type": "application/json; charset=utf-8"
        }
        return requests.post(
            f"http://{self.server_ip}:5000/resource",
            data=json.dumps(body),
            headers=header
        )

    def get_resource(self, resource):
        """
        Call server to search peer ips that contains this resource

        :param resource: Resource provided by this peer
        :return: Server's response
        """

        body = {
            "resource_name": resource
        }
        header = {
            "content-type": "application/json; charset=utf-8"
        }
        return requests.get(
            f"http://{self.server_ip}:5000/resource",
            data=json.dumps(body),
            headers=header
        )
