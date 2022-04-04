from datetime import datetime, date
from typing import List
from ..service_interface import ServiceInterface
from ..db.entities.log_record import LogRecord
from ..service_type import ServiceType

class wordpressService(ServiceInterface):
    """
    Wordpress service that implements the parse method
    """
    def _parse(self, loglines: str) -> List["LogRecord"]:
        """
        Parser for Wordpress
        """
        result = list()
        match_str = ["POST", "wordpress", "wp-login", "200"] 

        for log in loglines:
            if all(line in log for line in match_str):
                split_str = log.split()
                print(split_str)
                ip_address = split_str[0]
                if ip_address == "::1":
                    ip_address = "127.0.0.1"
                receivedTime = split_str[3][1:]
                timeStamp = datetime.strptime(receivedTime, '%d/%b/%Y:%H:%M:%S')

                result.append(
                    LogRecord(
                        timestamp = timeStamp,
                        ip = ip_address,
                        service = ServiceType.wordpress.value
                    )
                )
                    
        return result
