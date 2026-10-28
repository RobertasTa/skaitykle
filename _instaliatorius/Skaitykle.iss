; Skaitykle - Inno Setup instaliatorius (2026-10-28). Is SpeakDream.iss (dviracio neieskom).
;
; STATYTI PER POWERSHELL, ne per Git Bash (MSYS argumenta "/O..." pavercia keliu):
;   & "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" "/O$env:TEMP\skaitykle_setup" Skaitykle.iss
;   Move-Item "$env:TEMP\skaitykle_setup\Skaitykle-0.1.0-setup.exe" ..\dist\
; ⛔ Inno Setup i D: diska rasyti NEGALI ("output file appears to be in use (32)") -
;   seimos pamoka 2026-09-19.
; ⛔ Failas UTF-8 SU BOM (AppName turi lietuviska raide) - guard Rule 6.
;
; SPRENDIMAI:
;  - ROBERTO REIKALAVIMAS 10-28: abu balsai su teisingais nustatymais - PAKETE. Visas onedir
;    aplankas (exe + _internal su balsai\ ir lietuviskai\) eina vienu [Files] irasu; programa
;    paleidziama pasitikrina pati (SHA256, nustatymai, zodziu sarasas) ir ieško TIK savo kataloge.
;  - PrivilegesRequired=lowest -> {localappdata}\Programs\Skaitykle, JOKIO UAC lango.
;  - Diegimo kalba - TIK lietuviu: programos sasaja lietuviska, balsai lietuviski (guard Rule 6).
;  - AppId GUID FIKSUOTAS - NIEKADA nekeisti (kitaip senos versijos liks salia).
;  - CloseApplications=force: perleidziant setup'a ant veikiancios programos garso gija
;    mandagiai neuzsidaro (Diktuokles pamoka 09-11).

#define AppName      "Skaityklė"
#define AppDirName   "Skaitykle"
#define AppVersion   "0.1.0"
#define AppExeName   "Skaitykle.exe"
#define AppUrl       "https://github.com/RobertasTa/skaitykle"

[Setup]
AppId={{A1314294-EF6F-4447-B13B-99F1CF8C58D9}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher=Robertas & Claude (AI)
AppPublisherURL={#AppUrl}
AppSupportURL={#AppUrl}/issues
AppUpdatesURL={#AppUrl}/releases
DefaultDirName={autopf}\{#AppDirName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
; OutputDir perrasomas komandines eilutes /O (i D: rasyti negalima, zr. virsuje).
OutputDir=..\dist
OutputBaseFilename={#AppDirName}-{#AppVersion}-setup
SetupIconFile=..\skaitykle\Skaitykle.ico
UninstallDisplayIcon={app}\{#AppExeName}
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=2
WizardStyle=modern
CloseApplications=force

[Languages]
Name: "lt"; MessagesFile: "Lithuanian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Visas onedir aplankas: Skaitykle.exe + _internal\ (balsai, zodynai, licencija) rekursyviai.
Source: "..\dist\Skaitykle\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent

; PASTABA salinant programa: %APPDATA%\Skaitykle (nustatymai.json, tarimas.json) NETRINAMA -
; tai zmogaus nustatymai ir jo tarimo zodynelis; perdiegus jie lieka.
