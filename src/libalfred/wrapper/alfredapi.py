import logging
from typing import Optional

from libalfred.wrapper.mixins.redis_user import RedisUserMixin
from libalfred.utils.position import Position
from libalfred.utils.command import Command
from libalfred.wrapper import exceptions

logger = logging.getLogger(__name__)


class AlfredAPI(RedisUserMixin):
    """API for sending commands to the robot."""

    password: Optional[str]
    pub_channel: str

    def __init__(
        self,
        redis_host: str,
        redis_port: int,
        redis_password: str = None,
        pub_channel: str = "command-robot",
        auto_connect: bool = False,
    ):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.pub_channel = pub_channel

        if auto_connect:
            self.connect_redis()

    def publish_command(self, command: Command):
        if not self._connected:
            raise exceptions.NotConnectedException(
                "This AlfredAPI instance is not connected to a redis server."
            )
        self.rc.publish(self.pub_channel, {"command": repr(command)})

    def move_line(
        self,
        goal_pos: Position,
        speed: int = -1,
        acc: int = -1,
        is_relative: bool = False,
        do_wait: bool = False,
        timeout_ms: int = -1,
    ):
        """Move from start_pos to goal_pos in a straight line."""

        cmd = Command(
            x=goal_pos.x,
            y=goal_pos.y,
            z=goal_pos.z,
            roll=goal_pos.roll,
            pitch=goal_pos.pitch,
            yaw=goal_pos.yaw,
            is_radian=goal_pos.is_radian,
            speed=speed,
            acc=acc,
            is_cartesian=True,
            is_relative=is_relative,
            do_wait=do_wait,
            timeout_ms=timeout_ms,
        )

        self.publish_command(cmd)
