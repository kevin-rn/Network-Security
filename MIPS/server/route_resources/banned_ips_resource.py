from flask_restful import Resource
from core.src.nft_ban import get_banned_ips
import json
from datetime import datetime, date


class BannedIPs(Resource):
    def get(self):
        entries = get_banned_ips()
        res = []
        for entry in entries:
            dict_entry = entry.__dict__
            jsonified_entry = json.dumps(
                dict_entry, sort_keys=True, default=self.json_serial)
            res.append(jsonified_entry)
        return res

    @staticmethod
    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Type {obj} not serializable")
