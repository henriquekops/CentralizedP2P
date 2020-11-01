#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import typing

# external dependencies
import flask
import flask_restful
import marshmallow

# project dependencies
from controllers.database import get_database_resource_table_controller
from schema.heartbeat import PostHeartbeatSchema
from threads.server.heartbeat import ServerHeartBeatThread

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class HeartBeatController(flask_restful.Resource):
    """
    Controller for '/heartbeat' route
    """

    get_schema = PostHeartbeatSchema()
    peer_map = dict()

    @classmethod
    def post(cls) -> typing.Tuple:

        body = flask.request.get_json()

        if not body:
            return "No body", 400

        try:
            body_data = cls.get_schema.load(body)
            peer_id = str(body_data.get("peer_id"))

            if peer_id not in cls.peer_map.keys():
                new_queue = list()

                # tell heartbeat thread that a request has arrived
                new_queue.append(1)

                cls.peer_map.update({
                    peer_id: new_queue
                })

                server_heart_beat_thread = ServerHeartBeatThread(peer_id, new_queue)
                server_heart_beat_thread.start()

            else:
                peer_queue = cls.peer_map.get(peer_id)

                # tell heartbeat thread that a request has arrived
                peer_queue.append(1)

            return "OK", 200

        except marshmallow.ValidationError as error:
            return error.messages, 422
