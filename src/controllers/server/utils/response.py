#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines a pattern for central server's responses
"""

# built-in dependencies
import typing

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "02/11/2020"


def ok(data: str) -> typing.Tuple:
    """
    Generic OK (200) response
    """

    return {"success": True, "data": data}, 200


def bad_request(data: str) -> typing.Tuple:
    """
    Generic BAD REQUEST (400) response
    """

    return {"success": False, "data": data}, 400


def unprocessable_entity(data: str) -> typing.Tuple:
    """
    Generic UNPROCESSABLE ENTITY (422) response
    """

    return {"success": False, "data": data}, 422


def internal_server_error(data: str) -> typing.Tuple:
    """
    Generic INTERNAL SERVER ERROR (500) response
    """

    return {"success": False, "data": data}, 500
