#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines a controller for '/heartbeat' route
"""

# built-in dependencies
import typing

# external dependencies
import flask
import flask_restful
import marshmallow

# project dependencies
from schema.heartbeat import PostHeartbeatSchema
from threads.server.heartbeat import ServerHeartBeatThread

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "30/10/2020"


class HeartBeatController(flask_restful.Resource):
    """
    Controller for '/heartbeat' route
    """

    get_schema = PostHeartbeatSchema()

    threads = list()  # list of opened threads (one thread per caller peer)
    peer_map = dict()  # structure to map every caller peer's id to a queue for thread communication

    @classmethod
    def post(cls) -> typing.Tuple:
        """
        Manipulates a heartbeat thread for the caller peer

        :return: Tuple which contains a message for the peer and a relevant HTTP status code
        """

        body = flask.request.get_json()

        if not body:
            return "No body", 400

        try:
            # request's body validation through marshmallow
            body_data = cls.get_schema.load(body)

            peer_id = str(body_data.get("peer_id"))

            if peer_id not in cls.peer_map.keys():  # new peer
                new_queue = list()

                # tell heartbeat thread that a request has arrived
                new_queue.append(1)

                # create a new 'peer x queue' association at map
                cls.peer_map.update({
                    peer_id: new_queue
                })

                # start heartbeat thread for caller peer's ip
                server_heart_beat_thread = ServerHeartBeatThread(peer_id, new_queue)
                cls.threads.append(server_heart_beat_thread)
                server_heart_beat_thread.start()

            else:  # old peer

                # get peer's queue at map
                peer_queue = cls.peer_map.get(peer_id)

                # when thread finishes, it produces a `0` at its queue
                # this code is reachable when peer restarts communications
                # it starts a new thread for old disconnected peer
                if 0 in peer_queue:
                    server_heart_beat_thread = ServerHeartBeatThread(peer_id, peer_queue)
                    cls.threads.append(server_heart_beat_thread)
                    server_heart_beat_thread.start()

                # tell heartbeat thread that a request has arrived
                peer_queue.append(1)

            return "OK", 200

        except marshmallow.ValidationError as error:
            return error.messages, 422

    @classmethod
    def stop_threads(cls) -> None:
        """
        Stop all central server's heartbeat threads
        """

        print("\nstopping threads ...")

        for t in cls.threads:
            t.stop()
            t.join()
