#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
    name="qbit_watcher",
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            'qbit_watcher=qbit_watcher.main:main'
        ]
    },
    install_requires=[
        "pyyaml==5.1.2",
        "qbittorrent-api==2020.10.11",
        "watchdog==0.10.3",
        "win10toast==0.9",
        "infi.systray==0.1.12"
    ],
    author="fdugast",
    description="Watch torrent folder, add torrent to qbitorrent, download it",
    keywords="torrent qbitorrent",
    url="https://github.com/insoIite/qbit-watcher"
)
