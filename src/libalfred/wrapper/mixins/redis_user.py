from typing import Optional

import redis


class RedisUserMixin:
    """Mixin for redis capability."""

    redis_host: str
    redis_port: int
    redis_password: Optional[str]

    rc: redis.Redis
    pubsub: redis.client.PubSub
    _connected: bool = False

    def connect_redis(self):
        self.rc = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password,
        )
        self.pubsub = self.rc.pubsub(ignore_subscribe_messages=True)

        self._connected = True
