from datetime import datetime, date
from typing import List
from ..service_interface import ServiceInterface
from ..db.entities.log_record import LogRecord
from ..service_type import ServiceType

class phpMyAdminService(ServiceInterface):
    """
    phpMyAdmin service that implements the parse method
    """

    def _parse(self, loglines: str) -> List["LogRecord"]:
        """
        Parser for phpMyAdmin
        """
        result = list()
        for line in loglines:
            if "phpMyAdmin" in line:
                split_str = line.split()
                print(split_str)

                # Format timestamp to be a datetime object: Feb 20 23:21:13 --> 2022-02-20 23:21:13
                timestamp = str(date.today().year) + " " + " ".join( split_str[0:3])
                datetime_object = datetime.strptime(timestamp, '%Y %b %d %H:%M:%S')
                ip_address = split_str[10].rstrip('\n')

                result.append(
                    LogRecord(
                        timestamp=datetime_object, 
                        ip=ip_address, 
                        service=ServiceType.phpmyadmin.value
                    )
                )
        return result
            
