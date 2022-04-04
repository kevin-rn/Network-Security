from enum import Enum


class ServiceType(Enum):
    """
    Leagal services that have an instance of ServiceInstance implemented
    """
    ssh = "SSH"
    phpmyadmin = "phpMyAdmin"
    joomla = "Joomla"
    wordpress = "Wordpress"
