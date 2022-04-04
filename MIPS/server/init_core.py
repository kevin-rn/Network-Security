from core.src.services.joomla_service import JoomlaService
from core.src.services.phpmyadmin_service import phpMyAdminService
from core.src.services.ssh_service import SSHService
from core.src.config import Config
from core.src.services.wordpress_service import wordpressService
from core.src.pubsub_config.publisher_config import PublisherConfig
from core.src.nft_ban import clean, init, create_ban_thread
from core.src.db.db import SQLALCHEMY_DB_PATH
from core.src.db_observer import DbObserver
from core.src.db.crud.crud_log_record import delete_all_log_records

pc = PublisherConfig()
conf = Config()
pc.subscribe(conf)


def init_core():
    global conf

    clean()
    init()

    ssh = SSHService("/var/log/auth.log") \
        .set_config(conf) \
        .start()

    joomla = JoomlaService("/var/www/html/joomla/administrator/logs/error.php") \
        .set_config(conf) \
        .start()

    phpMyAdmin = phpMyAdminService("/var/log/auth.log") \
        .set_config(conf) \
        .start()

    wordpress = wordpressService("/var/log/apache2/access.log") \
        .set_config(conf) \
        .start()

    # ban_method is a callback function that accepts  list[LogRecord] as input and bans those ip addresses
    db_observer = DbObserver(SQLALCHEMY_DB_PATH) \
        .set_config(conf) \
        .set_ban_method(create_ban_thread) \
        .start()
    
    assert ssh is not None
    assert joomla is not None
    assert phpMyAdmin is not None
    assert wordpress is not None
    assert db_observer is not None

    return ssh, joomla, phpMyAdmin, wordpress, db_observer


def stop_core(ssh, joomla, phpMyAdmin, wordpress, db_observer):
    assert ssh is not None
    assert joomla is not None
    assert phpMyAdmin is not None
    assert wordpress is not None
    assert db_observer is not None

    ssh.stop()
    joomla.stop()
    phpMyAdmin.stop()
    wordpress.stop()
    db_observer.stop()
