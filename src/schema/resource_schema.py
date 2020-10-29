#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# external dependencies
from marshmallow import Schema, fields

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class GetSchema(Schema):
    """
    Schema validation for server's 'GET' route (/resource)
    """

    resource_name = fields.String()


class PostSchema(Schema):
    """
    Schema validation for server's 'POST' route (/resource)
    """

    peer_id = fields.UUID()
    peer_ip = fields.IPv4()
    peer_port = fields.Int()
    resource_name = fields.String()
    resource_hash = fields.String()
