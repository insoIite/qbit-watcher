# qbit-watcher

## Introduction

This program is here to automate torrents downloads

It will:
* Listen a source folder for new torrent file
* Connect to qbitorrent and will add the torrent to it
* Ensure the torrent has finished to downloads
* Download the torrent using ftp
* Notify user with toasts

## Requirements

* Windows 10
* Python 3 (For developers only)

## Install dir

The application will be installed with non admin rights.

Files will be found in (replace %USER% by your username):

* C:\Users\%USER%\AppData\Local\Programs\qbit-watcher
* C:\Users\%USER%\AppData\Roaming\qbit-watcher

## Developers

### Build app in local without exe file

```bash
git clone https://github.com/insoIite/qbit-watcher.git
cd qbit-watcher
pip3 install -r requirements.txt
python setup.py sdist
pip3 install dist\qbit_watcher-X.tar.gz
edit config.yml
qbit_watcher.exe
```

### Build app in local with exe file
```bash
git clone https://github.com/insoIite/qbit-watcher.git
cd qbit-watcher
pip3 install -r requirements.txt
# -w generate an exe that will run in background
# The systray will attach the background process
pyinstaller.exe .\qbit-watcher.py --hiddenimport win32timezone --additional-hooks-dir .\packaging\pyinstaller_hooks\ -w
edit config.yml
dist\qbit-watcher\qbit_watcher.exe
```

### InnoSetup
More than InnoSetup installed, You will need `Inno Download Plugin` installed

The installer will:

* Download baretail (~220ko), that is an open source tail log file reader app
* Copy files in install directory
* Run notepad on config.yml in order to setup configuration
* Create shortcurt in Startup dir in order to run program at Startup
* Run program
