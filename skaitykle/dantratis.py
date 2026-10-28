# -*- coding: utf-8 -*-
"""DANTRATIS (⚙): ekvalaizeris, garsumas, pauzė tarp pastraipų (2026-10-28).

Roberto: „daugiau tų slankiklių, tegu vartotojas renkasi, kaip susiderint, ir šalia —
mygtukas pasiklausyti, ką prisiderino". Slankikliai keičia garsą IŠ KARTO, net grojant —
taip derina muzikantai: klausaisi ir suki.

Langas pats garso negroja ir nieko nesaugo: jis tik praneša apie pokyčius (`pakeista`) ir
paprašo perklausos (`klausyti`) — groja ir saugo pagrindinis langas, kad grojimo kelias būtų
vienas (SpeakDream pamoka: du tiesos šaltiniai tam pačiam = defektas).
"""
from functools import partial

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QDialog, QGridLayout, QHBoxLayout, QLabel, QPushButton, QSlider,
                             QVBoxLayout)

import garsas


class GarsoNustatymai(QDialog):
    pakeista = pyqtSignal()
    klausyti = pyqtSignal()

    def __init__(self, tevas, eq, garsumas, pauze):
        super().__init__(tevas)
        self.setWindowTitle('Garso nustatymai')
        self.setStyleSheet(tevas.styleSheet())

        antraste = QLabel('Ekvalaizeris')
        antraste.setObjectName('antraste')
        uzuomina = QLabel('Spauskite „Pasiklausyti" ir judinkite slankiklius — garsas keičiasi '
                          'iš karto. Užveskite pelę ant juostos vardo — pamatysite, už ką ji atsakinga.')
        uzuomina.setObjectName('uzuomina')
        uzuomina.setWordWrap(True)

        tinklas = QGridLayout()
        tinklas.setHorizontalSpacing(14)
        tinklas.setVerticalSpacing(4)
        self.juostos = []
        self._reiksmes = []
        for i, (daznis, vardas, aprasas) in enumerate(garsas.JUOSTOS):
            reiksme = QLabel()
            reiksme.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            s = QSlider(Qt.Orientation.Vertical)
            s.setObjectName('eq')
            s.setRange(-garsas.EQ_RIBA, garsas.EQ_RIBA)
            s.setPageStep(3)
            s.setMinimumHeight(150)
            s.setValue(int(eq[i]) if i < len(eq) else 0)
            s.setToolTip(aprasas)
            s.valueChanged.connect(partial(self._juosta_pakeista, i))
            hz = QLabel(('%d Hz' % daznis) if daznis < 1000 else ('%d kHz' % (daznis // 1000)))
            hz.setObjectName('uzuomina')
            hz.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            pav = QLabel(vardas)
            pav.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            pav.setToolTip(aprasas)
            tinklas.addWidget(reiksme, 0, i)
            tinklas.addWidget(s, 1, i, Qt.AlignmentFlag.AlignHCenter)
            tinklas.addWidget(hz, 2, i)
            tinklas.addWidget(pav, 3, i)
            self.juostos.append(s)
            self._reiksmes.append(reiksme)
            self._rodyk_db(reiksme, s.value())

        self.garsumas = QSlider(Qt.Orientation.Horizontal)
        self.garsumas.setRange(-12, 12)
        self.garsumas.setValue(int(garsumas))
        self.garsumas.setToolTip('Viso įrašo garsumas. Garsiausios vietos apsaugotos nuo traškėjimo.')
        self.garsumo_zyme = QLabel()
        self.garsumo_zyme.setMinimumWidth(48)
        self.garsumas.valueChanged.connect(self._garsumas_pakeistas)
        self._rodyk_db(self.garsumo_zyme, self.garsumas.value())

        # Sekundėmis, kas 0,1 s (Roberto: „sekundėmis — lengviau ir tiksliau, nei trim punktais").
        # Slankiklis, ne skaičių laukas — kaip SpeakDream „Pauzė: 1,0 s"; rodyklėmis — po 0,1 s.
        self.pauze = QSlider(Qt.Orientation.Horizontal)
        self.pauze.setRange(0, 50)
        self.pauze.setPageStep(5)
        self.pauze.setValue(int(round(float(pauze) * 10)))
        self.pauze.setToolTip('Tyla tarp pastraipų. Skaidrėms dažnai patogu ilgesnė.')
        self.pauzes_zyme = QLabel()
        self.pauze.valueChanged.connect(self._pauze_pakeista)
        self._rodyk_pauze()

        kiti = QGridLayout()
        kiti.setHorizontalSpacing(10)
        kiti.addWidget(QLabel('Garsumas'), 0, 0)
        kiti.addWidget(self.garsumas, 0, 1)
        kiti.addWidget(self.garsumo_zyme, 0, 2)
        kiti.addWidget(QLabel('Pauzė tarp pastraipų'), 1, 0)
        kiti.addWidget(self.pauze, 1, 1)
        kiti.addWidget(self.pauzes_zyme, 1, 2)
        kiti.setColumnStretch(1, 1)

        self.b_klausyti = QPushButton('▶  Pasiklausyti')
        self.b_klausyti.setProperty('aktyvus', 'taip')
        self.b_klausyti.clicked.connect(self.klausyti.emit)
        b_atstatyti = QPushButton('Atstatyti')
        b_atstatyti.setToolTip('Ekvalaizeris lygus, garsumas +%d dB, pauzė %.1f s'
                               % (garsas.GARSUMAS_NUMATYTAS, garsas.PAUZE_NUMATYTA))
        b_atstatyti.clicked.connect(self._atstatyk)
        b_uzdaryti = QPushButton('Uždaryti')
        b_uzdaryti.clicked.connect(self.accept)
        for b in (self.b_klausyti, b_atstatyti, b_uzdaryti):
            b.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        mygtukai = QHBoxLayout()
        mygtukai.addWidget(self.b_klausyti)
        mygtukai.addWidget(b_atstatyti)
        mygtukai.addStretch(1)
        mygtukai.addWidget(b_uzdaryti)

        visas = QVBoxLayout(self)
        visas.setContentsMargins(14, 12, 14, 12)
        visas.setSpacing(10)
        visas.addWidget(antraste)
        visas.addWidget(uzuomina)
        visas.addLayout(tinklas)
        visas.addSpacing(4)
        visas.addLayout(kiti)
        visas.addLayout(mygtukai)

    # ---- reikšmės pagrindiniam langui ---------------------------------------------------
    def eq(self):
        return [s.value() for s in self.juostos]

    def garsumo_db(self):
        return self.garsumas.value()

    def pauzes_s(self):
        return self.pauze.value() / 10.0

    def rodyk_grojima(self, groja):
        self.b_klausyti.setText('■  Sustabdyti' if groja else '▶  Pasiklausyti')

    # ---- vidus --------------------------------------------------------------------------
    @staticmethod
    def _rodyk_db(zyme, v):
        zyme.setText(('%+d dB' % v) if v else '0 dB')

    def _juosta_pakeista(self, i, v):
        self._rodyk_db(self._reiksmes[i], v)
        self.pakeista.emit()

    def _garsumas_pakeistas(self, v):
        self._rodyk_db(self.garsumo_zyme, v)
        self.pakeista.emit()

    def _rodyk_pauze(self):
        self.pauzes_zyme.setText(('%.1f s' % self.pauzes_s()).replace('.', ','))

    def _pauze_pakeista(self, _v):
        self._rodyk_pauze()
        self.pakeista.emit()

    def _atstatyk(self):
        for s in self.juostos:
            s.setValue(0)
        self.garsumas.setValue(garsas.GARSUMAS_NUMATYTAS)
        self.pauze.setValue(int(round(garsas.PAUZE_NUMATYTA * 10)))
