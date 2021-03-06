from dataclasses import dataclass, fields

import numpy as np


@dataclass
class Position:
    """Represents a position the robot can have."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    is_radian: bool = True

    @property
    def xyzrpy(self) -> list:
        """Returns a list containing x, y, z, roll, pitch, yaw.
        R, P and Y are always in radians."""
        return [
            self.x,
            self.y,
            self.z,
            self.roll if self.is_radian else np.deg2rad(self.roll),
            self.pitch if self.is_radian else np.deg2rad(self.pitch),
            self.yaw if self.is_radian else np.deg2rad(self.yaw),
        ]

    def __iter__(self):
        return iter([self.x, self.y, self.z, self.roll, self.pitch, self.yaw])

    def __len__(self):
        return len(fields(self))

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(len(self)))]

        try:
            field_name = fields(self)[index].name
            return self.__getattribute__(field_name)
        except IndexError:
            raise IndexError(
                f"Command index out of range. (max index: {len((self))})"
            ) from None
