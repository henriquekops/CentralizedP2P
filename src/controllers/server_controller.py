#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import json
from typing import Tuple

# external dependencies
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

# project dependencies
from controllers.database_controller import DatabaseResourceTableController
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

    db_access = DatabaseResourceTableController()

    @classmethod
    def get(cls) -> Tuple:
        """
        Retrieve every peer's info that contains such resource
        :return: List of peer's info
        """

        body = request.get_json()

        if not body:
            return "No body", 400

        try:
            body_data = cls.get_schema.load(body)

            peer_matrix = cls.db_access.get_available_peers(
                resource_name=body_data.get("resource_name")
            )

            # map returned db matrix into list of dicts as: [{"peer_ip": "...", "peer_port": "..."}]
            fields = ["peer_ip", "peer_port"]
            peer_list = list(map(lambda x: {fields[i]: x[i] for i in range(len(x))}, peer_matrix))

            return json.dumps(peer_list), 200

        except ValidationError as error:
            return error.messages, 422

    @classmethod
    def post(cls) -> Tuple:
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
                peer_port=int(body_data.get("peer_port")),
                resource_name=body_data.get("resource_name"),
                resource_hash=body_data.get("resource_hash")
            )

            return json.dumps(body), 200

        except ValidationError as error:
            return error.messages, 422
