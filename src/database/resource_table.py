#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# external dependencies
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
    Database resource table
    """

    __tablename__ = "resources"
    sqlite_autoincrement = True

    id = Column(Integer, primary_key=True)  # auto incremental PK
    peerId = Column(String(36), nullable=False, unique=True)  # peer ID
    peerIp = Column(String(16), nullable=False)  # peer IP
    peerPort = Column(Integer, nullable=False) # peer download port
    resourceName = Column(String(100), nullable=False)  # resource's name
    resourceHash = Column(String(50), nullable=False)  # resource's hash
