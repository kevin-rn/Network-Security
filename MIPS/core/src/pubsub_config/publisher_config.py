from typing import List

from core.src.config import Config


class PublisherConfig:

    def __init__(self):
        self.subscribers: List["Config"] = []

    def subscribe(self, config: Config):
        self.subscribers.append(config)

    def notify(self, threshold: int, time_window: int, block_time: int):
        if threshold < 0 or time_window < 0 or block_time < 0:
            return
        for s in self.subscribers:
            s.threshold = threshold
            s.time_window = time_window
            s.block_time = block_time
