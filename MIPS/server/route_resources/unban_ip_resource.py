from flask_restful import Resource, reqparse
import ipaddress
from core.src.nft_ban import unban_ip

unban_ip_args = reqparse.RequestParser()
unban_ip_args.add_argument("ip", type=str, help="IP address is required and needs to be provided as a string.",
                           required=True)


class UnbanIP(Resource):
    def post(self):
        args = unban_ip_args.parse_args()

        try:
            ipaddress.ip_address(args.ip)
        except ValueError as ve:
            return {"message": {"ip": "The IP address is not valid!"}}, 400

        try: 
            unban_ip(args.ip)
        except:
            return {"message": {"ip": "Vailed to unban ip"}}, 400
        return 200
