#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# project dependencies
from controllers.peer_controller import PeerController

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "25/10/2020"


if __name__ == "__main__":
    peer_ip = input("peer ip: ")
    server_ip = input("server ip: ")

    peer = PeerController(peer_ip, server_ip)

    resource = input("resource to register: ")
    peer.register_resource(resource)

    resource = input("resource to retrieve: ")
    peer.get_resource(resource)
