from typing import Optional

import redis


class RedisUserMixin:
    """Mixin for redis capability."""

    rc: redis.Redis
    pubsub: redis.client.PubSub
    connected: bool = False

    def connect_redis(
        self, host: str, port: int, password: Optional[str] = None,
    ):
        self.rc = redis.Redis(host=host, port=port, password=password)
        self.pubsub = self.rc.pubsub(ignore_subscribe_messages=True)

        self.connected = True
