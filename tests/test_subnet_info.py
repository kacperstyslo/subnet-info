"""
SubnetInfo tests.
"""

__all__ = ("TestSubnetInfo",)

from unittest import TestCase
from typing import List

from ..subnet_info import SubnetInfo


class TestSubnetInfo(TestCase):
    """
    In all test cases always check if functions returning correct data type.
    """

    def setUp(self) -> None:
        self.subnet_info = SubnetInfo()

    def test_if_get_local_ip_fnc_returning_correct_address(self):
        my_local_ip_addr: str = "192.168.0.173"

        self.assertIsInstance(
            self.subnet_info.get_local_ip(), str, msg="Return data type should be str."
        )
        self.assertEqual(
            my_local_ip_addr,
            self.subnet_info.get_local_ip(),
            msg="Should be equal. Change ip address to yours to verify.",
        )

    def test_if_get_subnet_mask_fnc_returning_correct_subnet_mask(self):
        my_local_subnet_mask: str = "255.255.255.0"

        self.assertIsInstance(
            self.subnet_info.get_subnet_mask(),
            str,
            msg="Return data type should be str.",
        )
        self.assertEqual(
            my_local_subnet_mask,
            self.subnet_info.get_subnet_mask(),
            msg="Should be equal. Change subnet mask to yours to verify.",
        )

    def test_if_calculate_cidr_fnc_returning_correct_cidr(self):
        self.assertIsInstance(
            self.subnet_info.calculate_cidr(subnet_mask="248.0.0.0"),
            int,
            msg="Return data type should be int.",
        )
        self.assertEqual(
            24,
            self.subnet_info.calculate_cidr(subnet_mask="255.255.255.0"),
            msg="Should return 24 CIDR from netmask 255.255.255.0",
        )
        self.assertEqual(
            1,
            self.subnet_info.calculate_cidr(subnet_mask="128.0.0.0"),
            msg="Should return 1 CIDR from netmask 128.0.0.0",
        )

    def test_if_calculate_host_amount_fnc_returning_correct_host_amount(self):
        self.assertIsInstance(
            self.subnet_info.calculate_hosts_amount(32),
            int,
            msg="Return data type should be int.",
        )
        self.assertEqual(
            1,
            self.subnet_info.calculate_hosts_amount(subnet_mask="255.255.255.255"),
            msg="Should return 1 hosts for subnet '255.255.255.255'.",
        )
        self.assertEqual(
            32766,
            self.subnet_info.calculate_hosts_amount(17),
            msg="Should return 32766 hosts for CIDR 17.",
        )

    def test_if_get_first_ip_address_fnc_returning_actually_first_ip_addr_in_given_network(
        self,
    ):
        self.assertIsInstance(
            self.subnet_info.get_first_ip_address("192.168.0.10", "255.255.255.0"),
            str,
            msg="Return data type should be str.",
        )
        self.assertEqual(
            "192.168.0.1",
            self.subnet_info.get_first_ip_address("192.168.0.173", "255.255.255.0"),
            msg="First IP for network 192.168.0.0/24 is 192.168.0.1 and fnc should return it.",
        )

    def test_if_get_last_ip_address_fnc_returning_actually_first_ip_addr_in_given_network(
        self,
    ):
        self.assertIsInstance(
            self.subnet_info.get_last_ip_address("192.168.0.10", "255.255.240.0"),
            str,
            msg="Return data type should be str.",
        )
        self.assertEqual(
            "192.168.0.254",
            self.subnet_info.get_last_ip_address("192.168.0.173", "255.255.255.0"),
            msg="Last IP for network 192.168.0.0/24 is 192.168.0.254 and fnc should return it.",
        )

    def test_if_generate_all_ip_addr_in_subnet_generating_correct_addresses(self):
        expected: List[str] = ["192.168.0.1", "192.168.0.2"]
        self.assertEqual(
            len(expected),
            self.subnet_info.calculate_hosts_amount(
                self.subnet_info.calculate_cidr("255.255.255.252")
            ),
            msg="here should only be two hosts on this subnet.",
        )
        self.assertEqual(
            expected,
            self.subnet_info.generate_all_ip_addr("192.168.0.1", "255.255.255.252"),
            msg="Function should return this two IP's ['192.168.0.1', '192.168.0.2']",
        )
