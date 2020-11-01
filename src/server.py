#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# external dependencies
import atexit
import flask
import flask_restful

# project dependencies
from controllers.rest.server.resource import ResourceController
from controllers.rest.server.heartbeat import HeartBeatController
from database.table import create_table

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"

if __name__ == "__main__":
    app = flask.Flask(__name__)
    api = flask_restful.Api(app)

    atexit.register(HeartBeatController.stop_threads)

    api.add_resource(ResourceController, "/resource")
    api.add_resource(HeartBeatController, "/heartbeat")

    create_table()

    app.run()
