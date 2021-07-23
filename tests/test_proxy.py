# -*- coding: UTF-8 -*-
"""
Proxy tests
"""

from unicaps.proxy import ProxyServer, ProxyServerType


def test_proxy_from_string():
    proxy = ProxyServer('http://login:password@address:8080')

    assert proxy.address == 'address'
    assert proxy.proxy_type == ProxyServerType.HTTP
    assert proxy.port == 8080
    assert proxy.login == 'login'
    assert proxy.password == 'password'


def test_proxy_wo_auth_from_string():
    proxy = ProxyServer('https://address:8080')

    assert proxy.address == 'address'
    assert proxy.proxy_type == ProxyServerType.HTTPS
    assert proxy.port == 8080
    assert proxy.login is None
    assert proxy.password is None


def test_proxy_address_only():
    proxy = ProxyServer('address')

    assert proxy.address == 'address'
    assert proxy.proxy_type == ProxyServerType.HTTP
    assert proxy.port == 80
    assert proxy.login is None
    assert proxy.password is None


def test_proxy_all():
    proxy = ProxyServer('address', ProxyServerType.SOCKS4, 80, 'login', 'password')

    assert proxy.address == 'address'
    assert proxy.proxy_type == ProxyServerType.SOCKS4
    assert proxy.port == 80
    assert proxy.login == 'login'
    assert proxy.password == 'password'


def test_proxy_to_string():
    proxy = ProxyServer('address', ProxyServerType.SOCKS5, 80, 'login', 'password')

    assert str(proxy) == 'socks5://login:password@address:80'
