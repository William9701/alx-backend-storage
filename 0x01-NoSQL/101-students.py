#!/usr/bin/env python3
"""This is a mangodb tutorial module"""

from typing import List
from pymongo import MongoClient


def top_students(mongo_collection) -> List:
    """ Returns all students sorted by average score """
    students = mongo_collection.aggregate([
        {
            '$unwind': {
                'path': '$topics'
            }
        }, {
            '$group': {
                '_id': '$_id',
                'name': {
                    '$first': '$name'
                },
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        }, {
            '$sort': {
                'averageScore': -1
            }
        }
    ])
    return list(students)
