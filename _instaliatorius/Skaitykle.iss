; Skaitykle - Inno Setup instaliatorius (2026-10-28). Is SpeakDream.iss (dviracio neieskom).
;
; STATYTI PER POWERSHELL, ne per Git Bash (MSYS argumenta "/O..." pavercia keliu):
;   & "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" "/O$env:TEMP\skaitykle_setup" Skaitykle.iss
;   Move-Item "$env:TEMP\skaitykle_setup\Skaitykle-<versija>-setup.exe" ..\dist\
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
;  - 0.2 (2026-10-29): KETURIOS KALBOS, BALSU PAKETE NERA (Roberto: "kazkam reikes tik
;    lietuviu, kazkam tik rusu"). Kaip Diktuokle: varneles tik IRASO pasirinkima i
;    vienkartini %APPDATA%\Skaitykle\diegimo_kalbos.json, o balsus (po 64 MB, SHA256)
;    parsisiuncia programa, paklaususi. Inno dideliems siuntimams netinka (Diktuokles pamoka).
;    TYLUS diegimas (winget) failo NERASO - kitaip kiekvienas atnaujinimas perrasytu zmogaus
;    pasirinkta kalba Windows kalba.
;  - Atnaujinant is 0.1.x senieji lietuviu balsai lieka {app}\_internal\balsai\ - programa juos
;    randa (SHA tikrina), parsisiusti is naujo nereikia.

#define AppName      "Skaityklė"
#define AppDirName   "Skaitykle"
#define AppVersion   "0.2.0"
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
; Instaliatoriaus kalbos = programos kalbos (seimos pamoka, FOTO namai 08-30). Lietuviu pirma —
; tai lietuviska dovana; Lithuanian.isl - musu (Inno Setup jos neturi).
Name: "lt"; MessagesFile: "Lithuanian.isl"
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "de"; MessagesFile: "compiler:Languages\German.isl"

[CustomMessages]
lt.KalbuPuslapis=Kalbos
lt.KalbuAprasas=Kokiomis kalbomis norėsite įgarsinti tekstus?
lt.KalbuPaaiskinimas=Pažymėkite tik tai, ko jums reikia. Kiekvienos kalbos balsai parsisiunčiami vieną kartą, pirmą kartą paleidus programą (iš Piper balsų katalogo):%n%n    Lietuvių 128 MB    Rusų 64 MB    Anglų 64 MB    Vokiečių 64 MB%n%nKitas kalbas galėsite pridėti bet kada: ⚙ → Kalbos ir balsai. Pirmoji pažymėta kalba nustato ir programos lango kalbą.
lt.KalbaLT=Lietuvių (Ingutė, Reginutė)
lt.KalbaRU=Rusų (Dmitri)
lt.KalbaEN=Anglų (Cori)
lt.KalbaDE=Vokiečių (Thorsten)
lt.NiekoNepazymeta=Pažymėkite bent vieną kalbą.
ru.KalbuPuslapis=Языки
ru.KalbuAprasas=На каких языках вы хотите озвучивать тексты?
ru.KalbuPaaiskinimas=Отметьте только то, что нужно. Голоса каждого языка загружаются один раз при первом запуске программы (из каталога голосов Piper):%n%n    Литовский 128 MB    Русский 64 MB    Английский 64 MB    Немецкий 64 MB%n%nДругие языки можно добавить в любое время: ⚙ → Языки и голоса. Первый отмеченный язык задаёт и язык окна программы.
ru.KalbaLT=Литовский (Ingutė, Reginutė)
ru.KalbaRU=Русский (Dmitri)
ru.KalbaEN=Английский (Cori)
ru.KalbaDE=Немецкий (Thorsten)
ru.NiekoNepazymeta=Отметьте хотя бы один язык.
en.KalbuPuslapis=Languages
en.KalbuAprasas=Which languages do you want to read texts aloud in?
en.KalbuPaaiskinimas=Tick only what you need. The voices of each language are downloaded once, on the first start of the program (from the Piper voice catalogue):%n%n    Lithuanian 128 MB    Russian 64 MB    English 64 MB    German 64 MB%n%nYou can add other languages at any time: ⚙ → Languages and voices. The first ticked language also sets the language of the program window.
en.KalbaLT=Lithuanian (Ingutė, Reginutė)
en.KalbaRU=Russian (Dmitri)
en.KalbaEN=English (Cori)
en.KalbaDE=German (Thorsten)
en.NiekoNepazymeta=Please tick at least one language.
de.KalbuPuslapis=Sprachen
de.KalbuAprasas=In welchen Sprachen möchten Sie Texte vorlesen lassen?
de.KalbuPaaiskinimas=Haken Sie nur an, was Sie brauchen. Die Stimmen jeder Sprache werden einmal beim ersten Programmstart heruntergeladen (aus dem Piper-Stimmenkatalog):%n%n    Litauisch 128 MB    Russisch 64 MB    Englisch 64 MB    Deutsch 64 MB%n%nWeitere Sprachen können Sie jederzeit hinzufügen: ⚙ → Sprachen und Stimmen. Die erste angehakte Sprache bestimmt auch die Sprache des Programmfensters.
de.KalbaLT=Litauisch (Ingutė, Reginutė)
de.KalbaRU=Russisch (Dmitri)
de.KalbaEN=Englisch (Cori)
de.KalbaDE=Deutsch (Thorsten)
de.NiekoNepazymeta=Bitte haken Sie mindestens eine Sprache an.

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

[UninstallDelete]
; Parsiusti balsai (iki ~320 MB) - salinant istrinami: juos visada galima parsisiusti is naujo.
Type: filesandordirs; Name: "{localappdata}\{#AppDirName}\balsai"

; PASTABA salinant programa: %APPDATA%\Skaitykle (nustatymai.json, tarimas.json) NETRINAMA -
; tai zmogaus nustatymai ir jo tarimo zodynelis; perdiegus jie lieka.

[Code]
var
  KalbuPuslapis: TInputOptionWizardPage;

procedure InitializeWizard;
begin
  // Atskiras puslapis, ne [Components]: kalbos nekeicia paketo failu - tik nustatyma.
  KalbuPuslapis := CreateInputOptionPage(wpSelectTasks,
    ExpandConstant('{cm:KalbuPuslapis}'),
    ExpandConstant('{cm:KalbuAprasas}'),
    ExpandConstant('{cm:KalbuPaaiskinimas}'),
    False, False);   // varneles, be "pazymeti viska"
  KalbuPuslapis.Add(ExpandConstant('{cm:KalbaLT}'));
  KalbuPuslapis.Add(ExpandConstant('{cm:KalbaRU}'));
  KalbuPuslapis.Add(ExpandConstant('{cm:KalbaEN}'));
  KalbuPuslapis.Add(ExpandConstant('{cm:KalbaDE}'));
  // Numatytoji varnele - pagal DIEGIMO kalba: kas diegia rusiskai, greiciausiai skaitys
  // rusiskai. Lietuviu - kitais atvejais, nes tai lietuviska dovana.
  if ActiveLanguage = 'ru' then
    KalbuPuslapis.Values[1] := True
  else if ActiveLanguage = 'en' then
    KalbuPuslapis.Values[2] := True
  else if ActiveLanguage = 'de' then
    KalbuPuslapis.Values[3] := True
  else
    KalbuPuslapis.Values[0] := True;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  i, Kiek: Integer;
begin
  Result := True;
  if CurPageID = KalbuPuslapis.ID then
  begin
    Kiek := 0;
    for i := 0 to 3 do
      if KalbuPuslapis.Values[i] then
        Kiek := Kiek + 1;
    // Be nė vienos kalbos programa neturetu nė vieno balso - neleidziam eiti toliau.
    if Kiek = 0 then
    begin
      MsgBox(ExpandConstant('{cm:NiekoNepazymeta}'), mbError, MB_OK);
      Result := False;
    end;
  end;
end;

procedure RasykKalbas;
var
  Katalogas, Kalbos: String;
  i: Integer;
  Kodai: array[0..3] of String;
begin
  Kodai[0] := 'lt'; Kodai[1] := 'ru'; Kodai[2] := 'en'; Kodai[3] := 'de';
  Kalbos := '';
  for i := 0 to 3 do
    if KalbuPuslapis.Values[i] then
    begin
      if Kalbos <> '' then Kalbos := Kalbos + ', ';
      Kalbos := Kalbos + '"' + Kodai[i] + '"';
    end;
  // Tas pats katalogas, kuri skaito programa (main.APLANKAS = %APPDATA%\Skaitykle).
  Katalogas := ExpandConstant('{userappdata}\{#AppDirName}');
  if not DirExists(Katalogas) then
    ForceDirectories(Katalogas);
  SaveStringToFile(Katalogas + '\diegimo_kalbos.json',
    '{"kalbos": [' + Kalbos + ']}' + #13#10, False);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  // Tylus diegimas (winget) varneliu nemato - nerasom, programa ims Windows kalba.
  if (CurStep = ssPostInstall) and not WizardSilent then
    RasykKalbas;
end;
