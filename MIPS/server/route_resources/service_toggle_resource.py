from flask_restful import Resource, reqparse
from core.src.service_type import ServiceType

service_toggle_args = reqparse.RequestParser()
service_toggle_args.add_argument("service", type=str,
                                 help="Valid service type is needed: wordpress, joomla, ssh or phpmyadmin.",
                                 required=True)
service_toggle_args.add_argument("toggle", type=bool,
                                 help="Toggle boolean value is needed: 1 for start, 0 for stopping a service.",
                                 required=True)


class ServiceToggle(Resource):
    def __init__(self, ssh, phpmyadmin, joomla, wordpress):
        self.services = {"ssh": ssh, "phpmyadmin": phpmyadmin,
                         "joomla": joomla, "wordpress": wordpress}

    def post(self):
        args = service_toggle_args.parse_args()
        service_type = args.service.lower()
        if service_type in self.services:
            if not(self.services[service_type].isrunning) and args.toggle:
                self.services[service_type].start()
                return 200 if self.services[service_type].isrunning else 400
            elif self.services[service_type].isrunning and not(args.toggle):
                self.services[service_type].stop()
                return 200 if not self.services[service_type].isrunning else 400
            else:
                return {"message": f"Something went wrong: {service_type}"}, 400
        else:
            return {"message": f"Invalid service type: {service_type}"}, 400
