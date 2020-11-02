#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import json
import typing

# external dependencies
import flask
import flask_restful
import marshmallow

# project dependencies
from controllers.database import get_database_resource_table_controller
from schema.resource import (
    GetResourceSchema,
    PostResourceSchema
)

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class ResourceController(flask_restful.Resource):
    """
    Controller for '/resource' route
    """

    post_schema = PostResourceSchema()
    get_schema = GetResourceSchema()
    db_access = get_database_resource_table_controller()
    db_get_fields = ["peer_ip", "peer_port", "resource_path", "resource_name"]

    @classmethod
    def get(cls) -> typing.Tuple:

        """
        Retrieve every peer's info OR every peer's info that contains a certain resource
        :return: List of all peer's info OR every peer's info that contains a certain resource
        """

        body = flask.request.get_json()
        resource_matrix = None

        if not body:
            resource_matrix = cls.db_access.get_all_resources()
        else:
            try:
                body_data = cls.get_schema.load(body)
                resource_matrix = cls.db_access.get_available_peers(
                    resource_name=str(body_data.get("resource_name"))
                )
            except marshmallow.ValidationError as error:
                return error.messages, 422

        # map returned db matrix into list of dicts as:
        # [{"peer_ip": "...", "peer_port": "...", "resource_name": "..."}]
        resource_list = list(map(lambda x: {cls.db_get_fields[i]: x[i] for i in range(len(x))}, resource_matrix))

        return json.dumps(resource_list), 200


    @classmethod
    def post(cls) -> typing.Tuple:
        """
        Assign a new resource to a peer
        :return: Request body
        """

        body = flask.request.get_json()

        if not body:
            return "No body", 400

        try:
            body_data = cls.post_schema.load(body)

            cls.db_access.register_peer(
                peer_ip=str(body_data.get("peer_ip")),
                peer_id=str(body_data.get("peer_id")),
                peer_port=int(body_data.get("peer_port")),
                resource_name=str(body_data.get("resource_name")),
                resource_path=str(body_data.get("resource_path")),
                resource_hash=str(body_data.get("resource_hash"))
            )

            return json.dumps(body), 200

        except marshmallow.ValidationError as error:
            return error.messages, 422
