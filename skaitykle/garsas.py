# -*- coding: utf-8 -*-
"""GARSAS: ekvalaizeris + garsumas (2026-10-28).

Roberto užsakymas: „su garsu kaip su paveikslais — vieniems vieni patinka, kitiems kiti; lai
susiderina, kas jų ausiai geriau". Todėl ne trys paruošti tembrai, o slankikliai.

Juostos — oktavos 125 Hz … 8 kHz (ISO 266). Tai tos pačios septynios oktavos, kuriomis
skaičiuojamas kalbos suprantamumas (Articulation Index, French ir Steinberg 1947); 1–4 kHz
suprantamumui svarbiausios. Žemiau 125 Hz moterų balsas beveik nieko neturi, o virš ~11 kHz
mūsų garso NĖRA iš viso: Piper balsai 22 050 Hz, Nyquisto riba 11 025 Hz.

Biblioteka — `pedalboard` (Spotify, GPL-3.0 — tinka mūsų GPL v3), pasirinkta pamatavus prieš
`scipy` (2026-10-28, `PASAS.md`): 9 MB vietoj 115 MB, filtrai paruošti, 1900× greičiau už
realų laiką.

⛔ Du pamatuoti spąstai:
  * `process(..., reset=False)` — PRIVALOMA, kai garsas eina gabalais. Su `reset=True`
    (numatytasis!) filtro būsena nuliuojama kiekvieno gabalo pradžioje — skirtumas nuo
    apdorojimo vienu kartu 0,56 (spragtelėjimai sandūrose); su `False` — 3·10⁻⁸.
  * `pedalboard.Limiter` NĖRA apsauga nuo kirpimo: jis viduje turi kompresorių ir pakelia
    garsą net tada, kai niekas slenksčio neperžengia (−24,3 → −19,6 LUFS „plokščiu" EQ).
    Vietoj jo — `Compressor` (žemiau slenksčio skirtumas lygiai 0) ir minkštas kirpimas
    paskutiniams pikams, kuriuos kompresorius praleidžia per pirmą milisekundę.
"""
import numpy as np
import pedalboard as pb

# (dažnis Hz, pavadinimas, ką daro) — aprašai iš garso inžinierių vadovų balsui (podkastai,
# radijas); ribos tarp šaltinių šiek tiek skiriasi, todėl čia — kryptis, ne receptas.
JUOSTOS = (
    (125, 'Gylis', 'Balso kūnas ir sodrumas. Per daug — balsas dunda.'),
    (250, 'Šiluma', 'Šiltumas. Per daug — balsas tampa neaiškus, „purvinas".'),
    (500, 'Pilnumas', 'Balso pilnumas. Per daug — skamba kaip iš kartoninės dėžės.'),
    (1000, 'Vidurys', 'Balso branduolys. Per daug — nosinis, „telefoninis" skambesys.'),
    (2000, 'Aiškumas', 'Žodžių suprantamumas — čia gyvena priebalsiai.'),
    (4000, 'Ryškumas', 'Artumas, balsas „prie ausies". Per daug — rėžia ausį.'),
    (8000, 'S garsai', 'Gaivumas, s, š, z, ž. Per daug — švilpia; per mažai — duslu.'),
)
Q_OKTAVA = 1.41         # vienos oktavos pločio juosta
EQ_RIBA = 12            # ± dB kiekvienai juostai (įprasta grafiniams ekvalaizeriams)

# Numatytasis garsumas +6 dB: be jo failai −24 LUFS (balsai sulyginti namų kolonėlei), o
# podkastai ir vaizdo įrašai būna apie −16. +6 dB duoda −18 LUFS, pikas −1,5 dBFS — dar
# be kompresoriaus darbo (pamatuota 2026-10-28 ant Ingutės paskaitos).
GARSUMAS_NUMATYTAS = 6
PAUZE_NUMATYTA = 1.3    # s tarp pastraipų — tiek, kiek buvo iki šiol (0,45 + 0,15 + 0,7)
SLENKSTIS = 0.89        # −1 dBFS: virš jo minkštas kirpimas


def minkstas_kirpimas(a):
    """Žemiau SLENKSČIO — nepaliesta; virš — tanh kreive švelniai iki 1,0 (ne kampu)."""
    virs = np.abs(a) > SLENKSTIS
    if not virs.any():
        return a
    a = a.copy()
    v = np.abs(a[virs]) - SLENKSTIS
    a[virs] = np.sign(a[virs]) * (SLENKSTIS + (1 - SLENKSTIS) * np.tanh(v / (1 - SLENKSTIS)))
    return a


class Ekvalaizeris:
    """7 juostos + garsumas + apsauga nuo kirpimo. Vienas egzempliorius = vienas srautas
    (filtrų būsena tęsiasi per gabalus), todėl įrašymas ir perklausa turi po savo."""

    def __init__(self, stiprinimai=(0,) * len(JUOSTOS), garsumas_db=GARSUMAS_NUMATYTAS):
        self._filtrai = [pb.PeakFilter(cutoff_frequency_hz=float(f), gain_db=0.0, q=Q_OKTAVA)
                         for f, _, _ in JUOSTOS]
        self._garsumas = pb.Gain(gain_db=0.0)
        self._lenta = pb.Pedalboard(self._filtrai + [
            self._garsumas,
            pb.Compressor(threshold_db=-2.0, ratio=20.0, attack_ms=1.0, release_ms=80.0)])
        self.nustatyk(stiprinimai, garsumas_db)

    def nustatyk(self, stiprinimai, garsumas_db):
        """Keičia reikšmes NEnuliuodamas būsenos — galima judinti slankiklius grojant."""
        for f, g in zip(self._filtrai, stiprinimai):
            f.gain_db = float(g)
        self._garsumas.gain_db = float(garsumas_db)

    def apdorok(self, a, daznis):
        if not len(a):
            return a
        y = self._lenta.process(np.asarray(a, dtype='float32'), float(daznis), reset=False)
        return minkstas_kirpimas(y)
