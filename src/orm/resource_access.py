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

    def insert(self, peer_id, peer_ip, resource_name, resource_hash):
        session = self.session()
        try:
            new_resource = ResourceTable(peer_id, peer_ip, resource_name, resource_hash)
            session.add(new_resource)
            session.commit()
        finally:
            session.close()

    def select(self, resource_name):
        session = self.session()
        try:
            return session\
                .query(ResourceTable.peerIp)\
                .filter(ResourceTable.resourceName == resource_name)\
                .groupBy(ResourceTable.peerId)\
                .all()
        finally:
            session.close()

    def delete(self, peer_ip):
        session = self.session()
        try:
            session\
                .query(ResourceTable)\
                .filter(ResourceTable.peerIp == peer_ip)\
                .delete()
        finally:
            session.close()
