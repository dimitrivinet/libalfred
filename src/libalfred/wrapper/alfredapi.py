import logging
from typing import Optional

from libalfred.wrapper.mixins.redis_user import RedisUserMixin

logger = logging.getLogger(__name__)


class AlfredAPI(RedisUserMixin):
    """API for sending commands to the robot."""

    host: str
    port: int
    password: str

    def __init__(
        self,
        host: str,
        port: int,
        password: Optional[str] = None,
        auto_connect: bool = False,
    ):
        self.host = host
        self.port = port
        self.password = password

        if auto_connect:
            self.connect_redis(self.host, self.port, self.password)
