#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that starts the REST central server (server's main thread)
"""

# external dependencies
import atexit
import flask
import flask_restful
from werkzeug.exceptions import InternalServerError

# project dependencies
from controllers.server.heartbeat import HeartBeatController
from controllers.server.resource import ResourceController
from controllers.server.utils import response
from database.table import create_table

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"

if __name__ == "__main__":
    app = flask.Flask(__name__)
    api = flask_restful.Api(app)

    # stop server's heartbeat threads when server is stopped
    atexit.register(HeartBeatController.stop_threads)

    # when internal exceptions occurs
    @app.errorhandler(InternalServerError)
    def handle_exception(e):
        return response.internal_server_error(data=e)

    # assign resources to routes
    api.add_resource(ResourceController, "/resource")
    api.add_resource(HeartBeatController, "/heartbeat")

    # create database table if not exists
    create_table()

    app.run()
