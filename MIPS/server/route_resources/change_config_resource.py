from flask_restful import Resource, reqparse
from core.src.pubsub_config.publisher_config import PublisherConfig

change_config_args = reqparse.RequestParser()
change_config_args.add_argument("threshold", type=int, help="Threshold of requests is required and needs to be an int.",
                                required=True)
change_config_args.add_argument("time_window", type=int, help="Time window of requests is required and needs to be an "
                                                              "int.",
                                required=True)
change_config_args.add_argument("block_time", type=int, help="Block time of requests is required and needs to be an "
                                                             "int.",
                                required=True)


class ChangeConfig(Resource):
    def __init__(self, pc: PublisherConfig):
        self.pc = pc

    def post(self):
        args = change_config_args.parse_args()

        if args.threshold < 0 or args.time_window < 0 or args.block_time < 0:
            return {'message': 'threshold, time window and block time need to be greater than or equal to 0.'}, 400

        self.pc.notify(threshold=args.threshold, time_window=args.time_window, block_time=args.block_time)

        return 200
