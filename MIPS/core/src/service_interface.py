from typing import List
from .config import Config
from .db.entities.log_record import LogRecord
from abc import ABC, abstractmethod
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from os.path import exists, getsize
from core.src.db.crud.crud_log_record import insert_multiple_log_records

class ServiceInterface(ABC):
    """
    This class is an interface that should be extended by each service that needs to be implemented
    """

    def __init__(self, log_path: str, config=None, ban_callback=None) -> None:
        """
        Initializition of the class
        """
        self.isrunning = False
        self._last_position = 0
        self.observer = None
        self.log_path = log_path
        self.ban_callback = ban_callback
        if config is None:
            self.config = Config()
        else:
            self.config = config

    def start(self) -> "ServiceInterface":
        """
        Create an observer instance to monitor the log log_path and call event_handler
        """
        if not exists(self.log_path):
            return self
        self.jumptolastline()
        observer = Observer()
        event_handler = LoggingEventHandler()
        event_handler.on_modified = self._on_modified
        observer.schedule(event_handler, self.log_path)
        self.observer = observer
        observer.start()
        self.isrunning = True
        print("service started")
        return self

    def set_config(self, config) -> "ServiceInterface":
        """
        Set the config object
        """
        self.config = config
        return self

    def stop(self) -> None:
        """
        If the observer class is already started, stop it and change the service status to not running
        """
        if self.observer != None:
            self.observer.stop()
            self.observer.join()
            self.isrunning = False
            return True

        return False

    def jumptolastline(self):
        """
        Move the cursor to the last line
        """
        self._last_position = getsize(self.log_path)

    def _on_modified(self, event) -> None:
        """
        What should happen when the log file changes
        """
        if event.src_path != self.log_path or not exists(self.log_path):
            return
        if self._last_position > getsize(self.log_path):
            self.jumptolastline()

        with open(self.log_path) as f:
            # Read the lines changes
            f.seek(self._last_position)
            lines = f.readlines()
            self._last_position = f.tell()
            self.do(lines)

    def do(self, lines: str) -> None:
        """
        Perform necessary steps to ban ip addresses or add them to db
        """
        all_ips_list = self._parse(lines)  # Read all IP records from log
        # Filter IP records based on the config
        insert_multiple_log_records(all_ips_list)

    @abstractmethod
    def _parse(self, loglines: str) -> List["LogRecord"]:
        """
        The content should be parsed.
        The output should be a list of LogRecord
        This method should be overwritten in the extended classes
        """
        raise NotImplementedError("Parse Not Implemented")
