# -*- coding: utf-8 -*-
"""TARIMO ŽODYNĖLIS: „rašoma → tariama" (2026-10-28).

Dėstytojo tekste — terminai, pavardės, svetimžodžiai, kurių balsas nežino. Kiti tą patį sprendžia
pakeitimų žodynu (Piper-Read `replace.dict`, Balabolka taisyklės). Čia — lentelė: kairėje kaip
parašyta, dešinėje kaip turi skambėti („Home Assistant" → „Hom Asistent" — taip Reginutė
skamba geriausiai, išbandyta 09-03). Šalia — perklausa, kad nereikėtų daryti viso mp3.

Langas pats negroja ir nesaugo — kaip dantratis: praneša `klausyti(tekstas)`, o saugo ir groja
pagrindinis langas.
"""
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QAbstractItemView, QDialog, QHBoxLayout, QHeaderView, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout)


class TarimoZodynas(QDialog):
    klausyti = pyqtSignal(str)

    def __init__(self, tevas, poros):
        super().__init__(tevas)
        self.setWindowTitle('Tarimo žodynėlis')
        self.setStyleSheet(tevas.styleSheet())
        self.resize(560, 420)

        antraste = QLabel('Tarimo žodynėlis')
        antraste.setObjectName('antraste')
        uzuomina = QLabel('Kairėje — kaip parašyta tekste, dešinėje — kaip turi skambėti, pvz. '
                          '„Home Assistant" → „Hom Asistent". Galioja ištisiems žodžiams, didžiosios '
                          'raidės nesvarbu. Pažymėkite eilutę ir spauskite ▸ — išgirsite, kaip skamba.')
        uzuomina.setObjectName('uzuomina')
        uzuomina.setWordWrap(True)

        self.lentele = QTableWidget(0, 2)
        self.lentele.setHorizontalHeaderLabels(['Rašoma', 'Tariama'])
        self.lentele.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.lentele.verticalHeader().setVisible(False)
        self.lentele.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        for rasoma, tariama in poros:
            self._prideti(rasoma, tariama)

        b_prideti = QPushButton('Pridėti')
        b_prideti.clicked.connect(self._nauja_eilute)
        b_salinti = QPushButton('Pašalinti')
        b_salinti.clicked.connect(self._salinti)
        self.b_klausyti = QPushButton('▸  Pasiklausyti')
        self.b_klausyti.setProperty('aktyvus', 'taip')
        self.b_klausyti.clicked.connect(self._klausyti)
        b_uzdaryti = QPushButton('Uždaryti')
        b_uzdaryti.clicked.connect(self.accept)
        for b in (b_prideti, b_salinti, self.b_klausyti, b_uzdaryti):
            b.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        mygtukai = QHBoxLayout()
        mygtukai.addWidget(b_prideti)
        mygtukai.addWidget(b_salinti)
        mygtukai.addWidget(self.b_klausyti)
        mygtukai.addStretch(1)
        mygtukai.addWidget(b_uzdaryti)

        visas = QVBoxLayout(self)
        visas.setContentsMargins(14, 12, 14, 12)
        visas.setSpacing(10)
        visas.addWidget(antraste)
        visas.addWidget(uzuomina)
        visas.addWidget(self.lentele, 1)
        visas.addLayout(mygtukai)

    def poros(self):
        """Užpildytos eilutės [[rašoma, tariama], ...] — tuščios praleidžiamos."""
        out = []
        for i in range(self.lentele.rowCount()):
            r = (self.lentele.item(i, 0).text() if self.lentele.item(i, 0) else '').strip()
            t = (self.lentele.item(i, 1).text() if self.lentele.item(i, 1) else '').strip()
            if r:
                out.append([r, t])
        return out

    def _prideti(self, rasoma='', tariama=''):
        i = self.lentele.rowCount()
        self.lentele.insertRow(i)
        self.lentele.setItem(i, 0, QTableWidgetItem(rasoma))
        self.lentele.setItem(i, 1, QTableWidgetItem(tariama))
        return i

    def _nauja_eilute(self):
        i = self._prideti()
        self.lentele.setCurrentCell(i, 0)
        self.lentele.editItem(self.lentele.item(i, 0))

    def _salinti(self):
        for i in sorted({x.row() for x in self.lentele.selectedIndexes()}, reverse=True):
            self.lentele.removeRow(i)

    def _klausyti(self):
        i = self.lentele.currentRow()
        if i < 0:
            return
        t = (self.lentele.item(i, 1).text() if self.lentele.item(i, 1) else '').strip()
        r = (self.lentele.item(i, 0).text() if self.lentele.item(i, 0) else '').strip()
        if t or r:
            # Tariama — jei įrašyta; kitaip parašyta, kad išgirstum, kaip skamba BE pataisos.
            self.klausyti.emit(t or r)
