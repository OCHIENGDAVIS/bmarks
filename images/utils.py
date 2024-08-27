from django.conf import settings

import redis


def create_redis_connection(host, port, db):
    r = redis.Redis(
        host,
        port,
        db
    )
    return r
