#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
    name="torrent_manager",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            'torrent_manager=torrent_manager.main:main'
        ]
    },
    install_requires=[],
    author="fdugast",
    description="Watch torrent folder, add torrent to qbitorrent, download it",
    keywords="torrent qbitorrent",
    url="https://github.com/insoIite/torrent-manager"
)
