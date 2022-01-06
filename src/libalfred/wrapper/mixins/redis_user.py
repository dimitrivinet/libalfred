from typing import Optional

import redis


class RedisUserMixin:
    """Mixin for redis capability."""

    rc: redis.Redis

    def connect_redis(
        self, host: str, port: int, password: Optional[str] = None,
    ):
        self.rc = redis.Redis(host=host, port=port, password=password)
