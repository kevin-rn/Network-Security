import time
from src.services.joomla_service import JoomlaService
from src.services.phpmyadmin_service import phpMyAdminService
from src.services.wordpress_service import wordpressService
from src.services.ssh_service import SSHService
from src.config import Config
from src.nft_ban import clean, init, create_ban_thread
from src.db_observer import DbObserver
from src.db.db import SQLALCHEMY_DB_PATH


def main():
    conf = Config()

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

    wordpress = wordpressService("/var/log/apache2/other_vhosts_access.log") \
        .set_config(conf) \
        .start()

    # ban_method is a callback function that accepts  list[LogRecord] as input and bans those ip addresses
    db_observer = DbObserver(SQLALCHEMY_DB_PATH) \
        .set_config(conf) \
        .set_ban_method(create_ban_thread) \
        .start()

    try:
        while True:
            time.sleep(1)
    finally:
        ssh.stop()
        joomla.stop()
        phpMyAdmin.stop()
        wordpress.stop()
        db_observer.stop()


if __name__ == '__main__':
    main()
