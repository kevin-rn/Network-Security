from datetime import datetime, timedelta
from typing import List, Tuple
from .config import Config
from .db.entities.log_record import LogRecord
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from os.path import exists
from core.src.db.crud.crud_log_record import distinct_ip_counts_between


class DbObserver:
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

    def start(self) -> "DbObserver":
        """
        Create an observer instance to monitor the log log_path and call event_handler
        """
        if not exists(self.log_path):
            return self
        observer = Observer()
        event_handler = LoggingEventHandler()
        event_handler.on_modified = self._on_modified
        observer.schedule(event_handler, self.log_path)
        self.observer = observer
        observer.start()
        self.isrunning = True
        print("db observer started")
        return self

    # Method of observing using watchdog, still needs to be rewritten and not sure if applicable on databases
    def set_config(self, config) -> "DbObserver":
        """
        Set the config object
        """
        self.config = config
        return self

    def set_ban_method(self, ban_callback) -> "DbObserver":
        """
        Set a callback method to be called when there is a list of ip addresses to be blocked
        """
        self.ban_callback = ban_callback
        return self

    def stop(self) -> None:
        """
        If the observer class is already started, stop it and change the service status to not running
        """
        if self.observer != None:
            self.observer.stop()
            self.observer.join()
            self.isrunning = False

    def _on_modified(self, event) -> None:
        """
        What should happen when the db file changes
        """
        if event.src_path != self.log_path or not exists(self.log_path):
            return

        self.do()

    def do(self) -> None:
        """
        Perform necessary steps to ban ip addresses or add them to db
        """
        # Filter IP records based on the config
        timewindow = self.config.time_window
        block_time = self.config.block_time
        threshold = self.config.threshold

        count_vals_ips: List[Tuple[LogRecord, int]] = distinct_ip_counts_between(
            datetime.now() - timedelta(minutes=timewindow), datetime.now()
        )

        for tup in count_vals_ips:
            lr = tup[0]
            count = tup[1]
            if count >= threshold:
                if self.ban_callback is not None:
                    self.ban_callback(lr.ip, block_time, lr.service)
                else:
                    print("[DbObserver] WARN: ban callback is not set!")
