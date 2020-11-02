#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# built-in dependencies
import hashlib

__authors__ = ["Gabriel Castro", "Gustavo Possebon", "Henrique Kops"]
__date__ = "24/10/2020"


class HashUtil:

    @staticmethod
    def generate_hash(resource_path: str, resource_name: str) -> str:
        """
        Generates a MD5 hash over resource's content

        :param resource_path: Resource's path (provided by this peer)
        :param resource_name: Resource's name (provided by this peer)
        :return: MD5 hash over resource's content
        """

        hash_md5 = hashlib.md5()

        with open(f"{resource_path}/{resource_name}", "rb") as r:
            for chunk in iter(lambda: r.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()
