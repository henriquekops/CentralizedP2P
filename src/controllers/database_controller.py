#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
from typing import List

# external dependencies
import sqlalchemy
from sqlalchemy.orm import sessionmaker

# project dependencies
from database.resource_table import (Base, ResourceTable)

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class DatabaseResourceTableController:
    """
    Controller for resource table access
    """

    def __init__(self):
        self.engine = sqlalchemy.create_engine("sqlite:///db.sqlite3")
        self.session = sessionmaker(bind=self.engine)

    def create_database(self):
        """
        Create all sqlite3 databases registered at 'Base' object through declared 'engine'
        """

        Base.metadata.create_all(self.engine)

    def register_peer(self, peer_id: str, peer_ip: str, peer_port: int, resource_name: str, resource_path: str,
                      resource_hash: str) -> None:
        """
        Register peer-resource relationship at database

        :param peer_id: Peer's id
        :param peer_ip: Peer's ip
        :param peer_port: Peer's listen port
        :param resource_name: Resource's name
        :param resource_path: Resource's path
        :param resource_hash: Resource's MD5
        """

        session = self.session()

        try:
            new_resource = ResourceTable()

            new_resource.peerId = peer_id
            new_resource.peerIp = peer_ip
            new_resource.peerPort = peer_port
            new_resource.resourceName = resource_name
            new_resource.resourcePath = resource_path
            new_resource.resourceHash = resource_hash

            session.add(new_resource)
            session.commit()

        finally:
            session.close()

    def get_available_peers(self, resource_name: str) -> List:
        """
        Get every peer's info and port that has registered same resource name

        :param resource_name: Name of the resource to be searched at database
        :return: List of every peer's info
        """

        session = self.session()

        try:
            return session\
                .query(
                    ResourceTable.peerIp,
                    ResourceTable.peerPort,
                    ResourceTable.resourcePath,
                    ResourceTable.resourceName
                )\
                .filter(ResourceTable.resourceName == resource_name)\
                .group_by(ResourceTable.peerId)\
                .all()

        finally:
            session.close()

    def drop_peer(self, peer_id: str) -> None:
        """
        Delete every peer's record through its id

        :param peer_id: Peer's ip to be used as filter
        """

        session = self.session()
        try:
            session\
                .query(ResourceTable)\
                .filter(ResourceTable.peerId == peer_id)\
                .delete()
            session.commit()
        finally:
            session.close()
