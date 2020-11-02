#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import hashlib

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


def generate_hash(resource_path: str, resource_name: str) -> str:
    """
    Generates a MD5 hash over resource's content
    :param resource_path: Resource's path (provided by this peer)
    :param resource_name: Resource's name (provided by this peer)
    :return: MD5 hash over resource's content
    """

    md5_hash = hashlib.md5()

    a_file = open(f"{resource_path}/{resource_name}", "rb")
    content = a_file.read()
    md5_hash.update(content)

    digest = md5_hash.hexdigest()
    return digest
