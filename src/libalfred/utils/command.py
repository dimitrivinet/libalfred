from __future__ import annotations

from dataclasses import dataclass

from libalfred.utils.position import Position


@dataclass
class Command(Position):
    """Represents a command sent to the controller."""

    speed: int = 1
    acc: int = 1
    is_cartesian: bool = False
    is_relative: bool = False
    do_wait: bool = False
    timeout_ms: int = 0

    @classmethod
    def from_string(cls, command: str) -> Command:
        """Get a Command object from its representation as a string."""

        command = command[8:-1]  # remove 'Command(' and ')' from string.
        args = command.split(", ")
        args_dict = {key: val for key, val in [arg.split("=") for arg in args]}

        return Command(
            float(args_dict["x"]),
            float(args_dict["y"]),
            float(args_dict["z"]),
            float(args_dict["roll"]),
            float(args_dict["pitch"]),
            float(args_dict["yaw"]),
            args_dict["is_radian"] == "True",
            int(args_dict["speed"]),
            int(args_dict["acc"]),
            args_dict["is_cartesian"] == "True",
            args_dict["is_relative"] == "True",
            args_dict["do_wait"] == "True",
            int(args_dict["timeout_ms"]),
        )
