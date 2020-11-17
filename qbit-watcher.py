import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil

from multiprocessing import Process, freeze_support

from qbit_watcher.main import main

class WinService(win32serviceutil.ServiceFramework):
    _svc_name_ = "qbit-watcher"
    _svc_display_name_ = "Qbit watcher"
    _svc_description_ = """Scan src folder and add torrent files to qbittorrent
, wait for it to be complete, then download it in dest folder"""

    def __init__(self, args):
        super().__init__(*args)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.main()

    def main(self):
        main()

if __name__ == '__main__':
    freeze_support()
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WinService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(WinService)
