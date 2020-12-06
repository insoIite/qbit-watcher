; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!
#pragma include __INCLUDE__ + ";" + "C:\Program Files (x86)\Inno Download Plugin"

[Setup]
AppName=qbit-watcher
AppVersion=1.2.1
WizardStyle=modern
DefaultDirName={autopf}\qbit-watcher
Uninstallable=yes
UninstallDisplayName={app}\qbit-watcher
UninstallDisplayIcon={app}\qbit-watcher.exe
Compression=lzma2
SolidCompression=yes
OutputDir=..\..\
OutputBaseFilename=qbit-watcher-setup
ChangesEnvironment=yes
PrivilegesRequired=lowest

#include <idp.iss>

[Files]
Source: "..\..\dist\qbit-watcher\*"; DestDir: "{app}\qbit-watcher"; Flags: ignoreversion recursesubdirs
Source: "..\..\config.yml"; DestDir: "{app}\qbit-watcher";
Source: "..\..\icon\*"; DestDir: "{app}\qbit-watcher\icon";
Source: "..\..\README.md"; DestDir: "{app}\qbit-watcher";
Source: "{tmp}\baretail.exe"; DestDir: "{app}\qbit-watcher" ; Flags: external; ExternalSize: 225280


[Code]
procedure InitializeWizard();
begin
    idpAddFileSize('https://www.baremetalsoft.com/baretail/download.php?p=m', ExpandConstant('{tmp}\baretail.exe'), 225280);
    idpDownloadAfter(wpReady);
end;

[Icons]
Name: "{userstartup}\qbit-watcher.exe"; Filename: "{app}\qbit-watcher\qbit-watcher.exe"; WorkingDir: "{app}\qbit-watcher"

[Run]
Filename: "notepad"; Parameters: {app}\qbit-watcher\config.yml; Description: "Edit configuration file";
Filename: {app}\qbit-watcher\qbit-watcher.exe ; Flags: runhidden nowait
