#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines '/resource' routes body's schemas
"""

# external dependencies
import marshmallow

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class GetResourceSchema(marshmallow.Schema):
    """
    Schema validation for central server's 'GET' route (/resource)

    Example:
    {
        resource_name: <String>
    }
    """

    resource_name = marshmallow.fields.String()


class PostResourceSchema(marshmallow.Schema):
    """
    Schema validation for central server's 'POST' route (/resource)

    Example:
    {
        peer_id: <UUID>
        peer_ip: <IPV4>
        peer_port: <Int>
        resource_name: <String>
        resource_path: <String>
        resource_hash: <String>
    }
    """

    peer_id = marshmallow.fields.UUID()
    peer_ip = marshmallow.fields.IPv4()
    peer_port = marshmallow.fields.Int()
    resource_name = marshmallow.fields.String()
    resource_path = marshmallow.fields.String()
    resource_hash = marshmallow.fields.String()
