# -*- coding: UTF-8 -*-
"""
Proxy Server representation
"""
import socket

from dataclasses import dataclass
from enum import Enum
from typing import Optional


def _is_ip_address(value):
    try:
        socket.inet_aton(value)
        return True
    except socket.error:
        return False


class ProxyServerType(Enum):
    """ Type of proxy server """

    HTTP = 'http'
    HTTPS = 'https'
    SOCKS4 = 'socks4'
    SOCKS5 = 'socks5'


@dataclass
class ProxyServer:
    """ Represents Proxy server """

    address: str
    proxy_type: ProxyServerType = ProxyServerType.HTTP
    port: int = 80
    login: Optional[str] = None
    password: Optional[str] = None

    def __post_init__(self):
        proxy_string = self.address
        if '://' in proxy_string:
            proxy_type, proxy_string = proxy_string.split('://')
            self.proxy_type = ProxyServerType(proxy_type.lower())

        if '@' in proxy_string:
            credentials, proxy_string = proxy_string.split('@')
            self.login, self.password = credentials.split(':', maxsplit=1)

        if ':' in proxy_string:
            self.address, port = proxy_string.split(':', maxsplit=1)
            self.port = int(port)
        else:
            self.address = proxy_string

    def __str__(self):
        return self.get_string(including_type=True)

    def get_string(self, including_type=False):
        """ Get proxy as string like [<type>://][<login>:<password>@]<addr>:<port> """

        proxy_string = ''
        if including_type:
            proxy_string += self.proxy_type.value + '://'

        if self.login:
            proxy_string += self.login + ':' + self.password + '@'

        return proxy_string + self.address + ':' + str(self.port)

    def get_ip_address(self):
        """ Get IP address by hostname """

        if not _is_ip_address(self.address):
            return socket.gethostbyname(self.address)
        return self.address
