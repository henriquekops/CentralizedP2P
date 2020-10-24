#!/usr/bin/env python3

# external dependencies
from flask_restful import Resource

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class ResourceController(Resource):
    """
    Controller for '/resource' route
    """

    @staticmethod
    def get():
        # get resource
        print("get resource")

    @staticmethod
    def post():
        # post resource
        print("post resource")
