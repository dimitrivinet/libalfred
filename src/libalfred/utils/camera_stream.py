import logging
import pickle
import threading
import time
from collections import deque
from typing import Optional, Tuple

import numpy as np
from libalfred.wrapper.mixins.redis_user import RedisUserMixin

logger = logging.getLogger(__name__)
_lock = threading.Lock()


class StreamCamThread(threading.Thread, RedisUserMixin):
    """Thread to stream with the realsense"""

    def __init__(
        self,
        camera_feed: str = "device-data-realsense",
        buffer_size: int = 1,
        redis_host: str = "redis",
        redis_port: int = 6379,
        redis_password: str = None,
        daemon: bool = True,
        **kwargs
    ) -> None:
        super().__init__(daemon=daemon, **kwargs)

        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password

        self.camera_feed = camera_feed
        self.buffer: deque = deque(maxlen=buffer_size)
        self._frame_size = (0, 0)
        self.frame_ready = False
        self._stop = threading.Event()

        self.count = -1

    def run(self):
        self.connect_redis()
        self.pubsub.subscribe(self.camera_feed)
        while True:
            message = self.pubsub.get_message()
            if not message:
                time.sleep(0.001)
                continue
            if self._stop.is_set():
                break

            frame: np.ndarray = pickle.loads(message["data"])
            self._frame_size = frame.shape
            self.buffer.append(frame)
            self.frame_ready = True

    @property
    def frame_size(self) -> Tuple[int, int]:
        """Get frame size as tuple."""

        with _lock:
            return self._frame_size

    def get_frame(self) -> Optional[np.ndarray]:
        """Return the last streamed frame"""

        with _lock:
            if not self.frame_ready:
                return None
            frame = self.buffer[-1]
            self.frame_ready = False
        return frame

    def stop(self):
        """Stop cam thread."""

        self._stop.set()

    def __iter__(self):
        self.count = -1  # reset number of frames returned by iterator
        return self

    def __next__(self):
        self.count += 1
        if self._stop.is_set():
            raise StopIteration

        frame = self.get_frame()
        while frame is None:
            frame = self.get_frame()

        return self.camera_feed, frame
