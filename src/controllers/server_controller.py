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
from schema.heartbeat_schema import GetHeartbeatSchema
from schema.resource_schema import (
    GetResourceSchema,
    PostResourceSchema
)
from threads.heart_beat_thread import ServerHeartBeatThread

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"

db_access = DatabaseResourceTableController()


class ResourceController(Resource):
    """
    Controller for '/resource' route
    """

    post_schema = PostResourceSchema()
    get_schema = GetResourceSchema()

    db_get_fields = ["peer_ip", "peer_port", "resource_path", "resource_name"]

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

            peer_matrix = db_access.get_available_peers(
                resource_name=str(body_data.get("resource_name"))
            )

            # map returned db matrix into list of dicts as:
            # [{"peer_ip": "...", "peer_port": "...", "resource_path": "...", "resource_name": "..."}]
            peer_list = list(map(lambda x: {cls.db_get_fields[i]: x[i] for i in range(len(x))}, peer_matrix))

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

            db_access.register_peer(
                peer_ip=str(body_data.get("peer_ip")),
                peer_id=str(body_data.get("peer_id")),
                peer_port=int(body_data.get("peer_port")),
                resource_name=str(body_data.get("resource_name")),
                resource_path=str(body_data.get("resource_path")),
                resource_hash=str(body_data.get("resource_hash"))
            )

            return json.dumps(body), 200

        except ValidationError as error:
            return error.messages, 422


class HeartBeatController(Resource):
    """
    Controller for '/heartbeat' route
    """

    get_schema = GetHeartbeatSchema()

    peer_map = dict()

    @classmethod
    def post(cls) -> Tuple:

        body = request.get_json()

        if not body:
            return "No body", 400

        try:

            body_data = cls.get_schema.load(body)
            peer_id = str(body_data.get("peer_id"))

            if peer_id not in cls.peer_map.keys():
                new_queue = list()
                new_queue.append(1)

                cls.peer_map.update({
                    peer_id: new_queue
                })

                server_heart_beat_thread = ServerHeartBeatThread(peer_id, new_queue, db_access)
                server_heart_beat_thread.start()

            else:
                peer_queue = cls.peer_map.get(peer_id)

                if 0 in peer_queue:
                    _ = cls.peer_map.pop(peer_id)
                peer_queue.append(1)

            return "OK", 200

        except ValidationError as error:
            return error.messages, 422
