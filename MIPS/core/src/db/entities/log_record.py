from sqlalchemy import Integer, String, Column, DateTime
from ..db import Base
from datetime import datetime

"""
A class representing the log records.
"""


class LogRecord(Base):
    __tablename__ = "log_records"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    service = Column(String, nullable=False, index=True)

    def __repr__(self):
        return f"<LogRecord(id={self.id}, ip={self.ip}, timestamp={self.timestamp}, service={self.service})>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}