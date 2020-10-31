#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# external dependencies
from marshmallow import Schema, fields

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "29/10/2020"


class GetHeartbeatSchema(Schema):
    """
    Schema validation for server's 'GET' route (/heartbeat)
    """

    peer_id = fields.UUID()
