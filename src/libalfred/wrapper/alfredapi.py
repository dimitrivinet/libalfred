import logging
from typing import Optional

from libalfred.wrapper.mixins.redis_user import RedisUserMixin
from libalfred.utils.position import Position
from libalfred.utils.command import Command
from libalfred.wrapper import exceptions

logger = logging.getLogger(__name__)


class AlfredAPI(RedisUserMixin):
    """API for sending commands to the robot."""

    host: str
    port: int
    password: Optional[str]
    pub_channel: str

    def __init__(
        self,
        host: str,
        port: int,
        password: str = None,
        pub_channel: str = "command-robot",
        auto_connect: bool = False,
    ):
        self.host = host
        self.port = port
        self.password = password
        self.pub_channel = pub_channel

        if auto_connect:
            self.connect_redis(self.host, self.port, self.password)

    def publish_command(self, command: Command):
        if not self.connected:
            raise exceptions.NotConnectedException(
                "This AlfredAPI instance is not connected to a redis server."
            )
        self.rc.publish(self.pub_channel, repr(command))

    def move_line(
        self,
        goal_pos: Position,
        speed: int,
        acc: int,
        is_relative: bool,
        do_wait: bool,
        timeout_ms: int,
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
