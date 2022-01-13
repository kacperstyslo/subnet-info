"""
All SubnetInfo methods available for end user.
"""

__all__ = (
    "SubnetSingleton",
    "SubnetInfo",
)

import os
from math import pow
from typing import List, Optional

from .helpers import SubnetInfoHelpers


class SubnetSingleton(type):
    """
    Created to make sure if only one SubnetInfo instance exists.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SubnetInfo(metaclass=SubnetSingleton):
    """
    This stores all methods witch you can get information about subnet.
    This methods will be available to the end user.
    """

    def __init__(self) -> None:
        self._subnet_info_helpers = SubnetInfoHelpers()

    def get_local_ip(self) -> str:
        """
        Get device local IP address.

        :return: Device local IP address.
        :rtype: str
        """
        return self._subnet_info_helpers.user_device.local_ip

    def get_public_ip(self) -> str:
        """
        Get device public IP address.

        :return: Device public IP address.
        :rtype: str
        """
        return self._subnet_info_helpers.user_device.public_ip

    def get_subnet_mask(self) -> str:
        """
        Get the subnet mask where device is currently connected.

        :return: Subnet mask from ipconfig
        :rtype: str
        """
        ip_conf = self._subnet_info_helpers.get_ip_config()
        while True:
            line = ip_conf.stdout.readline()
            if self._subnet_info_helpers.user_device.local_ip.encode() in line:
                break
        if os.name == "nt":
            return (
                ip_conf.stdout.readline()
                .rstrip()
                .split(b":")[-1]
                .replace(b" ", b"")
                .decode()
            )
        return line.rstrip().split(b":")[-1].replace(b" ", b"").decode()

    def calculate_cidr(self, subnet_mask: Optional[str] = "") -> int:
        """
        Calculate CIDR based on subnet mask and subnet blocks.

        :param subnet_mask: Provided subnet_mask, for example '255.255.255.0'
        :type subnet_mask: str
        :return: CIDR of provided subnet mask
        :rtype: int
        """
        cidr: int = 0
        _subnet_block = self._subnet_info_helpers.generate_subnet_block()
        if not subnet_mask:
            subnet_mask = self.get_subnet_mask()
        for num in subnet_mask.split("."):
            cidr += _subnet_block.get(int(num), 0)
        return cidr

    def calculate_hosts_amount(self, cidr: int = None, subnet_mask: str = "") -> int:
        """
        Calculate how many hosts can be in subnet. To calculate hosts amount user
        must provide CIDR or subnet mask.

        :param cidr: CIDR for example 32 not /32
        :type cidr: int
        :param subnet_mask: Subnet mask for example 255.255.255.0
        :type subnet_mask: str
        :return: Amount of hosts in chosen subnet
        :rtype: int
        """
        if subnet_mask:
            cidr = self.calculate_cidr(subnet_mask)
        return int(abs(pow(2, 32 - cidr) - 2))

    def get_first_ip_address(self, ip_address: str, subnet_mask: str) -> str:
        """
        Get the first address in the subnet by using the given IP address and subnet
        mask.

        :param ip_address: IP address for example '192.168.0.1'.
        :type ip_address: str
        :param subnet_mask: Subnet mask for example '255.255.255.0'.
        :type subnet_mask: str
        :return: First IP address in chosen subnet.
        :rtype: str
        """
        return self._subnet_info_helpers.template_for_first_and_last_ip_address(
            ip_address, subnet_mask
        )

    def get_last_ip_address(self, ip_address: str, subnet_mask: str) -> str:
        """
        Get the last address in the subnet by using the given IP address and subnet
        mask.

        :param ip_address: IP address for example '192.168.0.1'.
        :type ip_address: str
        :param subnet_mask: Subnet mask for example '255.255.255.0'.
        :type subnet_mask: str
        :return: Last IP address in chosen subnet.
        :rtype: str
        """
        return self._subnet_info_helpers.template_for_first_and_last_ip_address(
            ip_address, subnet_mask
        )

    def generate_all_ip_addr(self, ip_address: str, subnet_mask: str) -> List[str]:
        """
        Generate all IP addresses in chosen subnet based on provided IP address and
        subnet mask.

        :param ip_address: IP address for example '192.168.0.1'.
        :type ip_address: str
        :param subnet_mask: Subnet mask for example '255.255.255.0'.
        :type subnet_mask: str
        :return: All ip addresses in chosen subnet. For example ['192.168.0.1'] for
        subnet /32 and IP address '192.168.0.1'.
        :rtype: List[str]
        """

        first_ip: List[int] = [
            int(octet)
            for octet in self.get_first_ip_address(ip_address, subnet_mask).split(".")
        ]
        last_ip: List[int] = [
            int(octet)
            for octet in self.get_last_ip_address(ip_address, subnet_mask).split(".")
        ]

        ip_addresses: List[str] = []
        for octet_1 in range(first_ip[0], last_ip[0] + 1):
            for octet_2 in range(first_ip[1], last_ip[1] + 1):
                for octet_3 in range(first_ip[2], last_ip[2] + 1):
                    for octet_4 in range(first_ip[3], last_ip[3] + 1):
                        ip_addresses.append(f"{octet_1}.{octet_2}.{octet_3}.{octet_4}")

        return ip_addresses
