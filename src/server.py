#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# external dependencies
import flask
import flask_restful

# project dependencies
from controllers.server_controller import ResourceController, HeartBeatController
from controllers.database_controller import DatabaseResourceTableController

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"

if __name__ == "__main__":
    app = flask.Flask(__name__)
    api = flask_restful.Api(app)

    api.add_resource(ResourceController, "/resource")
    api.add_resource(HeartBeatController, "/heartbeat")

    access = DatabaseResourceTableController()
    access.create_database()

    app.run()
