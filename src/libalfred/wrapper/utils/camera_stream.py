import json
import logging
import pickle
import time
import threading
from collections import deque
from typing import Optional

from libalfred.wrapper import exceptions
from libalfred.wrapper.mixins.redis_user import RedisUserMixin

logger = logging.getLogger(__name__)
_lock = threading.Lock()


class StreamCamThread(threading.Thread,RedisUserMixin):
    """Thread to stream with the realsense"""
    def __init__(self, camera_feed: str, buffer_size: int, daemon: bool=True, redis_host: str = "redis", redis_port: int = 6379, redis_password: str = None,) -> None:
        super().__init__()

        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password

        self.connect_redis()
        self.pubsub.subscribe(camera_feed)

        self.buffer=deque(maxlen=buffer_size)
        self.frame_ready=False
    
    def run(self):
        while True:
            message=self.pubsub.get_message()
            if not message:
                time.sleep(0.001)
                continue
            frame = pickle.loads(message["data"])
            self.buffer.append(frame)
            self.frame_ready=True
    
    def get_frame(self):
        """Return the last streamed frame"""
        with _lock:
            if not self.frame_ready:
                return None
            frame=self.buffer[-1]
            self.frame_ready=False
        return frame



