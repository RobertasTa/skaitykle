# -*- mode: python ; coding: utf-8 -*-
"""Skaityklė — PyInstaller receptas (2026-10-28). Iš `VERTEJAS lokalus\\SpeakDream.spec`,
be visko, ko Skaityklei nereikia (torch, transformers, ausys, vertimas).

Statyti IS SIO katalogo ir VISADA per `python -m PyInstaller`:

    .venv\\Scripts\\python.exe -m PyInstaller Skaitykle.spec --noconfirm

⛔ PRIES LIECIANT — `\\\\NAS-Rtrob\\OKF_Zinios\\OKF_PyInstaller\\paketo_patikros_guard.md`.

ROBERTO REIKALAVIMAS (10-28): abu balsai su TEISINGAIS nustatymais turi buti PAKETE, o programa
ieskoti TIK savo kataloge. Todel:
  * `balsai\\` — abu .onnx (Piper katalogo failai, SHA256 tikrinamas paleidziant), abu musu
    `espeak` .json ir Ingutes LICENSE-VOICE. ⛔ 2026-09-19 Vertejas isejo BE Ingutes, nes
    `datas` truko eilutes — is saltiniu viskas veike.
  * `lietuviskai\\` — fonemizatorius, receptas, plėtiklis, trys zodynai ir `zodziai_trumpi.txt`
    (be jo „ORAI" skaitomas raidemis; programa ji ikelia PATI is paketo, ne is D:\\).
  * Po statymo — `Skaitykle.exe --egzaminas <katalogas>`: abu balsai, sunkios vietos, savitikra.

SPRENDIMAI (paveldeti): ONEDIR (ne onefile), UPX isjungtas (antivirusai), console=False
(apsauga `main.py` `_uzkaisk_isvesti()` — guard Rule 8).
"""
from PyInstaller.utils.hooks import collect_all

KATALOGAS = "skaitykle"

piper_d, piper_b, piper_h = collect_all("piper")
ort_d, ort_b, ort_h = collect_all("onnxruntime")
pb_d, pb_b, pb_h = collect_all("pedalboard")
sd_d, sd_b, sd_h = collect_all("sounddevice")
sf_d, sf_b, sf_h = collect_all("soundfile")

a = Analysis(
    [f"{KATALOGAS}/main.py"],
    pathex=[KATALOGAS],
    binaries=piper_b + ort_b + pb_b + sd_b + sf_b,
    datas=[
        (f"{KATALOGAS}/Skaitykle.ico", "."),
        (f"{KATALOGAS}/README.txt", "."),
        # „?" → „Klauskite DI": promptas sako, kad brief'as guli šalia programos.
        ("AI_CONSULTANT_BRIEF.md", "."),
        (f"{KATALOGAS}/balsai", "balsai"),
        (f"{KATALOGAS}/lietuviskai", "lietuviskai"),
    ] + piper_d + ort_d + pb_d + sd_d + sf_d,
    hiddenimports=(["balsas", "garsas", "dantratis", "tarimas",
                    "lietuviskai.phonemize_lithuanian", "lietuviskai.skaiciu_pletiklis",
                    "lietuviskai.synth_reginute", "pedalboard_native"]
                   + piper_h + ort_h + pb_h + sd_h + sf_h),
    hookspath=[],
    runtime_hooks=[],
    # ⛔ `excludes` ismeta ir tai, ka importuoji virsuje (guard Rule 1) — musu importuose ju nera
    # (patikrinta 10-28). scipy/pyloudnorm venv'e tik matavimams, programai nereikia.
    excludes=["tkinter", "matplotlib", "pandas", "PIL", "IPython", "notebook", "pytest",
              "scipy", "pyloudnorm", "torch"],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Skaitykle",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=f"{KATALOGAS}/Skaitykle.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Skaitykle",
)
