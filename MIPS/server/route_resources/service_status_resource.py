from flask_restful import Resource
from core.src.service_type import ServiceType


class ServiceStatus(Resource):
    def __init__(self, ssh, phpmyadmin, joomla, wordpress):
        self.ssh = ssh
        self.phpmyadmin = phpmyadmin
        self.joomla = joomla
        self.wordpress = wordpress

    def get(self):
        try:
            return {
                ServiceType.ssh.value: self.ssh.isrunning,
                ServiceType.phpmyadmin.value: self.phpmyadmin.isrunning,
                ServiceType.joomla.value: self.joomla.isrunning,
                ServiceType.wordpress.value: self.wordpress.isrunning
            }, 200
        except Exception as e:
            print(e)
            return {"message": f"Server Error Occurred"}, 500
