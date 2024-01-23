#!/usr/bin/env python3
"""This is a mangodb tutorial module"""


def insert_school(mongo_collection, **kwargs):
    """ Insert a new document in a collection based on kwargs """
    document = kwargs
    result = mongo_collection.insert_one(document)
    return result.inserted_id

