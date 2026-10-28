# Building Skaityklė

Windows 10/11 x64, Python 3.12.

```
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Voices

The two `.onnx` voice files are not in git (63.5 MB each). Download them from the Piper voice
catalogue into `skaitykle\balsai\` — the matching `.onnx.json` files are already there:

| File | URL | SHA256 |
|---|---|---|
| `lt_LT-reginute1-medium.onnx` | https://huggingface.co/rhasspy/piper-voices/resolve/main/lt/lt_LT/reginute1/medium/lt_LT-reginute1-medium.onnx | `0417c4ef351686ec0b0e7bf63426aefc72faea4a7693cfcb2f01ea8f6ee986ee` |
| `lt_LT-ingute-medium.onnx` | https://huggingface.co/rhasspy/piper-voices/resolve/main/lt/lt_LT/ingute/medium/lt_LT-ingute-medium.onnx | `31bdf1df5339e7da0e0f8c8e847e0f9e720bb732c0ffc7fb3d81970844b441d8` |

⚠️ Use the `.onnx.json` files from this repository, not the catalogue ones: they say
`phoneme_type: espeak`, because piper-tts 1.8.0 does not know `lithuanian` yet; the program
feeds the phonemes itself (`skaitykle/lietuviskai/`). The program checks both SHA256 sums and
these settings every time it starts.

## Run from source

```
.venv\Scripts\python.exe skaitykle\main.py
```

## Package and installer

```
.venv\Scripts\python.exe -m PyInstaller Skaitykle.spec --noconfirm
dist\Skaitykle\Skaitykle.exe --egzaminas egzaminas
```

The second line is the package exam: both voices read a test text with the hard cases
(`15:25`, `ORAI`, `ES`, `---`) through the packaged program, and `egzaminas\egzaminas.txt`
must end with `REZULTATAS: GERAI`.

Installer (Inno Setup 6, from PowerShell; the output must go to a folder on C:):

```
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" "/O$env:TEMP\skaitykle_setup" _instaliatorius\Skaitykle.iss
```
