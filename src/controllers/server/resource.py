#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines a controller for '/resource' route
"""

# built-in dependencies
import json
import typing

# external dependencies
import flask
import flask_restful
import marshmallow

# project dependencies
from controllers.database.database import get_database_resource_table_controller
from controllers.server.utils import response
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

    # fields to map database's response
    db_fields = ["peer_ip", "peer_port", "resource_path", "resource_name", "resource_hash"]

    @classmethod
    def get(cls) -> typing.Tuple:
        """
        Retrieve peer's info that contains a certain resource name OR a list of every peer's info
        (decision is made with body presence or not, respectively)

        :return: Tuple which contains desired peer's info and a relevant HTTP status code
        """

        body = flask.request.get_json()

        # if request was called with no body, list all resources
        if not body:
            # call database
            resource_matrix = cls.db_access.get_all_resources()

            # transform matrix of values from database to list of dicts
            resource_list = list(map(
                lambda x: {cls.db_fields[i]: x[i] for i in range(len(x))},
                resource_matrix
            ))

            return response.ok(data=json.dumps(resource_list))

        # else filter through resource's name
        else:
            try:
                # request's body validation through marshmallow
                body_data = cls.get_schema.load(body)

                # call database
                resource_list = cls.db_access.get_available_peer(
                    resource_name=str(body_data.get("resource_name"))
                )

                # transform list of values from database to dict
                resource_dict = {
                    cls.db_fields[i]: resource_list[i] for i in range(len(resource_list))
                }

                return response.ok(data=json.dumps(resource_dict))

            except marshmallow.ValidationError as error:
                return response.unprocessable_entity(data=str(error.messages))

    @classmethod
    def post(cls) -> typing.Tuple:
        """
        Assign a new resource to a peer at the database

        :return: Request body
        """

        body = flask.request.get_json()

        if not body:
            return response.bad_request(data="Request needs a body, but none encountered.")

        try:
            # request's body validation through marshmallow
            body_data = cls.post_schema.load(body)

            # call database
            cls.db_access.register_peer(
                peer_ip=str(body_data.get("peer_ip")),
                peer_id=str(body_data.get("peer_id")),
                peer_port=int(body_data.get("peer_port")),
                resource_name=str(body_data.get("resource_name")),
                resource_path=str(body_data.get("resource_path")),
                resource_hash=str(body_data.get("resource_hash"))
            )

            return response.ok(data=json.dumps(body))

        except marshmallow.ValidationError as error:
            return response.unprocessable_entity(data=error.messages)
