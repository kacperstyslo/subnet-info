"""
Helpers for SubnetInfo class.
"""

__all__ = ("SubnetInfoHelpers",)

import inspect
import subprocess
from typing import Dict, List

from .state import UserDevice


class SubnetInfoHelpers:
    """
    Store all SubnetInfo helpers.
    """

    def __init__(self) -> None:
        self.user_device = UserDevice()
        self._ip_config_command: Dict[str, str] = {
            "nt": "ipconfig",
            "posix": "ifconfig",
        }

    def get_ip_config(self) -> bytes:
        """
        Get user ip config from command line by using 'ipconfig' | 'ifconfig'
        command(it depends or what system user use).

        :return: Raw 'ipconfig' | 'ifconfig' command output.
        :rtype: bytes
        """
        return subprocess.Popen(
            self._ip_config_command.get(self.user_device.system_name),
            stdout=subprocess.PIPE,
        )

    @staticmethod
    def change_addr_num_system(addr: str, num_system: str) -> str:
        """
        Change IP/Mask address from decimal/binary number system to decimal/binary
        number system.

        :param addr: IP or netmask address
        :type addr: str
        :param num_system: Chosen number system, available options ('binary' | 'decimal')
        :type num_system: str
        :return: Converted IP/Mask address into selected number system.
        :rtype: str
        """
        value_in_new_num_sys: str = ""
        for octet in addr.split("."):
            if num_system == "binary":
                value_in_new_num_sys += "{:08b}.".format(int(octet))
            elif num_system == "decimal":
                value_in_new_num_sys += f"{str(int(octet, 2))}."
        return value_in_new_num_sys[:-1]

    @staticmethod
    def fill_addr_with_selected_num(ip_addr_bin: str, filler_value: str) -> str:
        """
        It is necessary to fill IP/Mask address with zeros or ones.
        If IP/Mask address will not have enough nums or dots then SubnetInfo will crash
        during some operations.

        :param ip_addr_bin: IP/Mask address in binary number system.
        :type ip_addr_bin: str
        :param filler_value: filler_value can be set to '1' or '0'. If filler_value
        will be set to '1' ip_addr_bin will be filled be '1' otherwise ip_addr_bin will
        be filed with zeros.
        :return: IP/Mask address in binary number system with enough amount of numbers
        and dots.
        :rtype str:
        """
        ip_addr_bin_sliced: List[str] = ip_addr_bin.split(".")

        for counter in range(4):
            try:
                if len(ip_addr_bin_sliced[counter]) != 8:
                    ip_addr_bin += (
                        f"{filler_value * (8 - len(ip_addr_bin_sliced[counter]))}."
                    )
            except IndexError:
                ip_addr_bin += f"{filler_value * 8}."

        if ip_addr_bin[-1] == ".":
            return (
                ip_addr_bin[:-2] + "1"
                if filler_value == "0"
                else ip_addr_bin[:-2] + "0"
            )

    def template_for_first_and_last_ip_address(
        self, ip_address: str, subnet_mask: str
    ) -> str:
        """
        This is template for two functions in SubnetInfo ('get_first_ip_address_in_subnet',
        'get_last_ip_address_in_subnet'). Always run the same way but provide different
        results based on what function user chose.

        :param ip_address: IP address for example '192.168.0.1'.
        :type ip_address: str
        :param subnet_mask: Subnet mask where provided address is.
        :type subnet_mask: str
        :return: Last or first IP address in chosen subnet
        :rtype: str
        """
        ip_addr_bin: str = self.change_addr_num_system(ip_address, num_system="binary")
        subnet_mask_bin: str = self.change_addr_num_system(
            subnet_mask, num_system="binary"
        )

        temp_ip_addr: str = ""
        for poz, bin_ in enumerate(subnet_mask_bin):
            if bin_ == "0":
                break
            temp_ip_addr += ip_addr_bin[poz]

        filer_value = (
            "0" if inspect.stack()[1].function == "get_first_ip_address" else "1"
        )
        result_before_convert = self.fill_addr_with_selected_num(
            temp_ip_addr, filler_value=filer_value
        )
        return self.change_addr_num_system(result_before_convert, num_system="decimal")

    @staticmethod
    def generate_subnet_block() -> Dict[int, int]:
        """
        Generates subnet block, this blocks are necessary to calculate CIDR. Number of
        valid hosts is always two less than the subnet block.

        :return: Subnet block (first value is subnet mask, second is block size).
        Below are values in this generated subnet block:
        ({128: 1, 192: 2, 224: 3, 240: 4, 248: 5, 252: 6, 254: 7, 255: 8})
        :rtype: Dict[int, int]
        """
        return {
            int(pow(2, 8) - pow(2, num)): counter
            for counter, num in enumerate(reversed(range(0, 8)), start=1)
        }
