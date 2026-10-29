# Building Skaityklė

Windows 10/11 x64, Python 3.12.

```
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Voices

Since 0.2 the voice models are **not** part of the build: the program downloads them per language
(⚙ → Languages and voices) into `%LOCALAPPDATA%\Skaitykle\balsai\` and checks each file's SHA256
against `skaitykle/balsu_siuntimas.py`. The `.onnx.json` files for every voice are in this
repository and go into the package. To run from source without downloading, you may also put the
`.onnx` files into `skaitykle\balsai\` (git ignores them); the URLs and SHA256 sums are in
`balsu_siuntimas.FAILAI`. `SKAITYKLE_BALSAI=<folder>` points the program to another voice folder
(used by the tests, so they never touch your real voices).

⚠️ Use the Lithuanian `.onnx.json` files from this repository, not the catalogue ones: they say
`phoneme_type: espeak`, because piper-tts 1.8.0 does not know `lithuanian` yet; the program
feeds the phonemes itself (`skaitykle/lietuviskai/`).

## Run from source

```
.venv\Scripts\python.exe skaitykle\main.py
```

## Package and installer

```
.venv\Scripts\python.exe -m PyInstaller Skaitykle.spec --noconfirm
dist\Skaitykle\Skaitykle.exe --egzaminas egzaminas
```

The second line is the package exam: every downloaded voice reads a test text in its language with
the hard cases (`15:25`, `ORAI`, `ES`, `---`) through the packaged program, and
`egzaminas\egzaminas.txt` must end with `REZULTATAS: GERAI`. Voices that are not downloaded are
listed as `neparsiusta`; before a release run the exam with all of them (`SKAITYKLE_BALSAI`).

Installer (Inno Setup 6, from PowerShell; the output must go to a folder on C:):

```
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" "/O$env:TEMP\skaitykle_setup" _instaliatorius\Skaitykle.iss
```
