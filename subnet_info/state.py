"""
State for SubnetInfo module.
"""

__all__ = ("UserDevice",)

import os
import socket
from contextlib import contextmanager

import requests


class UserDevice:
    """
    Store user local/public IP address and user operating system name.
    """

    def __init__(self) -> None:
        self._local_ip: str = ""
        self._public_ip: str = ""
        self._system_name: str = ""

    @staticmethod
    @contextmanager
    def socket_context(*args, **kwargs):
        """
        Built for making sure if raw sockets after operation are closed.
        """
        s = socket.socket(*args, **kwargs)
        try:
            yield s
        finally:
            s.close()

    @property
    def system_name(self) -> str:
        """
        It is important to define if user use Linux or other system.

        :return: Information about what system the user is using, for example:
        'nt' is Windows | 'posix' is Linux
        :rtype: str
        """
        return os.name

    @property
    def local_ip(self) -> str:
        """
        Here the module collects information about the user's local ip address.
        User can get this address by using SubnetInfo class.

        :return: User local IP address
        :rtype: str
        """
        with self.socket_context(socket.AF_INET, socket.SOCK_DGRAM) as _socket:
            _socket.connect(("8.8.8.8", 80))
            return _socket.getsockname()[0]

    @property
    def public_ip(self) -> str:
        """
        Here the module collects information about the user's public ip address.
        User can get this address by using SubnetInfo class.

        :return: User public IP address
        :rtype: str
        """
        try:
            return requests.get("https://api.ipify.org").text
        except requests.exceptions.ConnectionError:
            return "Unknown"
