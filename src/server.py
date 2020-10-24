#!/usr/bin/env python3

# external dependencies
import flask
import flask_restful

# project dependencies
from src.controllers.resource import ResourceController

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"

if __name__ == "__main__":
    app = flask.Flask(__name__)
    api = flask_restful.Api(app)

    api.add_resource(ResourceController, "/resource")
    app.run()
