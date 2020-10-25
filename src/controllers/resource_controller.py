#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pprint import pprint

# external dependencies
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

# project dependencies
from orm.resource_access import ResourceAccess
from schema.resource_schema import (
    GetSchema,
    PostSchema
)

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class ResourceController(Resource):
    """
    Controller for '/resource' route
    """

    post_schema = PostSchema()
    get_schema = GetSchema()

    db_access = ResourceAccess()

    @classmethod
    def get(cls):
        """
        Retrieve peer ips that contains resource
        :return: List of peer ips
        """

        body = request.get_json()
        if not body:
            return "No body", 400
        try:
            body_data = cls.get_schema.load(body)
            peer_ips = cls.db_access.get_peer_ip(
                resource_name=body_data.get("resource_name")
            )
            return peer_ips, 200
        except ValidationError as error:
            return error.messages, 422

    @classmethod
    def post(cls):
        """
        Assign a new resource to a peer
        :return: Request body
        """

        body = request.get_json()
        if not body:
            return "No body", 400
        try:
            body_data = cls.post_schema.load(body)
            cls.db_access.register_peer(
                peer_ip=str(body_data.get("peer_ip")),
                peer_id=str(body_data.get("peer_id")),
                resource_name=body_data.get("resource_name"),
                resource_hash=body_data.get("resource_hash")
            )
            return cls.post_schema.dump(body_data), 200
        except ValidationError as error:
            return error.messages, 422
