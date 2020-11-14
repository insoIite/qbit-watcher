# qbit-watcher

## Introduction

This program is here to automate torrents downloads
It will:

* Listen a source folder for new torrent file
* Connect to qbitorrent and will add the torrent to it
* Ensure the torrent as finished to downloads
* Download the torrent using ftp
* Notify user with toasts

## Requirements

* Windows 10
* Python 3

## Configuration

Create a yml file

```yml
---
folders:
  # Folder in which torrent files are download
  # Example downloding my_movie.torrent in src_folder
  src: ''  # Example: C:\Users\foo\Downloads
  # Folder in which the actual files will be downloaded
  # Example downloading my_move from ftp
  dest: '' # Example: 'E:\Series

qbitorrent:
  scheme: https
  domain: ""   # Example 'qbittorrent.mydomain'
  user: ""     # qbittorrent user
  password: "" # qbittorrent password
  port: 8080   # qbitorrent port

ftp:
  domain: ""      # FTP hostname
  port: 21        # FTP port
  user: ""        # FTP user
  password: ""    # FTP password
  # Remote path on the FTP server
  remote_path: "" # Example: "/torrents/qbittorrent/"
```

## Developer

```
git clone https://github.com/insoIite/qbit-watcher.git
cd qbit-watcher
pip3 install -r requirements.txt
python setup.py sdist
pip3 install dist\qbit_watcher-0.1.tar.gz
qbit_watcher.exe --config "path_to_config_file\config.yml"
```
