"""Install premis """

from setuptools import setup, find_packages
from version import get_version


def main():
    """Install premis"""
    setup(
        name='premis',
        packages=find_packages(exclude=['tests', 'tests.*']),
        version=get_version(),
        install_requires=['lxml', 'xml-helpers'],
        dependency_links=[
            'git+https://gitlab.csc.fi/dpres/xml-helpers.git'
            '@develop#egg=xml-helpers-0.0'
        ]
    )


if __name__ == '__main__':
    main()
