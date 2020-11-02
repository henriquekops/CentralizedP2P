#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines the database's schemas
"""

# external dependencies
import sqlalchemy
from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.ext.declarative import declarative_base

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"

Base = declarative_base()


class ResourceTable(Base):
    """
    Database 'resources' table definition
    """

    __tablename__ = "resources"
    sqlite_autoincrement = True

    id = Column(Integer, primary_key=True)  # auto incremental PK
    peerId = Column(String(36), nullable=False)  # peer ID
    peerIp = Column(String(16), nullable=False)  # peer IP
    peerPort = Column(Integer, nullable=False)  # peer download port
    resourceName = Column(String(100), nullable=False)  # resource's name
    resourcePath = Column(String(100), nullable=False)  # resource's path at peerIp:peerPort
    resourceHash = Column(String(50), nullable=False)  # resource's hash


def create_table() -> None:
    """
    Create 'resources' table registered at 'Base' object through declared 'engine'
    """

    engine = sqlalchemy.create_engine("sqlite:///db.sqlite3")
    if not engine.dialect.has_table(engine, "resources"):
        Base.metadata.create_all(engine)
