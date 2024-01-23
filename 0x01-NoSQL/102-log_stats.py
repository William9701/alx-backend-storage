#!/usr/bin/env python3
"""
Log stats - improved version
"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})
    print(f"{total_logs} logs")

    # Methods status
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = logs_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Status check status
    status_check = logs_collection.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

    # IPs stats
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    top_ips = logs_collection.aggregate(pipeline)

    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")
