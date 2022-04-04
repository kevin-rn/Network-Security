import re
from datetime import datetime, date
from typing import List
from ..service_interface import ServiceInterface
from ..db.entities.log_record import LogRecord
from ..service_type import ServiceType


class SSHService(ServiceInterface):
    """
    SSH service that implements the parse method
    """

    def _parse(self, loglines: str) -> List["LogRecord"]:
        """
        Parser for ssh
        """
        result = list()
        for line in loglines:
            s = re.search("sshd\[.*\]: Failed password.*from (.+?) port", line)
            if s:
                split_str = line.split()
                print(split_str)
                _timestamp = str(date.today().year) + " " + \
                    " ".join(split_str[0:3])
                _timestamp = datetime.strptime(_timestamp, '%Y %b %d %H:%M:%S')
                _ip = s.group(1)
                result.append(
                    LogRecord(
                        timestamp=_timestamp,
                        ip=_ip,
                        service=ServiceType.ssh.value
                    )
                )

        return result
