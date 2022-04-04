from flask_restful import Resource
from core.src.pubsub_config.publisher_config import PublisherConfig


class ConfigState(Resource):
    def __init__(self, pc: PublisherConfig):
        self.pc = pc

    def get(self):
        resp = list()
        for c in self.pc.subscribers:
            resp.append(
                {
                    "threshold": c.threshold,
                    "time_window": c.time_window,
                    "block_time": c.block_time
                }
            )
        return resp, 200
