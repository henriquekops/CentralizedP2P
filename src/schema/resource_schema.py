#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# external dependencies
from marshmallow import Schema, fields

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class GetSchema(Schema):
    """
    Schema validation for resource 'GET' route
    """

    resource_name = fields.String()


class PostSchema(Schema):
    """
    Schema validation for resource 'POST' route
    """

    peer_id = fields.UUID()
    peer_ip = fields.IPv4()
    resource_name = fields.String()
    resource_hash = fields.String()
