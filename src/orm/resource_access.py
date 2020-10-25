#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# external dependencies
import sqlalchemy
from sqlalchemy.orm import sessionmaker

# project dependencies
from orm.resource_table import (Base, ResourceTable)

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class ResourceAccess:
    """
    Peer resource table access
    """

    def __init__(self):
        self.engine = sqlalchemy.create_engine("sqlite:///db.sqlite3")
        self.session = sessionmaker(bind=self.engine)

    def create_database(self):
        Base.metadata.create_all(self.engine)

    def register_peer(self, peer_id, peer_ip, resource_name, resource_hash):
        session = self.session()
        try:
            new_resource = ResourceTable()

            new_resource.peerId = peer_id
            new_resource.peerIp = peer_ip
            new_resource.resourceName = resource_name
            new_resource.resourceHash = resource_hash

            session.add(new_resource)
            session.commit()
        finally:
            session.close()

    def get_peer_ip(self, resource_name):
        session = self.session()
        try:
            return session\
                .query(ResourceTable.peerIp)\
                .filter(ResourceTable.resourceName == resource_name)\
                .group_by(ResourceTable.peerId)\
                .all()
        finally:
            session.close()

    def drop_peer(self, peer_id):
        session = self.session()
        try:
            session\
                .query(ResourceTable)\
                .filter(ResourceTable.peerId == peer_id)\
                .delete()
            session.commit()
        finally:
            session.close()
