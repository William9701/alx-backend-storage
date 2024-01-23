#!/usr/bin/env python3
"""This is a mangodb tutorial module"""
from typing import List
from pymongo import MongoClient


def list_all(mongo_collection) -> List:
    """ List all documents in a collection """
    documents = mongo_collection.find()
    return list(documents) if documents else []
