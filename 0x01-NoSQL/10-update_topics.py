#!/usr/bin/env python3
"""This is a mangodb tutorial module"""


def update_topics(mongo_collection, name, topics):
    """ Update all topics of a school document based on the name """
    mongo_collection.update_one({'name': name}, {'$set': {'topics': topics}})

