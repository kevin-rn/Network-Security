from datetime import datetime
import time
from typing import List
from ..service_interface import ServiceInterface
from ..db.entities.log_record import LogRecord
from ..service_type import ServiceType


class JoomlaService(ServiceInterface):
    """
    Joomla service that implements the parse method
    """

    def _parse(self, loglines: str) -> List['LogRecord']:
        """
        Parser for Joomla
        """
        result = list()
        match_str = ["joomlafailure", "Username and password do not match"]

        for log in loglines:
            if all(line in log for line in match_str):
                split_str = log.split()
                print(split_str)
                ip_address = split_str[2]
                if ip_address == "::1":
                    ip_address = "127.0.0.1"

                now_timestamp = time.time()
                offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
                utc_timestamp = datetime.strptime(split_str[0].split("+", 1)[0], '%Y-%m-%dT%H:%M:%S') 
                timestamp = utc_timestamp + offset
                result.append(
                    LogRecord(
                        timestamp=timestamp, 
                        ip=ip_address, 
                        service=ServiceType.joomla.value
                    )
                )
        return result
