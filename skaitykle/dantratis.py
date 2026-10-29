# -*- coding: utf-8 -*-
"""DANTRATIS (⚙): ekvalaizeris, garsumas, pauzė tarp pastraipų (2026-10-28).

Roberto: „daugiau tų slankiklių, tegu vartotojas renkasi, kaip susiderint, ir šalia —
mygtukas pasiklausyti, ką prisiderino". Slankikliai keičia garsą IŠ KARTO, net grojant —
taip derina muzikantai: klausaisi ir suki.

Langas pats garso negroja ir nieko nesaugo: jis tik praneša apie pokyčius (`pakeista`) ir
paprašo perklausos (`klausyti`) — groja ir saugo pagrindinis langas, kad grojimo kelias būtų
vienas (SpeakDream pamoka: du tiesos šaltiniai tam pačiam = defektas).

Greitis čia — ANTRAS to paties slankiklio vaizdas (Roberto 10-28: „derinant patogu ir greitį
nusistatyti"). Tiesa viena — pagrindinio lango slankiklis: šis tik praneša `greitis_pakeistas`, o
pagrindinis langas grąžina reikšmę per `nustatyk_greiti` (be signalo — kad nesusisuktų ratu).
Greitis keičia patį balso darymą, ne paruoštą garsą, todėl grojant pavyzdys persidaro (main.py).

NUO 0.2 (2026-10-29) — skyrius „Kalbos ir balsai" (Roberto: „per dantratį padaryk, kad
parsisiųsti būtų galima paketą reikiamą"). Siunčiama fone (`Siuntejas`, QThread), vienas paketas
vienu metu, kiti laukia eilėje. Kol siunčiama, langas neužsidaro be klausimo — kitaip žmogus
nežinotų, ar balsas atėjo.
"""
import threading
from functools import partial

from PyQt6.QtCore import QObject, QThread, Qt, pyqtSignal
from PyQt6.QtWidgets import (QDialog, QGridLayout, QHBoxLayout, QLabel, QMessageBox,
                             QProgressBar, QPushButton, QSlider, QVBoxLayout)

import balsas
import balsu_siuntimas
import garsas
import kalba as K


class Siuntejas(QObject):
    """Vienos kalbos balsai — iš eilės, fone. GUI neliečia: tik signalai (guard)."""
    progresas = pyqtSignal(int, int)        # gauta MB, iš viso MB (int — kad tilptų Qt int)
    baigta = pyqtSignal(str, str)           # kalba, klaida ('' — gerai, '-' — atšaukta)

    def __init__(self, kalba):
        super().__init__()
        self.kalba = kalba
        self.stabdyk = threading.Event()

    def run(self):
        raktai = [r for r in balsas.KALBOS[self.kalba][1] if not balsu_siuntimas.yra(r)]
        viso = sum(balsu_siuntimas.FAILAI[r][2] for r in raktai) or 1
        jau = 0
        try:
            for r in raktai:
                ankstesni = jau
                kelias = balsu_siuntimas.parsisiusk(
                    r, lambda g, _v, a=ankstesni: self.progresas.emit((a + g) >> 20, viso >> 20),
                    self.stabdyk)
                if kelias is None:
                    self.baigta.emit(self.kalba, '-')
                    return
                jau += balsu_siuntimas.FAILAI[r][2]
            self.baigta.emit(self.kalba, '')
        except Exception as e:
            self.baigta.emit(self.kalba, str(e) or type(e).__name__)


class GarsoNustatymai(QDialog):
    pakeista = pyqtSignal()
    klausyti = pyqtSignal()
    greitis_pakeistas = pyqtSignal(int)
    balsai_pasikeite = pyqtSignal()

    def __init__(self, tevas, eq, garsumas, pauze, greitis=100):
        super().__init__(tevas)
        self.setWindowTitle(K.t('Nustatymai'))
        self.setStyleSheet(tevas.styleSheet())
        self._thread = None
        self._worker = None
        self._eile = []                 # kalbos, laukiančios siuntimo

        antraste = QLabel(K.t('Ekvalaizeris'))
        antraste.setObjectName('antraste')
        uzuomina = QLabel(K.t('Spauskite „Pasiklausyti" ir judinkite slankiklius — garsas keičiasi '
                              'iš karto. Užveskite pelę ant juostos vardo — pamatysite, už ką ji '
                              'atsakinga.'))
        uzuomina.setObjectName('uzuomina')
        uzuomina.setWordWrap(True)

        tinklas = QGridLayout()
        tinklas.setHorizontalSpacing(14)
        tinklas.setVerticalSpacing(4)
        self.juostos = []
        self._reiksmes = []
        for i, (daznis, vardas, aprasas) in enumerate(garsas.JUOSTOS):
            vardas, aprasas = K.t(vardas), K.t(aprasas)
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
        self.garsumas.setToolTip(K.t('Viso įrašo garsumas. Garsiausios vietos apsaugotos nuo '
                                     'traškėjimo.'))
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
        self.pauze.setToolTip(K.t('Tyla tarp pastraipų. Skaidrėms dažnai patogu ilgesnė.'))
        self.pauzes_zyme = QLabel()
        self.pauze.valueChanged.connect(self._pauze_pakeista)
        self._rodyk_pauze()

        # Tas pats diapazonas kaip pagrindiniame lange (60–140 = 0,60–1,40×).
        self.greitis = QSlider(Qt.Orientation.Horizontal)
        self.greitis.setRange(60, 140)
        self.greitis.setSingleStep(5)
        self.greitis.setPageStep(10)
        self.greitis.setValue(int(greitis))
        self.greitis.setToolTip(K.t('Kalbėjimo greitis — tas pats, kas pagrindiniame lange. '
                                    'Grojant pavyzdys persidaro nauju greičiu.'))
        self.greicio_zyme = QLabel()
        self.greitis.valueChanged.connect(self._greitis_judintas)
        self._rodyk_greiti()
        b_numatytas = QPushButton('↺')
        b_numatytas.setObjectName('ikona')
        b_numatytas.setToolTip(K.t('Balso numatytasis greitis (1,00×)'))
        b_numatytas.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        b_numatytas.clicked.connect(lambda: self.greitis.setValue(100))

        kiti = QGridLayout()
        kiti.setHorizontalSpacing(10)
        kiti.addWidget(QLabel(K.t('Greitis')), 0, 0)
        kiti.addWidget(self.greitis, 0, 1)
        kiti.addWidget(self.greicio_zyme, 0, 2)
        kiti.addWidget(b_numatytas, 0, 3)
        kiti.addWidget(QLabel(K.t('Garsumas')), 1, 0)
        kiti.addWidget(self.garsumas, 1, 1)
        kiti.addWidget(self.garsumo_zyme, 1, 2)
        kiti.addWidget(QLabel(K.t('Pauzė tarp pastraipų')), 2, 0)
        kiti.addWidget(self.pauze, 2, 1)
        kiti.addWidget(self.pauzes_zyme, 2, 2)
        kiti.setColumnStretch(1, 1)

        self.b_klausyti = QPushButton(K.t('▶  Pasiklausyti'))
        self.b_klausyti.setProperty('aktyvus', 'taip')
        self.b_klausyti.clicked.connect(self.klausyti.emit)
        b_atstatyti = QPushButton(K.t('Atstatyti'))
        b_atstatyti.setToolTip(K.t('Ekvalaizeris lygus, garsumas +%d dB, pauzė %s s')
                               % (garsas.GARSUMAS_NUMATYTAS,
                                  K.skaicius(garsas.PAUZE_NUMATYTA, '%.1f')))
        b_atstatyti.clicked.connect(self._atstatyk)
        self.b_uzdaryti = QPushButton(K.t('Uždaryti'))
        self.b_uzdaryti.clicked.connect(self.accept)
        for b in (self.b_klausyti, b_atstatyti, self.b_uzdaryti):
            b.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        mygtukai = QHBoxLayout()
        mygtukai.addWidget(self.b_klausyti)
        mygtukai.addWidget(b_atstatyti)
        mygtukai.addStretch(1)
        mygtukai.addWidget(self.b_uzdaryti)

        visas = QVBoxLayout(self)
        visas.setContentsMargins(14, 12, 14, 12)
        visas.setSpacing(10)
        visas.addWidget(antraste)
        visas.addWidget(uzuomina)
        visas.addLayout(tinklas)
        visas.addSpacing(4)
        visas.addLayout(kiti)
        visas.addSpacing(6)
        visas.addLayout(self._kalbu_skyrius())
        visas.addLayout(mygtukai)
        self._rodyk_kalbas()            # tik dabar — visi mygtukai jau šio lango vaikai

    # ---- kalbos ir balsai ---------------------------------------------------------------
    def _kalbu_skyrius(self):
        """Kiekviena kalba — eilutė: vardas savo kalba, balsai, dydis, būsena arba mygtukas."""
        antraste = QLabel(K.t('Kalbos ir balsai'))
        antraste.setObjectName('antraste')
        uzuomina = QLabel(K.t('Kiekvienos kalbos balsai parsisiunčiami vieną kartą iš Piper balsų '
                              'katalogo (huggingface.co). Po to viskas veikia be interneto.'))
        uzuomina.setObjectName('uzuomina')
        uzuomina.setWordWrap(True)
        tinklas = QGridLayout()
        tinklas.setHorizontalSpacing(12)
        tinklas.setVerticalSpacing(6)
        self._kalbu_mygtukai = {}
        self._kalbu_busenos = {}
        for i, (kodas, (vardas, raktai)) in enumerate(balsas.KALBOS.items()):
            tinklas.addWidget(QLabel(vardas), i, 0)
            balsai = QLabel(', '.join(balsas.BALSAI[r][0] for r in raktai))
            balsai.setObjectName('uzuomina')
            tinklas.addWidget(balsai, i, 1)
            dydis = QLabel('%d MB' % balsas.kalbos_mb(kodas))
            dydis.setObjectName('uzuomina')
            tinklas.addWidget(dydis, i, 2, Qt.AlignmentFlag.AlignRight)
            busena = QLabel()
            b = QPushButton(K.t('Parsisiųsti'))
            b.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            b.clicked.connect(partial(self._kalbos_mygtukas, kodas))
            tinklas.addWidget(busena, i, 3)
            tinklas.addWidget(b, i, 4)
            self._kalbu_mygtukai[kodas] = b
            self._kalbu_busenos[kodas] = busena
        tinklas.setColumnStretch(1, 1)
        self.siuntimo_juosta = QProgressBar()
        self.siuntimo_juosta.setTextVisible(False)
        self.siuntimo_juosta.setRange(0, 1)
        self.siuntimo_juosta.setValue(0)
        self.siuntimo_zyme = QLabel()
        self.siuntimo_zyme.setObjectName('uzuomina')
        self.siuntimo_zyme.setWordWrap(True)
        lay = QVBoxLayout()
        lay.setSpacing(6)
        lay.addWidget(antraste)
        lay.addWidget(uzuomina)
        lay.addLayout(tinklas)
        lay.addWidget(self.siuntimo_juosta)
        lay.addWidget(self.siuntimo_zyme)
        # ⛔ `_rodyk_kalbas()` čia NEKVIEČIAM: mygtukai dar be tėvo, o `setVisible(True)` tėvo
        # neturinčiam valdikliui padaro jį ATSKIRU langu (pamatuota 10-29: aukštis 24 vietoj 31).
        return lay

    def siuncia(self):
        try:
            return self._thread is not None and self._thread.isRunning()
        except RuntimeError:
            return False

    def _rodyk_kalbas(self):
        siunciama = self._worker.kalba if self.siuncia() else None
        for kodas, b in self._kalbu_mygtukai.items():
            busena = self._kalbu_busenos[kodas]
            if kodas == siunciama:
                busena.setText('')
                b.setText(K.t('Atšaukti'))
                b.setVisible(True)
                b.setEnabled(True)
            elif balsas.kalba_yra(kodas):
                busena.setText('✓ ' + K.t('parsisiųsta'))
                b.setVisible(False)
            else:
                busena.setText(K.t('laukia eilėje') if kodas in self._eile else '')
                b.setText(K.t('Parsisiųsti'))
                b.setVisible(True)
                b.setEnabled(kodas not in self._eile)

    def siusk(self, kalbos):
        """Į eilę — kalbos, kurių balsų dar nėra (pirmas paleidimas, „Parsisiųsti…")."""
        for k in kalbos:
            if k in balsas.KALBOS and not balsas.kalba_yra(k) and k not in self._eile:
                self._eile.append(k)
        self._kitas()

    def _kalbos_mygtukas(self, kodas):
        if self.siuncia() and self._worker.kalba == kodas:
            self._worker.stabdyk.set()
            self.siuntimo_zyme.setText(K.t('Atšaukiama…'))
            return
        self.siusk([kodas])

    def _kitas(self):
        if self.siuncia() or not self._eile:
            self._rodyk_kalbas()
            return
        kodas = self._eile.pop(0)
        # Nuorodos ANT self ir niekur nenulinamos (pyqt6_threading_guard).
        self._worker = Siuntejas(kodas)
        self._thread = QThread()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progresas.connect(self._progresas)
        self._worker.baigta.connect(self._siuntimas_baigtas)
        self._worker.baigta.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.finished.connect(self._kitas)
        self.siuntimo_juosta.setRange(0, 0)
        self.siuntimo_zyme.setText(K.t('Jungiamasi prie Piper balsų katalogo…'))
        self._thread.start()
        self._rodyk_kalbas()

    def _progresas(self, gauta, viso):
        self.siuntimo_juosta.setRange(0, max(1, viso))
        self.siuntimo_juosta.setValue(gauta)
        self.siuntimo_zyme.setText(K.t('Siunčiama: %s — %d iš %d MB')
                                   % (balsas.KALBOS[self._worker.kalba][0], gauta, viso))

    def _siuntimas_baigtas(self, kodas, klaida):
        vardas = balsas.KALBOS[kodas][0]
        self.siuntimo_juosta.setRange(0, 1)
        if not klaida:
            self.siuntimo_juosta.setValue(1)
            self.siuntimo_zyme.setText(K.t('Parsisiųsta: %s. Balsai patikrinti (SHA256) ir '
                                           'paruošti.') % vardas)
        elif klaida == '-':
            self.siuntimo_juosta.setValue(0)
            self.siuntimo_zyme.setText(K.t('Atšaukta: %s. Pusiau parsiųstų failų nelieka.')
                                       % vardas)
        else:
            self.siuntimo_juosta.setValue(0)
            self.siuntimo_zyme.setText(K.t('Nepavyko parsisiųsti: %s.') % vardas)
            QMessageBox.warning(self, K.t('Kalbos ir balsai'),
                                K.t('Nepavyko parsisiųsti balsų: %s.\n\nPatikrinkite interneto '
                                    'ryšį ir bandykite dar kartą.\n\n(%s)') % (vardas, klaida))
        self.balsai_pasikeite.emit()
        self._rodyk_kalbas()

    def _ar_galima_uzdaryti(self):
        if not self.siuncia() and not self._eile:
            return True
        atsakymas = QMessageBox.question(
            self, K.t('Kalbos ir balsai'),
            K.t('Balsai dar siunčiami. Nutraukti siuntimą ir uždaryti langą?'))
        if atsakymas != QMessageBox.StandardButton.Yes:
            return False
        self.stabdyk_siuntima()
        return True

    def stabdyk_siuntima(self):
        """Atšaukia eilę ir einamąjį siuntimą; laukia, kol gija baigs (atšaukimas — per
        1 MB gabalą, užstrigus tinklui — iki `balsu_siuntimas.LAUKTI_S`)."""
        self._eile.clear()
        if self.siuncia():
            self._worker.stabdyk.set()
            self._thread.wait((balsu_siuntimas.LAUKTI_S + 5) * 1000)

    def showEvent(self, ivykis):
        # Pamatuota 10-29 (offscreen 800 px ekranas): dialogas atsidarė MINIMALIU aukščiu (654 vs
        # 684), ir kalbų eilučių mygtukai susispaudė iki 24 px — tekstas nukirstas. Su pilnu
        # aukščiu jie 31 px. Todėl pirmą kartą atidarant — ne žemiau, nei prašo pats langas.
        super().showEvent(ivykis)
        if self.height() < self.sizeHint().height():
            self.resize(self.width(), self.sizeHint().height())

    def accept(self):
        if self._ar_galima_uzdaryti():
            super().accept()

    def reject(self):
        if self._ar_galima_uzdaryti():
            super().reject()

    # ---- reikšmės pagrindiniam langui ---------------------------------------------------
    def eq(self):
        return [s.value() for s in self.juostos]

    def garsumo_db(self):
        return self.garsumas.value()

    def pauzes_s(self):
        return self.pauze.value() / 10.0

    def nustatyk_greiti(self, v):
        """Pagrindinis langas grąžina savo reikšmę — be signalo, kad nesusisuktų ratu."""
        self.greitis.blockSignals(True)
        self.greitis.setValue(int(v))
        self.greitis.blockSignals(False)
        self._rodyk_greiti()

    def _rodyk_greiti(self):
        self.greicio_zyme.setText(K.skaicius(self.greitis.value() / 100.0) + '×')

    def _greitis_judintas(self, v):
        self._rodyk_greiti()
        self.greitis_pakeistas.emit(v)

    def rodyk_grojima(self, groja):
        self.b_klausyti.setText(K.t('■  Sustabdyti') if groja else K.t('▶  Pasiklausyti'))

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
        self.pauzes_zyme.setText(K.skaicius(self.pauzes_s(), '%.1f') + ' s')

    def _pauze_pakeista(self, _v):
        self._rodyk_pauze()
        self.pakeista.emit()

    def _atstatyk(self):
        for s in self.juostos:
            s.setValue(0)
        self.garsumas.setValue(garsas.GARSUMAS_NUMATYTAS)
        self.pauze.setValue(int(round(garsas.PAUZE_NUMATYTA * 10)))
