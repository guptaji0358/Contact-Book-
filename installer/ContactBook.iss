; Inno Setup script for Contact Book.
; Compile with Inno Setup (https://jrsoftware.org/isinfo.php):
;   1. Build the app first:  pyinstaller installer\ContactBook.spec --distpath dist --workpath build
;   2. Open this file in Inno Setup Compiler (or run ISCC.exe installer\ContactBook.iss)
;
; Produces Output\ContactBook-Setup.exe

#define MyAppName "Contact Book"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Robin Gupta"
#define MyAppExeName "ContactBook.exe"
#define SourceDist "..\dist\ContactBook"

[Setup]
; The app stores its database files (CONTACT_BOOKS.db, books\*.db) next to
; its own exe at runtime. Installing under Program Files would make that
; fail for non-admin users (no write access there), so this installs
; per-user under %LOCALAPPDATA% instead and never asks for elevation.
AppId={{4C8E2C2B-7B7C-4E1E-9C7C-9B1B7C0B5B1A}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=ContactBook-Setup
SetupIconFile=..\CONTACT_BOOK_ICON.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#SourceDist}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Leave the user's contact books and settings alone on uninstall - only the
; program files themselves are removed by the default uninstaller behavior.
