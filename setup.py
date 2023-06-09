"""Install premis """

from setuptools import setup, find_packages
from version import get_version


def main():
    """Install premis"""
    setup(
        name='premis',
        packages=find_packages(exclude=['tests', 'tests.*']),
        include_package_data=True,
        version=get_version(),
        install_requires=[
            'lxml',
            'six'
        ]
    )


if __name__ == '__main__':
    main()
