# subnet-info

# Table of contents

* [General info](#general-info)
* [Documentation](#documentation)
* [Technologies](#technologies)
* [Setup](#setup)
* [Available methods](#available-methods)

## General info
With this app, you can get information about chosen subnet.

## Documentation
Click <a href="https://subnet-info.readthedocs.io/en/latest/">here</a> to see documentation!

## Technologies
<ul>
    <li>Python 3.6+</li>
</ul>

## Setup
First install subnet_info module from pypi
```commandline
pip install subnetinfo
```

Now you can create instance of main 'SubnetInfo' class to get important for you information.
```python
from subnet_info import SubnetInfo

_subnet = SubnetInfo()
print(_subnet.calculate_cidr(subnet_mask="255.255.255.0")) # returns 24
```

## Available methods
<ul>
    <li>get_local_ip (get your local ip address)</li>
    <li>get_public_ip (get your public ip address)</li>
    <li>get_subnet_mask (get your subnet netmask)</li>
    <li>calculate_cidr (calculate cidr based on provided subnet mask)</li>
    <li>calculate_hosts_amount (calculate how many hosts can be in subnet)</li>
    <li>get_first_ip_address (get first ip address in chosen subnet)</li>
    <li>get_last_ip_address (get last ip address in chosen subnet)</li>
    <li>generate_all_ip_addr (generate all ip addresses in chosen subnet)</li>
</ul>

