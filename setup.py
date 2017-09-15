"""
Install premis
"""

import os
from setuptools import setup, find_packages


def main():
    """Install premis"""
    setup(
        name='premis',
        packages=find_packages(exclude=['tests', 'tests.*']),
        version='0.1')


if __name__ == '__main__':
    main()
