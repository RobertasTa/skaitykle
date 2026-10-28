# Third-party components

Skaityklė is licensed under **GPL v3** (see [LICENSE](LICENSE)). The installer bundles the
components below. Licences were read from each installed package's metadata (2026-10-28),
not from memory.

| Component | Version | Licence | What it does here |
|---|---|---|---|
| [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) | 6.11.0 | GPL-3.0-only | the window — the reason the whole program is GPL v3 |
| Qt 6 (PyQt6-Qt6) | 6.11.2 | LGPL v3 | Qt libraries under PyQt6 |
| PyQt6-sip | 13.13.0 | BSD-2-Clause | PyQt6 runtime |
| [piper-tts](https://github.com/OHF-Voice/piper1-gpl) | 1.8.0 | GPL-3.0-or-later | speech synthesis engine; includes espeak-ng (GPL-3.0) and its data |
| [ONNX Runtime](https://github.com/microsoft/onnxruntime) | 1.30.0 | MIT | runs the voice models |
| [pedalboard](https://github.com/spotify/pedalboard) | 0.9.26 | GPL-3.0 | equaliser, compressor, MP3 decoding for playback; includes JUCE (GPL-3.0) and LAME |
| [soundfile](https://github.com/bastibe/python-soundfile) | 0.14.0 | BSD-3-Clause | writing MP3; bundles libsndfile 1.2.2 (LGPL-2.1) with LAME and mpg123 (LGPL) |
| [sounddevice](https://github.com/spatialaudio/python-sounddevice) | 0.5.6 | MIT | playing audio; bundles PortAudio (MIT) |
| [NumPy](https://numpy.org) | 2.5.3 | BSD-3-Clause and others | audio arrays |
| cffi | 2.1.1 | MIT-0 | used by soundfile and sounddevice |

## Voices

| Voice | Licence | Origin |
|---|---|---|
| Reginutė (`lt_LT-reginute1-medium`) | CC BY 4.0 | learned from the LIEPA corpus |
| Ingutė (`lt_LT-ingute-medium`) | NewGenLTU OpenRAIL-D — full text in [`skaitykle/balsai/LICENSE-VOICE-ingute`](skaitykle/balsai/LICENSE-VOICE-ingute) | grown from the Reginutė model with the authors' Python tools |

Both voice files are identical to the ones in the Piper voice catalogue
(`rhasspy/piper-voices`): SHA256 `0417c4ef…986ee` (Reginutė), `31bdf1df…41d8` (Ingutė).
If you redistribute Ingutė, keep `LICENSE-VOICE` with it and state the origin.

## Lithuanian text processing

`skaitykle/lietuviskai/` — the Lithuanian phonemizer, stress dictionary, letter names and
number expander — is the authors' own work (the same module that was merged into Piper),
GPL v3 with this program.

## Source code

The complete source code, the build recipe (`Skaitykle.spec`) and the installer script
(`_instaliatorius/Skaitykle.iss`) are in this repository: https://github.com/RobertasTa/skaitykle
