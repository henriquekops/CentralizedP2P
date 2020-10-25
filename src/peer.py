#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import json
import os
from hashlib import md5
from pprint import pprint
from uuid import uuid4

# external dependencies
import requests


class Peer:
    """
    Peer implementation
    """

    def __init__(self, peer_ip, server_ip):
        self.server_ip = server_ip
        self.peer_ip = peer_ip
        self.peer_id = str(uuid4())

    @staticmethod
    def __generate_hash(resource):
        hash_md5 = md5()
        with open(resource, "rb") as r:
            for chunk in iter(lambda: r.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def register_resource(self, resource):
        body = {
            "peer_id": self.peer_id,
            "peer_ip": self.peer_ip,
            "resource_name": os.path.basename(resource),
            "resource_hash": self.__generate_hash(resource)
        }
        header = {
            "content-type": "application/json; charset=utf-8"
        }
        response = requests.post(
            f"http://{self.server_ip}:5000/resource",
            data=json.dumps(body),
            headers=header
        )
        pprint(response.json())

    def get_resource(self, resource):
        body = {
            "resource_name": resource
        }
        header = {
            "content-type": "application/json; charset=utf-8"
        }
        response = requests.get(
            f"http://{self.server_ip}:5000/resource",
            data=json.dumps(body),
            headers=header
        )
        pprint(response.json())


if __name__ == "__main__":
    peer_ip = input("peer ip: ")
    server_ip = input("server ip: ")

    peer = Peer(peer_ip, server_ip)

    resource = input("resource to register: ")
    peer.register_resource(resource)

    resource = input("resource to retrieve: ")
    peer.get_resource(resource)
