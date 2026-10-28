# -*- coding: utf-8 -*-
"""SKAITYKLĖ — tekstas → mp3 Ingutės arba Reginutės balsu (2026-10-28).

Roberto užsakymas: pažįstami patys su Ingute nesusitvarko — „su kalbėjimo greičiu kažkas
nesigauna". Langas: kalba ir balsas (išskleidžiami, kaip SpeakDream), greičio slankiklis (kaip
Vertėjo), TEKSTO LAUKAS, kur dėti mp3, „Daryti" ir „Perklausyti". Dantratyje (⚙) — ekvalaizeris,
garsumas ir pauzė tarp pastraipų, su perklausa grojant. Viskas šiame kompiuteryje.

⭐ Kaip programa žino, ką įgarsinti (Roberto: „sugalvok, kad programa žinotų, ką įgarsinti"):
įgarsinama VISADA tai, kas yra teksto lauke. „Atidaryti .txt…" failą įkelia į tą patį lauką —
prieš įgarsinant jį galima pataisyti; įklijuotas ar įrašytas tekstas veikia lygiai taip pat.
Jokių režimų: ką matai, tą ir girdi. Eilutė „---" dalija į kelis mp3 (po vieną skaidrei).

Išvaizda — Diktuoklės šeimos („tai jau tampa kaip tavo vizitinė kortelė"). Vardas ir ikona — Roberto.

⛔ PyQt6 spąstai, į kuriuos jau esam įkritę: identifikatoriai TIK ASCII; nuorodos į gijas ANT
self ir niekur nenulinamos (`OKF_PyQt6_GUI\\pyqt6_threading_guard.md`); išjungiami valdikliai
po vieną, ne jų tėvas.
"""
import json
import os
import re
import sys
import threading
import unicodedata
import urllib.parse
import webbrowser

CIA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CIA)


def _uzkaisk_isvesti():
    """Be konsolės `sys.stdout` ir `sys.stderr` yra `None`, ir pirmas bibliotekos `logging`
    įrašas nuverčia programą (SpeakDream 09-18). Įdiegta programa veiks būtent taip."""
    for vardas in ('stdout', 'stderr'):
        srautas = getattr(sys, vardas, None)
        if srautas is None:
            setattr(sys, vardas, open(os.devnull, 'w', encoding='utf-8'))
        else:
            try:
                srautas.reconfigure(encoding='utf-8', errors='replace')
            except Exception:
                pass


_uzkaisk_isvesti()

import numpy as np
import sounddevice as sd
import soundfile as sf
from pedalboard.io import AudioFile
from PyQt6.QtCore import QObject, QThread, QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog, QGridLayout,
                             QHBoxLayout, QLabel, QLineEdit, QMenu, QMessageBox, QPlainTextEdit,
                             QProgressBar, QPushButton, QRadioButton, QSlider, QVBoxLayout,
                             QWidget)

import balsas
import garsas
from dantratis import GarsoNustatymai
from tarimas import TarimoZodynas

PAVADINIMAS = 'Skaityklė'
VERSIJA = '0.1'
# Ikona — PROGRAMOS kataloge (pakete `_internal\`), ne `build\`: iš ten ji į exe nepatektų.
# Roberto GPT paveikslas, kampai iškirpti `_ikona\kirpk_kvadrata.py` (spindulys pagal įstrižainę).
IKONA = os.path.join(CIA, 'Skaitykle.ico')
README = os.path.join(CIA, 'README.txt')
# „?" → „Klauskite DI" (šeimos standartas iš Diktuoklės). Nuoroda įrašyta IŠ ANKSTO, kaip
# SpeakDream'e: kol repo neviešas, ji neatsidaro, todėl promptas pats pasako, kad tas pats
# failas guli šalia programos — meluoti apie neveikiančią nuorodą būtų blogiau.
KUREJO_PUSLAPIS = 'https://github.com/RobertasTa/skaitykle'
BRIEF_URL = 'https://raw.githubusercontent.com/RobertasTa/skaitykle/main/AI_CONSULTANT_BRIEF.md'
# ES DI akto 50 str.: sintetinis garsas žymimas mašinai skaitomai. Balsų vardų NErašom
# (Roberto sprendimas 10-02). ⛔ ID3 žymose lietuviškos raidės susigadina (libsndfile/LAME
# rašo baitus kaip Latin-1; pamatuota 10-28) — todėl žymos tik ASCII.
ZYME_DI = 'Sintetinis balsas (DI) - Skaitykle'
APLANKAS = os.path.join(os.environ.get('APPDATA') or os.path.expanduser('~'), 'Skaitykle')
NUSTATYMAI = os.path.join(APLANKAS, 'nustatymai.json')
TARIMAS = os.path.join(APLANKAS, 'tarimas.json')
PAVYZDYS = ('Laba diena. Šiandien kalbėsime apie fotosintezę, procesą, kurio metu augalai, '
            'naudodami saulės šviesą, gamina deguonį. Pasiklausykite, kaip skamba balsas, ir '
            'pasirinkite, kas jūsų ausiai maloniausia.')
PABAIGOS_TYLA = 0.7     # s po paskutinės pastraipos (recepto pabaiga)
PAZYMETO_RIBA = 3000    # simbolių: tiek daugiausia groja „▸" iš pažymėto teksto
PERZIUROS_RIBA = 3000   # simbolių failo pradžios, rodomos „Iš failo" režimu
# Trukmės įvertis močiutei su 100 psl. knyga („kiek užtruks?"): pamatuota 10-28 — 174 simb. →
# 9,6 s kalbos (Ingutė), 442 simb. → 31,4 s (Reginutė) ⇒ ~16 simb./s esant 1,00×; sintezė
# ~20× greitesnė už realų laiką procesoriumi. Tai „≈", ne pažadas.
SIMB_PER_SEK = 16.0
DARBO_GREITIS = 20.0

# Būsenos taško spalvos — tos pačios kaip Diktuoklės.
ZALIA, GELTONA, RAUDONA, PILKA = '#4ADE80', '#ffaa00', '#ff6a6a', '#888888'

# Diktuoklės STILIUS + SpeakDream išskleidžiamas sąrašas ir slankiklis; nauja tik įvedimo
# laukai, progreso juosta, lentelė ir statūs ekvalaizerio slankikliai — iš tų pačių spalvų.
STILIUS = """
QWidget#saknis, QDialog { background: #1b1b1b; }
QLabel { color: #d8d8d8; font-family: 'Segoe UI'; font-size: 13px; }
QLabel#busena { color: #e6e6e6; font-size: 13px; }
QLabel#uzuomina { color: #7d7d7d; font-size: 11px; }
QLabel#antraste { color: #ffffff; font-size: 15px; font-weight: bold; }
QPushButton {
    background: #343434; color: #c8c8c8; border: none; border-radius: 5px;
    padding: 7px 15px; font-family: 'Segoe UI'; font-size: 13px;
}
QPushButton:hover { background: #444444; }
QPushButton:disabled { background: #262626; color: #5a5a5a; }
QPushButton[aktyvus="taip"] { background: #1668C1; color: #ffffff; }
QPushButton[aktyvus="taip"]:disabled { background: #233a55; color: #8a9bb0; }
QPushButton#ikona { padding: 6px 9px; font-size: 14px; }
QPushButton#ikona::menu-indicator { image: none; width: 0px; }
QMessageBox { background: #1b1b1b; }
QToolTip { background: #2b2b2b; color: #dddddd; border: 1px solid #3d3d3d; padding: 4px; }
QComboBox {
    background: #2b2b2b; color: #d8d8d8; border: 1px solid #3d3d3d;
    border-radius: 5px; padding: 5px 8px; font-family: 'Segoe UI'; font-size: 13px;
}
QComboBox:hover { border: 1px solid #4f4f4f; }
QComboBox:disabled { background: #242424; color: #5a5a5a; border: 1px solid #2f2f2f; }
QComboBox::drop-down { border: none; width: 18px; }
QComboBox QAbstractItemView {
    background: #2b2b2b; color: #dddddd; border: 1px solid #3d3d3d;
    selection-background-color: #1668C1; selection-color: #ffffff; outline: none;
}
QLineEdit, QPlainTextEdit {
    background: #242424; color: #d8d8d8; border: 1px solid #3d3d3d;
    border-radius: 5px; padding: 6px 8px; font-family: 'Segoe UI'; font-size: 13px;
    selection-background-color: #1668C1; selection-color: #ffffff;
}
QLineEdit:hover, QPlainTextEdit:hover { border: 1px solid #4f4f4f; }
QLineEdit:disabled, QPlainTextEdit:disabled { color: #6a6a6a; border: 1px solid #2f2f2f; }
QTableWidget {
    background: #242424; color: #d8d8d8; border: 1px solid #3d3d3d; gridline-color: #333333;
    selection-background-color: #1668C1; selection-color: #ffffff;
}
QHeaderView::section { background: #2b2b2b; color: #b8b8b8; border: none; padding: 5px; }
QSlider::groove:horizontal { height: 4px; background: #3a3a3a; border-radius: 2px; }
QSlider::handle:horizontal { background: #c8c8c8; width: 12px; height: 12px;
                             margin: -5px 0; border-radius: 6px; }
QSlider::handle:horizontal:hover { background: #ffffff; }
QSlider::sub-page:horizontal { background: #1668C1; border-radius: 2px; }
QSlider::groove:horizontal:disabled { background: #2a2a2a; }
QSlider::handle:horizontal:disabled { background: #5a5a5a; }
QSlider::sub-page:horizontal:disabled { background: #3a3a3a; }
QSlider::groove:vertical { width: 4px; background: #3a3a3a; border-radius: 2px; }
QSlider::handle:vertical { background: #c8c8c8; width: 14px; height: 14px;
                           margin: 0 -5px; border-radius: 7px; }
QSlider::handle:vertical:hover { background: #ffffff; }
QProgressBar { background: #2b2b2b; border: none; border-radius: 3px; max-height: 6px; }
QProgressBar::chunk { background: #1668C1; border-radius: 3px; }
QMenu { background: #2b2b2b; color: #dddddd; border: 1px solid #3d3d3d; }
QMenu::item { padding: 6px 26px 6px 22px; }
QMenu::item:selected { background: #1668C1; color: #ffffff; }
/* Skrituliukai „Iš failo / Iš lango" (Roberto pasiūlymas 10-28) — ta pati mėlyna, jokios naujos
   spalvos; pažymėtas — pilnas mėlynas skritulys su šviesiu centru. */
QRadioButton { color: #d8d8d8; font-family: 'Segoe UI'; font-size: 13px; spacing: 7px;
               padding-right: 6px; }
/* ⚠️ Qt rėmelį PRIDEDA prie width/height: visas skritulys = turinys + 2×rėmelis = 16 px abiem
   būsenoms, kitaip pažymėtas išeina kvadratėlis ir nustumia užrašą (pamatyta 10-28). */
QRadioButton::indicator { width: 14px; height: 14px; border-radius: 8px;
                          border: 1px solid #5a5a5a; background: #2b2b2b; }
QRadioButton::indicator:hover { border: 1px solid #8a8a8a; }
QRadioButton::indicator:checked { width: 8px; height: 8px; border: 4px solid #1668C1;
                                  background: #ffffff; }
QRadioButton:disabled { color: #5a5a5a; }
QRadioButton::indicator:disabled { border: 1px solid #3a3a3a; background: #242424; }
QRadioButton::indicator:checked:disabled { border: 4px solid #233a55; background: #8a9bb0; }
QPlainTextEdit[perziura="taip"] { color: #9a9a9a; }
"""


def trukmes_ivertis(tekstas, greitis, pauze):
    """„≈ 5 val. 50 min garso · darbas ≈ 15 min" — iš simbolių skaičiaus (žr. SIMB_PER_SEK)."""
    dalys = balsas.dalys(tekstas)
    simb = sum(len(d) for d in dalys)
    if not simb:
        return ''
    pastraipu = sum(len(balsas.pastraipos(d)) for d in dalys) if simb < 500000 else simb // 300
    sek = simb / (SIMB_PER_SEK * max(0.3, greitis)) + max(0, pastraipu - len(dalys)) * pauze
    out = '≈ %s garso' % _laikas(sek)
    if sek > 120:
        out += ' · darbas ≈ %s' % _laikas(sek / DARBO_GREITIS)
    return out


def _laikas(sek):
    sek = int(round(sek))
    if sek < 60:
        return '%d s' % max(1, sek)
    v, m = divmod(sek // 60, 60)
    return ('%d val. %02d min' % (v, m)) if v else ('%d min' % m)


def ascii_tekstas(t):
    """„Fotosintezė ir šviesa" → „Fotosinteze ir sviesa" (ID3 žymoms, žr. ZYME_DI)."""
    return unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode('ascii')


def pavyzdzio_tekstas(tekstas):
    """Pavyzdžiui — paties vartotojo teksto pradžia (jis derina SAVAI medžiagai), ~2–3 sakiniai.
    Laukas tuščias — bendras pavyzdys."""
    pastraipos = balsas.pastraipos(tekstas or '')
    tekstas = ''
    for p in pastraipos:
        tekstas = (tekstas + '\n' + p).strip()
        if len(tekstas) >= 250:
            break
    if len(tekstas) > 400:
        sakiniai = re.split(r'(?<=[.!?…])\s+', tekstas)
        tekstas = ''
        for s in sakiniai:
            if tekstas and len(tekstas) + len(s) > 400:
                break
            tekstas = (tekstas + ' ' + s).strip()
        tekstas = tekstas[:600]
    return tekstas or PAVYZDYS


def vardas_is_teksto(tekstas):
    """Siūlomas mp3 vardas įrašytam tekstui: pirmi žodžiai, be Windows draudžiamų ženklų."""
    pirma = next((e.strip() for e in (tekstas or '').splitlines() if e.strip()), '')
    pirma = re.sub(r'[\\/:*?"<>|.,;!]+', ' ', pirma)
    pirma = ' '.join(pirma.split()[:6])[:50].strip()
    return pirma or 'igarsinta'


def daliu_keliai(mp3, kiek):
    """Viena dalis — tas pats kelias; kelios — `vardas_01.mp3`, `vardas_02.mp3`…"""
    if kiek <= 1:
        return [mp3]
    pagrindas = os.path.splitext(mp3)[0]
    return ['%s_%0*d.mp3' % (pagrindas, max(2, len(str(kiek))), i + 1) for i in range(kiek)]


def skaityk_tarima():
    try:
        with open(TARIMAS, encoding='utf-8') as f:
            return [[str(r), str(t)] for r, t in json.load(f)]
    except Exception:
        return []


class Darbininkas(QObject):
    """Įgarsina dalis fone ir kiekvieną rašo į savo mp3 gabalais (knyga netilptų atmintyje)."""
    progresas = pyqtSignal(int, int)                # padaryta pastraipų, iš viso
    baigta = pyqtSignal(str, str, float, object)    # būsena, klaida, sekundės, padaryti failai

    def __init__(self, raktas, greitis, dalys, keliai, eq, garsumas, pauze, tarimas):
        super().__init__()
        self.raktas, self.greitis, self.dalys, self.keliai = raktas, greitis, dalys, keliai
        self.eq, self.garsumas, self.pauze = list(eq), garsumas, pauze
        self.tarimas = [list(p) for p in tarimas]
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        # Kiekviena dalis — į laikiną failą; pavykus `os.replace`. Atšaukus ar nulūžus
        # nebaigtos dalies ankstesnis geras mp3 lieka nepaliestas.
        padaryti, sekundes, laikinas = [], 0.0, None
        try:
            darbas = [(k, balsas.pastraipos(balsas.taikyk_tarima(d, self.tarimas)))
                      for k, d in zip(self.keliai, self.dalys)]
            darbas = [(k, p) for k, p in darbas if p]
            if not darbas:
                self.baigta.emit('klaida', 'Nėra teksto, kurį būtų galima perskaityti.', 0.0, [])
                return
            is_viso = sum(len(p) for _, p in darbas)
            b = balsas.Balsas(self.raktas, self.greitis)
            pauze = np.zeros(int(b.daznis * self.pauze), dtype='float32')
            pabaiga = np.zeros(int(b.daznis * PABAIGOS_TYLA), dtype='float32')
            padaryta = 0
            for kelias, pastraipos in darbas:
                eq = garsas.Ekvalaizeris(self.eq, self.garsumas)    # kiekvienam failui sava būsena
                laikinas = kelias + '.kuriama'
                kadru = 0
                with sf.SoundFile(laikinas, 'w', b.daznis, 1, format='MP3') as f:
                    f.title = ascii_tekstas(os.path.splitext(os.path.basename(kelias))[0])
                    f.comment = ZYME_DI
                    for i, p in enumerate(pastraipos):
                        if self._stop:
                            break
                        a = b.pastraipa(p)
                        if a.size:
                            uodega = pauze if i < len(pastraipos) - 1 else pabaiga
                            # EQ per VISĄ srautą, pauzes irgi — filtrų būsena tęsiasi.
                            y = eq.apdorok(np.concatenate([a, uodega]), b.daznis)
                            f.write(y)
                            kadru += len(y)
                        padaryta += 1
                        self.progresas.emit(padaryta, is_viso)
                if self._stop:
                    self.baigta.emit('atsaukta', '', sekundes, padaryti)
                    return
                os.replace(laikinas, kelias)
                padaryti.append(kelias)
                sekundes += kadru / b.daznis
            self.baigta.emit('gerai', '', sekundes, padaryti)
        except PermissionError:
            self.baigta.emit('klaida', 'Nepavyko įrašyti failo:\n%s\n\nGal jis atidarytas kitoje '
                             'programoje (grotuve)? Uždarykite ją ir bandykite dar kartą.'
                             % (laikinas or '').replace('.kuriama', ''), sekundes, padaryti)
        except Exception as e:
            self.baigta.emit('klaida', '%s: %s' % (type(e).__name__, e), sekundes, padaryti)
        finally:
            if laikinas and os.path.exists(laikinas):
                try:
                    os.remove(laikinas)
                except OSError:
                    pass


class PavyzdzioDarbininkas(QObject):
    """Pavyzdžio sintezė perklausai — „sausa", be ekvalaizerio: jį grotuvas uždeda gyvai."""
    paruosta = pyqtSignal(object, int, str)     # garsas, dažnis, klaida ('' = gerai)

    def __init__(self, raktas, greitis, tekstas):
        super().__init__()
        self.raktas, self.greitis, self.tekstas = raktas, greitis, tekstas

    def run(self):
        try:
            b = balsas.Balsas(self.raktas, self.greitis)
            dalys = []
            for p in balsas.pastraipos(self.tekstas):
                dalys += [b.pastraipa(p), np.zeros(int(b.daznis * 0.5), dtype='float32')]
            self.paruosta.emit(np.concatenate(dalys) if dalys else np.zeros(0, 'float32'),
                               b.daznis, '')
        except Exception as e:
            self.paruosta.emit(None, 0, '%s: %s' % (type(e).__name__, e))


class Langas(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('saknis')
        self.setStyleSheet(STILIUS)
        self.setWindowTitle('%s — tekstas į mp3' % PAVADINIMAS)
        if os.path.exists(IKONA):
            self.setWindowIcon(QIcon(IKONA))
        self.setMinimumSize(640, 620)
        self._thread = None
        self._worker = None
        self._pthread = None
        self._pworker = None
        self._grojimas = None
        self._stabdyk_grojima = threading.Event()
        self._grojimo_klaida = ''
        self._grojimo_mygtukas = None
        self._grojimo_tekstas = ''
        self._laukia_mygtukas = None
        self._pavyzdys = None       # (raktas, greitis, tekstas, garsas, dažnis)
        self._dialogas = None
        self._tarimo_dialogas = None
        self._sukurti = set()       # šios sesijos mp3 — juos perrašom be klausimo
        self._paskutiniai = []      # paskutinio darymo failai — „Perklausyti" groja juos
        self._txt_kelias = ''       # „Iš failo" režimo failas
        self._lango_tekstas = ''    # „Iš lango" režimo tekstas, kol rodomas failas
        n = self._skaityk_nustatymus()
        self._aplankas = n.get('aplankas', os.path.expanduser('~'))
        eq = n.get('eq', [0] * len(garsas.JUOSTOS))
        self._eq = [int(v) for v in eq][:len(garsas.JUOSTOS)]
        self._eq += [0] * (len(garsas.JUOSTOS) - len(self._eq))
        self._garsumas = int(n.get('garsumas', garsas.GARSUMAS_NUMATYTAS))
        self._pauze = float(n.get('pauze', garsas.PAUZE_NUMATYTA))
        self._tarimas = skaityk_tarima()
        # Grotuvo gija skaito TIK šitą kortežą (vienas priskyrimas — saugu tarp gijų).
        self._eq_dabar = (tuple(self._eq), self._garsumas)

        # Kalba → balsas, kaip SpeakDream. Kol kas viena kalba, bet sąrašas jau tikras.
        self.kalba = QComboBox()
        for kodas, (vardas, _) in balsas.KALBOS.items():
            self.kalba.addItem(vardas, kodas)
        self.balsas = QComboBox()
        i = self.kalba.findData(n.get('kalba'))
        if i >= 0:
            self.kalba.setCurrentIndex(i)
        self._uzpildyk_balsus(n.get('balsas'))
        self.kalba.currentIndexChanged.connect(lambda _i: self._uzpildyk_balsus(None))
        self.b_pavyzdys = QPushButton('▸')
        self.b_pavyzdys.setObjectName('ikona')
        self.b_pavyzdys.setToolTip('Pasiklausyti: pažymėtą tekstą arba teksto pradžią, '
                                   'su dabartiniais nustatymais')
        self.b_pavyzdys.clicked.connect(self._pavyzdys_paspaustas)

        # Kaip Vertėjo slankiklis: 0,6–1,4 karto, 1,0 — balso numatytasis tempas.
        self.greitis = QSlider(Qt.Orientation.Horizontal)
        self.greitis.setRange(60, 140)
        self.greitis.setSingleStep(5)
        self.greitis.setPageStep(10)
        self.greitis_zyme = QLabel()
        self.greitis_zyme.setMinimumWidth(44)
        self.greitis.valueChanged.connect(self._greitis_pakeistas)
        self.greitis.setValue(int(n.get('greitis', 100)))
        self._greitis_pakeistas(self.greitis.value())
        self.b_numatytas = QPushButton('↺')
        self.b_numatytas.setObjectName('ikona')
        self.b_numatytas.setToolTip('Balso numatytasis greitis (1,00×)')
        self.b_numatytas.clicked.connect(lambda: self.greitis.setValue(100))
        greitis = QHBoxLayout()
        greitis.setSpacing(8)
        lec, grei = QLabel('lėčiau'), QLabel('greičiau')
        lec.setObjectName('uzuomina')
        grei.setObjectName('uzuomina')
        greitis.addWidget(lec)
        greitis.addWidget(self.greitis, 1)
        greitis.addWidget(grei)
        greitis.addWidget(self.greitis_zyme)
        greitis.addWidget(self.b_numatytas)

        tinklas = QGridLayout()
        tinklas.setHorizontalSpacing(8)
        tinklas.setVerticalSpacing(8)
        tinklas.addWidget(QLabel('Kalba'), 0, 0)
        tinklas.addWidget(self.kalba, 0, 1, 1, 2)
        tinklas.addWidget(QLabel('Balsas'), 1, 0)
        tinklas.addWidget(self.balsas, 1, 1)
        tinklas.addWidget(self.b_pavyzdys, 1, 2, Qt.AlignmentFlag.AlignLeft)
        tinklas.addWidget(QLabel('Greitis'), 2, 0)
        tinklas.addLayout(greitis, 2, 1, 1, 2)
        tinklas.setColumnStretch(1, 1)
        tinklas.setColumnMinimumWidth(0, 72)

        # Iš kur tekstas — skrituliukai (Roberto 10-28: „kokia močiutė 100 puslapių knygą
        # sugalvos įsikelti"). „Iš failo": knygai lango nereikia — rodom vardą, dydį, kiek
        # užtruks ir tik pradžią; failas skaitomas darymo metu (pataisei Užrašinėje — nieko
        # iš naujo rinktis nereikia). „Iš lango": įklijuoji ar rašai, kaip dėstytojas iš skaidrių.
        self.r_failas = QRadioButton('Iš failo')
        self.r_langas = QRadioButton('Iš lango')
        self.r_failas.toggled.connect(self._rezimas_pakeistas)
        self.b_tarimas = QPushButton('Tarimas…')
        self.b_tarimas.setToolTip('Tarimo žodynėlis: kaip parašyta → kaip turi skambėti')
        self.b_tarimas.clicked.connect(self._rodyk_tarima)
        saltinis = QHBoxLayout()
        saltinis.setSpacing(18)
        zyme = QLabel('Tekstas')
        zyme.setMinimumWidth(72)
        saltinis.addWidget(zyme)
        self.b_isvalyti = QPushButton('Išvalyti')
        self.b_isvalyti.setToolTip('Išvalyti pasirinktą šaltinį: failą arba lango tekstą')
        self.b_isvalyti.clicked.connect(self._isvalyk)
        saltinis.addWidget(self.r_failas)
        saltinis.addWidget(self.r_langas)
        saltinis.addStretch(1)
        saltinis.addWidget(self.b_isvalyti)
        saltinis.addWidget(self.b_tarimas)

        # Failo eilutė NESLEPIAMA kitame režime — užgęsta ir užsirakina (taisyklė iš
        # `SQL uzklausos GG` `set_group_state`, Roberto 10-28: „skrituliukai GUI gerai išėjo"):
        # langas nešokinėja, o žmogus mato, kas būtų kitame režime.
        self.txt = QLineEdit()
        self.txt.setReadOnly(True)
        self.txt.setPlaceholderText('.txt failas — spauskite „Pasirinkti…"')
        self.b_txt = QPushButton('Pasirinkti…')
        self.b_txt.clicked.connect(self._atidaryk_txt)
        self.teksto_info = QLabel()
        self.teksto_info.setObjectName('uzuomina')
        self.teksto_info.setWordWrap(True)
        self.failo_eilute = QWidget()
        fe = QHBoxLayout(self.failo_eilute)
        fe.setContentsMargins(0, 0, 0, 0)
        fe.setSpacing(8)
        fe.addWidget(self.txt, 1)
        fe.addWidget(self.b_txt)

        self.tekstas = QPlainTextEdit()
        self.tekstas.setPlaceholderText(
            'Įklijuokite ar įrašykite tekstą čia.\n\n'
            'Tuščia eilutė — pauzė tarp pastraipų.\n'
            'Eilutė  ---  padalins įrašą į kelis mp3 (pvz., po vieną kiekvienai skaidrei).\n'
            'Pažymėkite fragmentą ir spauskite ▸ — išgirsite tik jį.')
        self.tekstas.setMinimumHeight(180)
        self.tekstas.textChanged.connect(self._tekstas_pakeistas)
        self._failo_tekstas = ''        # „Iš failo" režimu — paskutinį kartą perskaitytas

        self.mp3 = QLineEdit()
        self.mp3.setPlaceholderText('kur įrašyti .mp3 (paklausiu, jei tuščia)')
        self.mp3.setToolTip('Jei tekste yra „---", failai bus numeruojami: vardas_01.mp3, vardas_02.mp3…')
        self.b_mp3 = QPushButton('Pasirinkti…')
        self.b_mp3.clicked.connect(self._rink_mp3)
        irasyti = QHBoxLayout()
        irasyti.setSpacing(8)
        zyme = QLabel('Įrašyti į')
        zyme.setMinimumWidth(72)
        irasyti.addWidget(zyme)
        irasyti.addWidget(self.mp3, 1)
        irasyti.addWidget(self.b_mp3)

        self.daryti = QPushButton('Daryti mp3')
        self.daryti.setProperty('aktyvus', 'taip')
        self.daryti.clicked.connect(self._daryti_paspaustas)
        self.klausyti = QPushButton('▶  Perklausyti')
        self.klausyti.clicked.connect(self._klausyti_paspaustas)
        mygtukai = QHBoxLayout()
        mygtukai.setSpacing(6)
        mygtukai.addWidget(self.daryti, 1)
        mygtukai.addWidget(self.klausyti, 1)

        self.taskas = QLabel('●')
        self.busena = QLabel()
        self.busena.setObjectName('busena')
        self.busena.setWordWrap(True)
        self.juosta = QProgressBar()
        self.juosta.setTextVisible(False)
        self.juosta.setRange(0, 1)
        self.juosta.setValue(0)
        self.b_nust = QPushButton('⚙')
        self.b_nust.setObjectName('ikona')
        self.b_nust.setToolTip('Garso nustatymai: ekvalaizeris, garsumas, pauzės')
        self.b_nust.clicked.connect(self._rodyk_nustatymus)
        # "?" - šeimos standartas (Diktuoklė, SDF etalonas): meniu su trim punktais,
        # instrukcija gyvena PAČIOJE programoje, tinklas — tik paspaudus „Klauskite DI".
        self.b_pag = QPushButton('?')
        self.b_pag.setObjectName('ikona')
        self.b_pag.setToolTip('Pagalba')
        pagalba = QMenu(self.b_pag)
        pagalba.addAction('Apie...', self._rodyk_apie)
        pagalba.addAction('Instrukcija', self._rodyk_instrukcija)
        pagalba.addAction('Neradote atsakymo? Klauskite DI', self._klausk_di)
        self.b_pag.setMenu(pagalba)
        apacia = QHBoxLayout()
        apacia.setSpacing(8)
        apacia.addWidget(self.taskas, 0, Qt.AlignmentFlag.AlignTop)
        apacia.addWidget(self.busena, 1)
        apacia.addWidget(self.b_nust, 0, Qt.AlignmentFlag.AlignTop)
        apacia.addWidget(self.b_pag, 0, Qt.AlignmentFlag.AlignTop)

        visas = QVBoxLayout(self)
        visas.setContentsMargins(12, 10, 12, 10)
        visas.setSpacing(10)
        visas.addLayout(tinklas)
        visas.addLayout(saltinis)
        visas.addWidget(self.failo_eilute)
        visas.addWidget(self.tekstas, 1)
        visas.addWidget(self.teksto_info)
        visas.addLayout(irasyti)
        visas.addLayout(mygtukai)
        visas.addWidget(self.juosta)
        visas.addLayout(apacia)

        # Be klaviatūros fokuso rėmelio ant mygtukų (Roberto pastaba Diktuoklei 09-08).
        for b in (self.b_pavyzdys, self.b_numatytas, self.b_txt, self.b_isvalyti, self.b_tarimas,
                  self.b_mp3, self.daryti, self.klausyti, self.b_nust, self.b_pag,
                  self.r_failas, self.r_langas):
            b.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Išjungiami darbo metu — po vieną (⛔ išjungtas tėvas numarina vaikus).
        self._valdikliai = [self.kalba, self.balsas, self.b_pavyzdys, self.greitis,
                            self.b_numatytas, self.r_failas, self.r_langas, self.b_txt,
                            self.b_isvalyti, self.b_tarimas, self.tekstas, self.mp3, self.b_mp3,
                            self.klausyti, self.b_nust]

        self._laikmatis = QTimer(self)
        self._laikmatis.setInterval(200)
        self._laikmatis.timeout.connect(self._ar_dar_groja)
        self.greitis.valueChanged.connect(lambda _v: self._atnaujink_info())

        # Režimas — iš nustatymų; pirmą kartą „Iš failo" (Roberto pradinis užsakymas).
        (self.r_langas if n.get('rezimas') == 'langas' else self.r_failas).setChecked(True)
        self._rezimas_pakeistas()
        self._rodyk_busena('Pasirinkite .txt failą arba įklijuokite tekstą, tada „Daryti mp3".',
                           PILKA)

    # ---- būsena, balsai, greitis, tekstas ------------------------------------------------
    def _rodyk_busena(self, tekstas, spalva):
        self.busena.setText(tekstas)
        self.taskas.setStyleSheet('color: %s; font-size: 15px;' % spalva)

    def _uzpildyk_balsus(self, norimas):
        self.balsas.clear()
        for raktas in balsas.KALBOS[self.kalba.currentData()][1]:
            self.balsas.addItem(balsas.BALSAI[raktas][0], raktas)
        i = self.balsas.findData(norimas)
        self.balsas.setCurrentIndex(i if i >= 0 else 0)

    def _greitis_pakeistas(self, v):
        self.greitis_zyme.setText(('%.2f×' % (v / 100.0)).replace('.', ','))

    # ---- iš kur tekstas ---------------------------------------------------------------
    def is_failo(self):
        return self.r_failas.isChecked()

    def _failo_eilute_pagal_rezima(self):
        # Vaikai po vieną, ne tėvas (⛔ išjungtas tėvas numarina vaikus).
        for w in (self.txt, self.b_txt):
            w.setEnabled(self.is_failo())

    def _rezimas_pakeistas(self, *_a):
        failas = self.is_failo()
        self._failo_eilute_pagal_rezima()
        self.tekstas.setReadOnly(failas)
        self.tekstas.setProperty('perziura', 'taip' if failas else 'ne')
        self.tekstas.style().unpolish(self.tekstas)
        self.tekstas.style().polish(self.tekstas)
        self.tekstas.blockSignals(True)
        if failas:
            self.tekstas.setPlainText(self._perziura(self._failo_tekstas))
            self.tekstas.setPlaceholderText('Čia bus rodoma failo pradžia.')
        else:
            self.tekstas.setPlainText(self._lango_tekstas)
            self.tekstas.setPlaceholderText(
                'Įklijuokite ar įrašykite tekstą čia.\n\n'
                'Tuščia eilutė — pauzė tarp pastraipų.\n'
                'Eilutė  ---  padalins įrašą į kelis mp3 (pvz., po vieną kiekvienai skaidrei).\n'
                'Pažymėkite fragmentą ir spauskite ▸ — išgirsite tik jį.')
        self.tekstas.blockSignals(False)
        if failas and self._txt_kelias:
            self.mp3.setText(os.path.splitext(self._txt_kelias)[0] + '.mp3')
        self._atnaujink_info()

    @staticmethod
    def _perziura(tekstas):
        if len(tekstas) <= PERZIUROS_RIBA:
            return tekstas
        return tekstas[:PERZIUROS_RIBA].rstrip() + '\n\n[… rodoma tik pradžia — įgarsinamas visas failas]'

    def saltinio_tekstas(self, is_naujo=True):
        """Tai, kas bus įgarsinta. „Iš failo" — failas perskaitomas IŠ NAUJO (pataisei
        Užrašinėje — gauni pataisytą); „Iš lango" — laukas."""
        if not self.is_failo():
            return self.tekstas.toPlainText()
        if self._txt_kelias and is_naujo:
            self._failo_tekstas = balsas.skaityk_teksta(self._txt_kelias)
        return self._failo_tekstas

    def _tekstas_pakeistas(self):
        if not self.is_failo():
            self._lango_tekstas = self.tekstas.toPlainText()
        self._atnaujink_info()

    def _atnaujink_info(self):
        t = self._failo_tekstas if self.is_failo() else self.tekstas.toPlainText()
        if not t.strip():
            self.teksto_info.setText('')
            return
        n = len(balsas.dalys(t))
        dalys = {1: ''}.get(n, ' · %d mp3 failai' % n if n < 10 else ' · %d mp3 failų' % n)
        info = '%s simb.%s · %s' % ('{:,}'.format(len(t)).replace(',', ' '), dalys,
                                    trukmes_ivertis(t, self.greitis.value() / 100.0, self._pauze))
        if self.is_failo() and self._txt_kelias:
            info = os.path.basename(self._txt_kelias) + ' — ' + info
        self.teksto_info.setText(info)

    def _isvalyk(self):
        """Išvalo AKTYVŲ šaltinį: failo režime — failą, lango režime — lango tekstą."""
        if self.is_failo():
            self._txt_kelias = ''
            self._failo_tekstas = ''
            self.txt.clear()
            self.tekstas.blockSignals(True)
            self.tekstas.clear()
            self.tekstas.blockSignals(False)
            self._atnaujink_info()
        else:
            self.tekstas.clear()        # textChanged pats atnaujina _lango_tekstas ir info

    # ---- nustatymai -------------------------------------------------------------------
    def _skaityk_nustatymus(self):
        try:
            with open(NUSTATYMAI, encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _issaugok_nustatymus(self):
        try:
            os.makedirs(APLANKAS, exist_ok=True)
            with open(NUSTATYMAI, 'w', encoding='utf-8') as f:
                json.dump({'kalba': self.kalba.currentData(), 'balsas': self.balsas.currentData(),
                           'greitis': self.greitis.value(), 'aplankas': self._aplankas,
                           'eq': self._eq, 'garsumas': self._garsumas, 'pauze': self._pauze,
                           'rezimas': 'failas' if self.is_failo() else 'langas'},
                          f, ensure_ascii=False, indent=1)
            with open(TARIMAS, 'w', encoding='utf-8') as f:
                json.dump(self._tarimas, f, ensure_ascii=False, indent=1)
        except Exception:
            pass

    def _rodyk_nustatymus(self):
        self._stabdyk_groti()
        # Vienas langas visam programos gyvenimui: jis pats laiko savo reikšmes, o mygtukas,
        # kurį grotuvas perjunginėja, niekada neišnyksta po kojomis.
        if self._dialogas is None:
            self._dialogas = GarsoNustatymai(self, self._eq, self._garsumas, self._pauze)
            self._dialogas.pakeista.connect(self._nustatymai_pakeisti)
            self._dialogas.klausyti.connect(
                lambda: self._pavyzdys_paspaustas(self._dialogas.b_klausyti))
        self._dialogas.exec()
        self._stabdyk_groti()
        self._issaugok_nustatymus()

    def _nustatymai_pakeisti(self):
        d = self._dialogas
        self._eq, self._garsumas, self._pauze = d.eq(), d.garsumo_db(), d.pauzes_s()
        self._eq_dabar = (tuple(self._eq), self._garsumas)
        self._atnaujink_info()

    def _rodyk_tarima(self):
        self._stabdyk_groti()
        if self._tarimo_dialogas is None:
            self._tarimo_dialogas = TarimoZodynas(self, self._tarimas)
            # Žodynėlio eilutė grojama TOKIA, kokia įrašyta — be paties žodynėlio.
            self._tarimo_dialogas.klausyti.connect(
                lambda t: self._pavyzdys_paspaustas(self._tarimo_dialogas.b_klausyti, t, False))
        self._tarimo_dialogas.exec()
        self._stabdyk_groti()
        self._tarimas = self._tarimo_dialogas.poros()
        self._issaugok_nustatymus()

    # ---- "?" meniu (Diktuoklės receptas) ----------------------------------------------
    def _uzdarymo_mygtukas(self, dlg):
        eilute = QHBoxLayout()
        eilute.addStretch(1)
        b = QPushButton('Uždaryti')
        b.clicked.connect(dlg.reject)
        eilute.addWidget(b)
        return eilute

    def _rodyk_apie(self):
        """Apie... - logo, pavadinimas, aprašas, versija, autoriai, balsų kilmė ir licencijos
        (Ingutės licencija reikalauja nurodyti kilmę ir perduoti LICENSE-VOICE)."""
        dlg = QDialog(self)
        dlg.setWindowTitle('Apie programą')
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(18, 16, 18, 14)
        lay.setSpacing(10)
        virsus = QHBoxLayout()
        virsus.setSpacing(14)
        logo = QLabel()
        if os.path.exists(IKONA):
            logo.setPixmap(QIcon(IKONA).pixmap(64, 64))
        virsus.addWidget(logo, alignment=Qt.AlignmentFlag.AlignTop)
        info = QVBoxLayout()
        info.setSpacing(4)
        pavadinimas = QLabel(PAVADINIMAS)
        pavadinimas.setStyleSheet('font-size: 18px; font-weight: bold; color: #ffffff;')
        info.addWidget(pavadinimas)
        info.addWidget(QLabel('Tekstas į mp3 lietuvišku balsu, be interneto —\n'
                              'tekstas niekur nesiunčiamas, viskas lieka kompiuteryje.'))
        info.addWidget(QLabel('Versija %s' % VERSIJA))
        autoriai = QLabel('Robertas & Claude')
        autoriai.setStyleSheet('color: #8f8f8f;')
        info.addWidget(autoriai)
        # DI žymėjimas VIRŠUJE (ES DI akto 50 str., kaip Diktuoklėje).
        di = QLabel('Sukurta naudojant DI: kodą rašė Claude, ikona — DI.\n'
                    'Įgarsinti įrašai yra sintetiniai — mp3 faile tai pažymėta.')
        di.setStyleSheet('color: #E8B84B; font-size: 12px;')
        info.addWidget(di)
        virsus.addLayout(info)
        lay.addLayout(virsus)
        kilme = QLabel('Reginutė — mokyta iš LIEPA garsyno (CC BY 4.0)\n'
                       'Ingutė — išaugo iš Reginutės modelio (NewGenLTU OpenRAIL-D, žr. LICENSE-VOICE)\n'
                       'Varikliai — Piper (GPL-3.0), pedalboard (GPL-3.0)')
        kilme.setStyleSheet('color: #9a9a9a; font-size: 12px;')
        lay.addWidget(kilme)
        nuoroda = QLabel('Kūrėjo puslapis: <a href="%s" style="color:#4f9cf7; '
                         'font-weight:bold;">GitHub</a>' % KUREJO_PUSLAPIS)
        nuoroda.setOpenExternalLinks(True)
        lay.addWidget(nuoroda)
        lay.addLayout(self._uzdarymo_mygtukas(dlg))
        dlg.exec()

    def _rodyk_instrukcija(self):
        """README rodomas pačios programos lange su slinktimi — jokio Notepad, jokio tinklo."""
        try:
            with open(README, encoding='utf-8', errors='replace') as f:
                tekstas = f.read()
        except OSError as e:
            QMessageBox.warning(self, 'Pagalba', 'Nepavyko atidaryti instrukcijos: %s' % e)
            return
        dlg = QDialog(self)
        dlg.setWindowTitle('Instrukcija')
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(14, 14, 14, 12)
        rodinys = QPlainTextEdit(tekstas)
        rodinys.setReadOnly(True)
        rodinys.setFont(QFont('Consolas', 10))   # ASCII antraštės lygiuojasi
        lay.addWidget(rodinys)
        lay.addLayout(self._uzdarymo_mygtukas(dlg))
        dlg.resize(720, 540)
        dlg.exec()

    def _klausk_di(self):
        """Atidaro claude.ai su paruoštu promptu. claude.ai/new?q= tik UŽPILDO laukelį —
        siunčia pats žmogus. Tinklas TIK čia."""
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Neradote atsakymo? Klauskite DI')
        if os.path.exists(IKONA):
            dlg.setIconPixmap(QIcon(IKONA).pixmap(64, 64))
        dlg.setText(
            'Kas įvyks paspaudus OK:\n\n'
            '1. Atsidarys interneto naršyklė su DI padėjėjo claude.ai\n'
            '   puslapiu. Žinutės laukelyje jau bus įrašyta angliška\n'
            '   pradžia — prisistatymas, kas per programa.\n'
            '2. NEIŠSIGĄSKITE raudono pranešimo virš žinutės —\n'
            '   claude.ai jį rodo visada, kai tekstas ateina per nuorodą.\n'
            '3. Žinutės gale, po žodžių „My question:", įrašykite SAVO\n'
            '   klausimą — galima lietuviškai! — ir spauskite siuntimą.\n'
            '4. Jei DI atsakys angliškai — paprašykite: „atsakyk\n'
            '   lietuviškai".\n\n'
            'Pastaba: claude.ai gali paprašyti prisijungti (nemokama\n'
            'paskyra). Niekas neišsiunčiama be jūsų rankos.')
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        dlg.button(QMessageBox.StandardButton.Cancel).setText('Atšaukti')
        if dlg.exec() != QMessageBox.StandardButton.Ok:
            return
        promptas = (
            'Please read %s first - it is the author\'s briefing about the app "Skaitykle"'
            ' (Windows program that reads text aloud in a Lithuanian voice - Ingutė or'
            ' Reginutė - and saves MP3: text pasted into the window or opened from .txt;'
            ' a line "---" splits it into several MP3 files; speed slider, pronunciation'
            ' list, 7-band equaliser in the gear menu; nothing leaves the PC). If that link'
            ' does not open yet, the same file, AI_CONSULTANT_BRIEF.md, sits next to the'
            ' program; ask me to paste it. Source: %s. Then answer my question in plain, human'
            ' language, in the language I write in, no programmer jargon. My question: '
            % (BRIEF_URL, KUREJO_PUSLAPIS))
        webbrowser.open('https://claude.ai/new?q=' + urllib.parse.quote(promptas))

    # ---- failai -----------------------------------------------------------------------
    def _atidaryk_txt(self):
        kelias, _ = QFileDialog.getOpenFileName(self, 'Tekstas, kurį įgarsinti', self._aplankas,
                                                'Tekstas (*.txt);;Visi failai (*)')
        if not kelias:
            return
        kelias = os.path.normpath(kelias)
        try:
            tekstas = balsas.skaityk_teksta(kelias)
        except OSError as e:
            QMessageBox.warning(self, PAVADINIMAS, 'Nepavyko atidaryti:\n%s\n\n%s' % (kelias, e))
            return
        self._aplankas = os.path.dirname(kelias)
        self._txt_kelias = kelias
        self._failo_tekstas = tekstas
        self.txt.setText(kelias)
        self.tekstas.blockSignals(True)
        self.tekstas.setPlainText(self._perziura(tekstas))
        self.tekstas.blockSignals(False)
        # mp3 iškart šalia, tuo pačiu vardu — dažniausiai to ir reikia; pakeisti galima.
        self.mp3.setText(os.path.splitext(kelias)[0] + '.mp3')
        self._atnaujink_info()

    def _rink_mp3(self):
        pradzia = self.mp3.text().strip() or os.path.join(
            self._aplankas, vardas_is_teksto(self.saltinio_tekstas(is_naujo=False)) + '.mp3')
        kelias, _ = QFileDialog.getSaveFileName(self, 'Kur įrašyti mp3', pradzia, 'MP3 (*.mp3)')
        if not kelias:
            return ''
        kelias = os.path.normpath(kelias)
        if not kelias.lower().endswith('.mp3'):
            kelias += '.mp3'
        self._aplankas = os.path.dirname(kelias)
        self.mp3.setText(kelias)
        return kelias

    # ---- darymas ----------------------------------------------------------------------
    def _daryti_paspaustas(self):
        if self._thread is not None and self._ar_dirba(self._thread):
            self._worker.stop()
            self._rodyk_busena('Atšaukiama…', GELTONA)
            self.daryti.setEnabled(False)
            return
        if self.is_failo() and not self._txt_kelias:
            QMessageBox.information(self, PAVADINIMAS, 'Pasirinkite .txt failą — arba pažymėkite '
                                    '„Iš lango" ir įklijuokite tekstą.')
            return
        try:
            dalys = balsas.dalys(self.saltinio_tekstas())
        except OSError as e:
            QMessageBox.warning(self, PAVADINIMAS, 'Nepavyko perskaityti failo:\n%s\n\n%s'
                                % (self._txt_kelias, e))
            return
        if not dalys:
            QMessageBox.information(self, PAVADINIMAS, 'Nėra teksto, kurį būtų galima perskaityti.')
            return
        mp3 = self.mp3.text().strip() or self._rink_mp3()
        if not mp3:
            return
        if not mp3.lower().endswith('.mp3'):
            mp3 += '.mp3'
            self.mp3.setText(mp3)
        if not os.path.isdir(os.path.dirname(os.path.abspath(mp3))):
            QMessageBox.warning(self, PAVADINIMAS, 'Tokio aplanko nėra:\n%s'
                                % os.path.dirname(os.path.abspath(mp3)))
            return
        keliai = daliu_keliai(os.path.abspath(mp3), len(dalys))
        svetimi = [k for k in keliai if os.path.exists(k)
                   and os.path.normcase(k) not in self._sukurti]
        if svetimi and QMessageBox.question(
                self, PAVADINIMAS, 'Jau yra %s:\n%s\n\nPerrašyti?' % (
                    'failas' if len(svetimi) == 1 else '%d failai' % len(svetimi),
                    '\n'.join(svetimi[:5]) + ('\n…' if len(svetimi) > 5 else ''))
        ) != QMessageBox.StandardButton.Yes:
            return
        self._stabdyk_groti()
        self._issaugok_nustatymus()

        # Reikšmės nuskaitomos ČIA, pagrindinėje gijoje (guard: GUI fone neliečiamas).
        self._worker = Darbininkas(self.balsas.currentData(), self.greitis.value() / 100.0,
                                   dalys, keliai, self._eq, self._garsumas, self._pauze,
                                   self._tarimas)
        self._thread = QThread()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progresas.connect(self._progresas)
        self._worker.baigta.connect(self._baigta)
        self._worker.baigta.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        for v in self._valdikliai:
            v.setEnabled(False)
        self.daryti.setText('Atšaukti')
        self.juosta.setRange(0, 0)          # „dirba", kol neaišku, kiek pastraipų
        self._rodyk_busena('Kraunamas balsas…', GELTONA)
        self._thread.start()

    def _progresas(self, padaryta, is_viso):
        self.juosta.setRange(0, is_viso)
        self.juosta.setValue(padaryta)
        self._rodyk_busena('Įgarsinta pastraipų: %d iš %d' % (padaryta, is_viso), GELTONA)

    def _baigta(self, kaip, tekstas, sekundes, padaryti):
        for v in self._valdikliai:
            v.setEnabled(True)
        self._failo_eilute_pagal_rezima()      # kitaip po darbo užsidegtų neaktyvi eilutė
        self.daryti.setEnabled(True)
        self.daryti.setText('Daryti mp3')
        self.juosta.setRange(0, 1)
        for k in padaryti:
            self._sukurti.add(os.path.normcase(k))
        if padaryti:
            self._paskutiniai = list(padaryti)
        m, s = divmod(int(round(sekundes)), 60)
        v, m = divmod(m, 60)
        trukme = ('%d:%02d:%02d' % (v, m, s)) if v else ('%d:%02d' % (m, s))
        kas = (os.path.basename(padaryti[0]) if len(padaryti) == 1 else
               '%d failai (%s … %s)' % (len(padaryti), os.path.basename(padaryti[0]),
                                        os.path.basename(padaryti[-1])) if padaryti else '')
        if kaip == 'gerai':
            self.juosta.setValue(1)
            self._rodyk_busena('Paruošta: %s, iš viso %s. Paklausykite; nepatiko — pakeiskite '
                               'greitį, balsą ar garsą (⚙) ir darykite iš naujo.' % (kas, trukme),
                               ZALIA)
        elif kaip == 'atsaukta':
            self.juosta.setValue(0)
            self._rodyk_busena('Atšaukta.%s Nebaigto failo ankstesnė versija (jei buvo) '
                               'nepaliesta.' % ((' Spėjo: %s.' % kas) if padaryti else ''), PILKA)
        else:
            self.juosta.setValue(0)
            self._rodyk_busena('Nepavyko.', RAUDONA)
            QMessageBox.warning(self, PAVADINIMAS, tekstas)

    # ---- pavyzdys (▸, dantračio ir žodynėlio „Pasiklausyti") ------------------------
    def _pavyzdys_paspaustas(self, mygtukas=None, tekstas=None, su_tarimu=True):
        mygtukas = mygtukas if isinstance(mygtukas, QPushButton) else self.b_pavyzdys
        if self._grojimas is not None and self._grojimas.is_alive():
            self._stabdyk_groti()
            return
        if self._pthread is not None and self._ar_dirba(self._pthread):
            return
        if tekstas is None:
            # Pažymėtas fragmentas — jei yra; kitaip teksto pradžia. Qt pažymėtame tekste
            # eilutes skiria U+2029, ne „\n".
            pazymeta = self.tekstas.textCursor().selectedText().replace('\u2029', '\n').strip()
            visas = self.saltinio_tekstas(is_naujo=False)
            tekstas = pazymeta[:PAZYMETO_RIBA] if pazymeta else pavyzdzio_tekstas(
                balsas.dalys(visas)[0] if visas.strip() else '')
        if su_tarimu:
            tekstas = balsas.taikyk_tarima(tekstas, self._tarimas)
        raktas = self.balsas.currentData()
        greitis = self.greitis.value() / 100.0
        p = self._pavyzdys
        if p is not None and p[:3] == (raktas, greitis, tekstas):
            self._pradek_groti(mygtukas, garsas_=p[3], daznis=p[4])
            return
        # Sintezė — fone (pirmą kartą ~2 s su balso krovimu).
        self._laukia_mygtukas = mygtukas
        self._pworker = PavyzdzioDarbininkas(raktas, greitis, tekstas)
        self._pthread = QThread()
        self._pworker.moveToThread(self._pthread)
        self._pthread.started.connect(self._pworker.run)
        self._pworker.paruosta.connect(self._pavyzdys_paruostas)
        self._pworker.paruosta.connect(self._pthread.quit)
        self._pthread.finished.connect(self._pworker.deleteLater)
        self._pthread.finished.connect(self._pthread.deleteLater)
        self.daryti.setEnabled(False)
        mygtukas.setEnabled(False)
        self._rodyk_busena('Ruošiamas pavyzdys…', GELTONA)
        self._pthread.start()

    def _pavyzdys_paruostas(self, garsas_, daznis, klaida):
        mygtukas = self._laukia_mygtukas
        mygtukas.setEnabled(True)
        self.daryti.setEnabled(True)
        if klaida:
            self._rodyk_busena('Pavyzdžio paruošti nepavyko.', RAUDONA)
            QMessageBox.warning(self, PAVADINIMAS, klaida)
            return
        w = self._pworker
        self._pavyzdys = (w.raktas, w.greitis, w.tekstas, garsas_, daznis)
        if mygtukas.window() is not self and not mygtukas.window().isVisible():
            self._rodyk_busena('Pavyzdys paruoštas.', PILKA)
            return                  # dialogas jau uždarytas — negrojam „iš niekur"
        self._rodyk_busena('Groja pavyzdys — garso nustatymus (⚙) galima keisti grojant.', ZALIA)
        self._pradek_groti(mygtukas, garsas_=garsas_, daznis=daznis)

    # ---- grojimas: vienas kelias ir failams, ir pavyzdžiui ----------------------------
    def _klausyti_paspaustas(self):
        if self._grojimas is not None and self._grojimas.is_alive():
            self._stabdyk_groti()
            return
        # Grojam PAČIUS įrašytus failus, o ne atmintį: girdi lygiai tai, ką gaus studentai.
        failai = [k for k in self._paskutiniai if os.path.isfile(k)]
        mp3 = self.mp3.text().strip()
        if not failai and mp3 and os.path.isfile(mp3):
            failai = [mp3]
        if not failai:
            QMessageBox.information(self, PAVADINIMAS,
                                    'Dar nėra ką klausyti — pirma spauskite „Daryti mp3".')
            return
        self._pradek_groti(self.klausyti, keliai=failai)

    def _pradek_groti(self, mygtukas, keliai=None, garsas_=None, daznis=0):
        self._stabdyk_grojima = threading.Event()
        self._grojimo_klaida = ''
        self._grojimo_mygtukas = mygtukas
        self._grojimo_tekstas = mygtukas.text()
        self._grojimas = threading.Thread(target=self._grok,
                                          args=(keliai, garsas_, daznis, self._stabdyk_grojima),
                                          daemon=True)
        self._grojimas.start()
        mygtukas.setText('■  Sustabdyti' if len(self._grojimo_tekstas) > 2 else '■')
        self.daryti.setEnabled(False)
        self._laikmatis.start()

    def _grok(self, keliai, garsas_, daznis, stabdyk):
        """Fono gija (ne Qt): GUI čia neliečiam. Failai groja tokie, kokie yra (iš eilės);
        pavyzdys — per ekvalaizerį, kurio reikšmės imamos KIEKVIENAM blokui."""
        try:
            # ⛔ mp3 skaitom pedalboard'u, NE soundfile: libsndfile 1.2.2 mp3 dekoderis, skaitant
            # dalimis, gadina garsą ties kiekvienos dalies riba (iki 0,33 amplitudės, ~2000 imčių
            # 12 s įraše — girdisi spragtelėjimai, nors failas sveikas). Rado gyvas bandymas
            # 10-28 (mpg123 „part2_3_length too large"); pedalboard dalimis = visas, skirtumas 0.
            for kelias in keliai or []:
                if stabdyk.is_set():
                    break
                with AudioFile(kelias) as f, sd.OutputStream(samplerate=int(f.samplerate),
                                                             channels=f.num_channels,
                                                             dtype='float32') as srautas:
                    while not stabdyk.is_set() and f.tell() < f.frames:
                        blokas = f.read(4096)
                        if not blokas.shape[1]:
                            break
                        srautas.write(np.ascontiguousarray(blokas.T))
            if keliai:
                return
            dabar = self._eq_dabar
            eq = garsas.Ekvalaizeris(*dabar)
            with sd.OutputStream(samplerate=daznis, channels=1, dtype='float32') as srautas:
                for i in range(0, len(garsas_), 2048):
                    if stabdyk.is_set():
                        break
                    if self._eq_dabar is not dabar:
                        dabar = self._eq_dabar
                        eq.nustatyk(*dabar)
                    y = eq.apdorok(garsas_[i:i + 2048], daznis)
                    srautas.write(np.ascontiguousarray(y.reshape(-1, 1)))
        except Exception as e:
            self._grojimo_klaida = '%s: %s' % (type(e).__name__, e)

    def _stabdyk_groti(self):
        self._stabdyk_grojima.set()
        if self._grojimas is not None:
            self._grojimas.join(2.0)
        self._ar_dar_groja()

    def _ar_dar_groja(self):
        if self._grojimas is not None and self._grojimas.is_alive():
            return
        self._laikmatis.stop()
        if self._grojimo_mygtukas is not None:
            self._grojimo_mygtukas.setText(self._grojimo_tekstas)
        self._grojimo_mygtukas = None
        if self._thread is None or not self._ar_dirba(self._thread):
            self.daryti.setEnabled(True)
        if self._grojimo_klaida:
            klaida, self._grojimo_klaida = self._grojimo_klaida, ''
            QMessageBox.warning(self, PAVADINIMAS, 'Nepavyko paleisti garso.\n\n' + klaida)

    @staticmethod
    def _ar_dirba(gija):
        try:
            return gija.isRunning()
        except RuntimeError:
            return False

    def closeEvent(self, ivykis):
        self._stabdyk_groti()
        if self._thread is not None and self._ar_dirba(self._thread):
            self._worker.stop()
            self._thread.quit()
            self._thread.wait(5000)
        if self._pthread is not None and self._ar_dirba(self._pthread):
            self._pthread.quit()
            self._pthread.wait(5000)
        self._issaugok_nustatymus()
        super().closeEvent(ivykis)


# Paketo egzaminas (PASAS „Laukia" 3e): tas pats kelias, kuriuo žmogus daro mp3, abiem balsais,
# su sunkiomis vietomis — „15:25" (plėtiklis), „ORAI" (žodžių sąrašas iš PAKETO), ES/JAV
# (santrumpos), `---` (dalys). Paleidžiama `Skaitykle.exe --egzaminas <katalogas>`; mp3 po to
# klausosi mūsų ausys (lt_ausys) ir lyginama su šaltinių versija.
EGZAMINO_TEKSTAS = ('Laba diena, studentai. Paskaita prasidės 15:25 val.\n\n'
                    'ORAI šiandien geri, o ES ir JAV mokslininkai sutaria. '
                    'Per metus augalai sugeria 120 tonų anglies.\n---\n'
                    'Fotosintezė vyksta žaliuose lapuose.')


def egzaminas(katalogas):
    os.makedirs(katalogas, exist_ok=True)
    problemos = balsas.savitikra()
    eil = ['Skaitykle %s egzaminas' % VERSIJA, 'programa: %s' % CIA,
           'savitikra: %s' % ('GERAI' if not problemos else '; '.join(problemos)),
           'zodziu sarasas: %d' % len(balsas.skaiciu_pletiklis._ZODZIU_SARASAS or ()),
           'pletiklis: %s' % balsas.isplesk(EGZAMINO_TEKSTAS.replace('\n', ' '))]
    dalys = balsas.dalys(EGZAMINO_TEKSTAS)
    visi_gerai = not problemos
    for raktas in balsas.BALSAI:
        keliai = daliu_keliai(os.path.join(katalogas, 'egz_%s.mp3' % raktas), len(dalys))
        w = Darbininkas(raktas, 1.0, dalys, keliai, [0] * len(garsas.JUOSTOS),
                        garsas.GARSUMAS_NUMATYTAS, garsas.PAUZE_NUMATYTA, [])
        rez = []
        w.baigta.connect(lambda *a: rez.append(a))
        w.run()
        kaip, klaida, sek, failai = rez[0] if rez else ('klaida', 'nebaigta', 0.0, [])
        visi_gerai = visi_gerai and kaip == 'gerai'
        eil.append('%s: %s %s %.2f s %s' % (raktas, kaip, klaida, sek,
                                            [os.path.basename(f) for f in failai]))
    eil.append('REZULTATAS: %s' % ('GERAI' if visi_gerai else 'BLOGAI'))
    with open(os.path.join(katalogas, 'egzaminas.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(eil) + '\n')
    return 0 if visi_gerai else 1


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == '--egzaminas':
        app = QApplication(sys.argv)
        sys.exit(egzaminas(sys.argv[2]))
    app = QApplication(sys.argv)
    app.setApplicationName(PAVADINIMAS)
    if os.path.exists(IKONA):
        app.setWindowIcon(QIcon(IKONA))     # antraštės ikona pakete (PyInstaller IDI_ICON1 spąstas)
    langas = Langas()
    langas.show()
    problemos = balsas.savitikra()
    if problemos:
        langas._rodyk_busena('Programai trūksta dalių — įdiekite ją iš naujo.', RAUDONA)
        langas.daryti.setEnabled(False)
        QMessageBox.critical(langas, PAVADINIMAS,
                             'Programai trūksta dalių, todėl balsai neskambėtų taip, kaip turi:\n\n'
                             + '\n'.join(problemos) + '\n\nĮdiekite Skaityklę iš naujo.')
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
