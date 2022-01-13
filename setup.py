from typing import List
from setuptools import setup

with open('./requirements.txt') as req_pkg:
    required_pkg: List[str] = req_pkg.read().splitlines()

setup(
    install_requires=required_pkg,
)
