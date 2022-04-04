from flask import Flask
from flask_restful import Api
from core.src.db.db import create_tables
from core.src.db.entities.log_record import \
    LogRecord  # this has to be imported so that it gets attached to the Base class of DB
from server.route_resources.unban_ip_resource import UnbanIP
from server.route_resources.banned_ips_resource import BannedIPs
from server.route_resources.change_config_resource import ChangeConfig
from server.route_resources.service_toggle_resource import ServiceToggle
from server.route_resources.service_status_resource import ServiceStatus
from server.route_resources.current_config_state_resource import ConfigState
from core.src.db.crud.crud_log_record import *
from server.init_core import pc, init_core, stop_core
from datetime import datetime, timedelta
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

USE_DEBUG = True
SERVER_HOST_IP = '127.0.0.1'
SERVER_HOST_PORT = 5000


def test_db_for_debug():
    t = datetime.now()
    dt = timedelta(minutes=1)
    lst = [
        LogRecord(ip="192.2.2.2", timestamp=t - dt -
                  dt - dt - dt - dt - dt, service="ssh"),
        LogRecord(ip="192.2.2.2", timestamp=t - dt -
                  dt - dt - dt - dt, service="Joomla"),
        LogRecord(ip="192.2.2.2", timestamp=t -
                  dt - dt - dt - dt, service="phpMyAdmin"),
        LogRecord(ip="8.8.8.8", timestamp=t - dt - dt - dt, service="ssh"),
        LogRecord(ip="8.8.8.8", timestamp=t - dt - dt, service="ssh"),
        LogRecord(ip="1.1.1.1", timestamp=t - dt, service="phpMyAdmin"),
        LogRecord(ip="2.2.2.2", timestamp=t, service="WordPress"),
    ]
    print(insert_multiple_log_records(lst))
    print(get_log_records_between(t - dt - dt - dt - dt - dt - dt, t))
    print(distinct_ip_counts_between(t - timedelta(minutes=100), t))
    print(delete_log_records_between(t - dt - dt - dt - dt - dt - dt, t))
    print(distinct_ip_counts_between(t - timedelta(minutes=100), t))
    print(get_log_records())

    t = datetime.now()
    lst2 = [
        LogRecord(ip="9.9.9.9", timestamp=t - dt -
                  dt - dt - dt - dt - dt, service="ssh"),
        LogRecord(ip="7.7.7.7", timestamp=t - dt -
                  dt - dt - dt - dt, service="phpMyAdmin"),
        LogRecord(ip="7.7.7.7", timestamp=t - dt -
                  dt - dt - dt, service="phpMyAdmin"),
        LogRecord(ip="7.7.7.7", timestamp=t - dt -
                  dt - dt, service="WordPress"),
        LogRecord(ip="1.1.1.1", timestamp=t - dt, service="ssh"),
    ]
    print("insert_multiple_log_records(lst2)",
          insert_multiple_log_records(lst2))
    print("get_last_record_log()", get_last_record_log())
    print("get_log_records()", get_log_records())
    print("delete_log_records_between(t - dt - dt - dt, t)",
          delete_log_records_between(t - dt - dt - dt, t))
    print("delete_log_record_by_colnames",
          delete_log_record_by_colnames(ip="9.9.9.9"))
    print("insert_log_record_given_cols", insert_log_record_given_cols(
        ip="9.9.9.9", timestamp=t - dt, service="ssh"))
    print("distinct_ip_counts_between(t-timedelta(minutes=100), t)",
          distinct_ip_counts_between(t - timedelta(minutes=100), t))
    print("distinct_ip_counts_between(t-dt-dt-dt-dt, t)",
          distinct_ip_counts_between(t - dt - dt - dt - dt, t))


if __name__ == '__main__':
    create_tables()
    # test_db_for_debug()
    ssh, joomla, phpMyAdmin, wordpress, db_observer = init_core()
    
    api.add_resource(BannedIPs, "/api/v1/get_banned_ips")
    api.add_resource(
        ChangeConfig,
        "/api/v1/change_config",
        resource_class_kwargs={'pc': pc}
    )
    api.add_resource(UnbanIP, "/api/v1/unban")
    api.add_resource(
        ServiceToggle,
        "/api/v1/toggle_service",
        resource_class_kwargs={
            'ssh': ssh,
            'phpmyadmin': phpMyAdmin,
            'joomla': joomla,
            'wordpress': wordpress
        }
    )
    api.add_resource(
        ServiceStatus,
        "/api/v1/service_status",
        resource_class_kwargs={
            'ssh': ssh,
            'phpmyadmin': phpMyAdmin,
            'joomla': joomla,
            'wordpress': wordpress
        }
    )
    api.add_resource(
        ConfigState,
        "/api/v1/config_state",
        resource_class_kwargs={'pc': pc}
    )

    app.run(host=SERVER_HOST_IP, port=SERVER_HOST_PORT,
            debug=USE_DEBUG, use_reloader=False)

    stop_core(ssh, joomla, phpMyAdmin, wordpress, db_observer)
