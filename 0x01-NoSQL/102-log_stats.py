#!/usr/bin/env python3
"""This is a mangodb tutorial module"""

from pymongo import MongoClient


def log_stats(mongo_collection):
    """ Provides some stats about Nginx logs stored in MongoDB """
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print(f"{mongo_collection.count_documents({}):} logs")

    print("Methods:")
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    status_check_count = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

    print("IPs:")
    ips = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    log_stats(logs_collection)
