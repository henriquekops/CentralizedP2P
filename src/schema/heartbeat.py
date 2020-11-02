#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines '/heartbeat' route body's schema
"""

# external dependencies
import marshmallow

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "29/10/2020"


class PostHeartbeatSchema(marshmallow.Schema):
    """
    Schema validation for central server's 'POST' route (/heartbeat)

    Example:
    {
        peer_id: <UUID>
    }
    """

    peer_id = marshmallow.fields.UUID()
