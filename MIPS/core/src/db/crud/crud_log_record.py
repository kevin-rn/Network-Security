from datetime import datetime
from typing import List, Tuple
from ..db import DbSession
from ..entities.log_record import LogRecord
from sqlalchemy import or_, desc, func

"""
Copies LogRecord entries in a new LogRecord object so that 
the LogRecords become independent from the session used to fetch them from db.
NOTE: This is done so that the fetched LogRecords can still be used after session is closed  
"""


def copy_log_record(lr: LogRecord):
    return LogRecord(id=lr.id, ip=lr.ip, timestamp=lr.timestamp, service=lr.service)


"""
Insert multiple log record instances at once.

"""


def insert_multiple_log_records(log_records: List[LogRecord]) -> bool:
    try:
        with DbSession() as session:
            session.add_all(log_records)
        return True
    except Exception as e:
        print(e)
        return False


"""
Inserts a log record given the required args
"""


def insert_log_record_given_cols(ip: str, timestamp: "datetime", service: str) -> bool:
    try:
        with DbSession() as session:
            session.add(LogRecord(ip=ip, timestamp=timestamp, service=service))
        return True
    except Exception as e:
        print(e)
        return False


"""
Inserts a log record object
"""


def insert_log_record(lr: LogRecord) -> bool:
    try:
        with DbSession() as session:
            session.add(lr)
        return True
    except Exception as e:
        print(e)
        return False


"""
Delete a log record given a column name. Atleast one column name must be given 
"""


def delete_log_record_by_colnames(
        ip: str = None, timestamp: "datetime" = None, service: str = None
) -> int:
    try:
        if not ip and not timestamp and not service:
            return False
        with DbSession() as session:
            res = session.query(LogRecord).filter(
                or_(
                    LogRecord.ip == ip,
                    LogRecord.timestamp == timestamp,
                    LogRecord.service == service,
                )
            ).delete(synchronize_session=False)

        return res
    except Exception as e:
        print(e)
        return False


"""
Delete a log record given the log record object.
"""


def delete_log_record(lr: LogRecord) -> int:
    return delete_log_record_by_colnames(lr.ip, lr.timestamp, lr.service)


"""
Delete all log records.
"""


def delete_all_log_records() -> int:
    try:
        with DbSession() as session:
            nr_deleted_rows = session.query(LogRecord).delete(synchronize_session=False)
        return nr_deleted_rows
    except Exception as e:
        print(e)
        return -1


"""
Fetches all log records currently present in the database.
OPTIONAL: result can be limited using `limit` arg. Default: 0 = all records.
"""


def get_log_records(limit: int = 0) -> List[LogRecord]:
    try:
        res_lrs = []
        with DbSession() as session:
            if limit == 0:
                for lr in session.query(LogRecord).all():
                    res_lrs.append(copy_log_record(lr))
            else:
                for lr in session.query(LogRecord).limit(limit).all():
                    res_lrs.append(copy_log_record(lr))
        return res_lrs
    except Exception as e:
        print(e)
        return []


"""
Fetches only the last log record from the database.
"""


def get_last_record_log() -> LogRecord:
    try:
        with DbSession() as session:
            res = copy_log_record(session.query(LogRecord).order_by(desc(LogRecord.timestamp)).first())
        return res
    except Exception as e:
        print(e)
        return None


"""
Get logs between certain date times.
Returns: list of RecordLogs between two date times.
"""


def get_log_records_between(_from: "datetime", _to: "datetime") -> List[LogRecord]:
    try:
        res_lrs = []
        with DbSession() as session:
            query_res = session.query(LogRecord).filter(
                LogRecord.timestamp.between(_from, _to)
            )
            for lr in query_res:
                res_lrs.append(copy_log_record(lr))
        return res_lrs
    except Exception as e:
        print(e)
        return []


"""
Delete log records between certain date times.
Returns: number of records deleted.
"""


def delete_log_records_between(_from: "datetime", _to: "datetime") -> int:
    try:
        with DbSession() as session:
            nr_recs_deleted = (
                session.query(LogRecord)
                    .filter(LogRecord.timestamp.between(_from, _to))
                    .delete(synchronize_session=False)
            )
        return nr_recs_deleted
    except Exception as e:
        print(e)
        return -1


"""
Fetches distinct IP counts in certain interval
"""


def distinct_ip_counts_between(_from: "datetime", _to: "datetime") -> List[Tuple[LogRecord, int]]:
    try:
        res = []
        with DbSession() as session:
            query_res = session.query(LogRecord, func.count(LogRecord.ip)).filter(
                LogRecord.timestamp.between(_from, _to)
            ).group_by(LogRecord.ip)

            for tup in query_res:
                res.append(
                    (copy_log_record(tup[0]), tup[1])
                )
        return res
    except Exception as e:
        print(e)
        return []
