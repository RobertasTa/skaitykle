# -*- coding: utf-8 -*-
"""BALSAS: Ingutė ir Reginutė, tekstas → mp3 (2026-10-28).

Paimta iš SpeakDream `vertejas\\balsas.py` + `lietuviskai\\`, ne parašyta iš naujo
(DOVANU_ZEMELAPIS 1 sk.). Skirtumai nuo SpeakDream — trys, visi dėl ILGŲ tekstų:

  * **Receptas (`ReginuteSynth`) taikomas ABIEM balsams.** SpeakDream Ingutė eina be jo, nes
    ten tekstai trumpi; namų kolonėlėje, kur tekstai ilgi, Ingutė eina SU juo ir tempu 1,15 —
    Roberto verdiktas: „puikiai, žinok, pasakoja" (`INGUTE balsas\\SKAITYK.md`). Receptas ne tik
    pauzės: jis skaido tekstą ties skyryba (VITS atmintis auga kvadratiškai), valo jį ir kerpa
    modelio tylą.
  * **Skaičių plėtiklis prijungtas.** SpeakDream jo nemato (09-19 radinys) — „15:25" ten skamba
    kaip tūkstančiai. Paskaitose skaičių ir datų pilna.
  * **Garsas rašomas į failą gabalais**, ne kaupiamas atmintyje: 10 val. knyga būtų 3 GB.

Balsų failai guli šalia (`balsai\\`), SHA256 sutampa su Piper katalogu (2026-10-28):
Reginutė `0417c4ef…986ee`, Ingutė `31bdf1df…41d8`. Konfigai — mūsų `espeak` kopijos, nes
piper-tts 1.8.0 `phoneme_type: lithuanian` dar nežino.
"""
import hashlib
import json
import os
import re

import numpy as np
from piper import PiperVoice

CIA = os.path.dirname(os.path.abspath(__file__))
LT = os.path.join(CIA, 'lietuviskai')

from lietuviskai import skaiciu_pletiklis
from lietuviskai.phonemize_lithuanian import LithuanianPhonemizer
from lietuviskai.skaiciu_pletiklis import isplesk
from lietuviskai.synth_reginute import ReginuteSynth

# ⛔ Programa ieško TIK savo kataloge (Roberto 10-28: „ieško savo programos kataloge, o ne pas
# mešką ieškotis kompe"). Vienintelis kietas kelias — `skaiciu_pletiklis._yra_tikras_zodis`:
# pirma `D:\_Balsas Lietuviksas\...` (pilnas leksikonas). Roberto kompe jis YRA, todėl
# pamirštas paketo sąrašas čia NESIMATYTŲ, o kitur „ORAI" būtų skaitomas raidėmis. Sąrašą
# įkeliam patys iš paketo — tada tas kelias niekada nevykdomas, ir elgesys VISUR vienodas.
ZODZIU_SARASAS = os.path.join(LT, 'zodziai_trumpi.txt')


def _ikelk_zodzius():
    with open(ZODZIU_SARASAS, encoding='utf-8') as f:
        skaiciu_pletiklis._ZODZIU_SARASAS = {e.split('\t', 1)[0].strip() for e in f if e.strip()}


try:
    _ikelk_zodzius()
except OSError:
    pass            # savitikra() tai praneš žmogui aiškiai — nekrentam importo metu

# Balsų failai = Piper katalogo failai (SHA256 sutikrinta 2026-10-28). Kitoks failas = kitas
# balsas arba sugadintas paketas — geriau aiški klaida, nei „balsas skamba blogai".
SHA256 = {
    'lt_LT-reginute1-medium.onnx': '0417c4ef351686ec0b0e7bf63426aefc72faea4a7693cfcb2f01ea8f6ee986ee',
    'lt_LT-ingute-medium.onnx': '31bdf1df5339e7da0e0f8c8e847e0f9e720bb732c0ffc7fb3d81970844b441d8',
}
BUTINI = (['balsai/' + f for f in SHA256] + ['balsai/%s.json' % f for f in SHA256]
          + ['balsai/LICENSE-VOICE-ingute', 'lietuviskai/lt_kirciai.tsv',
             'lietuviskai/lt_raides.tsv', 'lietuviskai/lt_kreipiniai.tsv',
             'lietuviskai/zodziai_trumpi.txt'])


def savitikra(su_sha=True):
    """Ar programa turi VISKĄ, ko reikia, kad balsai skambėtų taip, kaip išmatuota.
    Grąžina problemų sąrašą (tuščias — viskas gerai). Roberto reikalavimas 10-28: „kad
    nesigautų, jog kažkoks parametras ne taip įsikrovė, ir paskui verks, kad skamba blogai"."""
    problemos = []
    for f in BUTINI:
        if not os.path.isfile(os.path.join(CIA, *f.split('/'))):
            problemos.append('Trūksta failo: %s' % f)
    if problemos:
        return problemos
    for onnx, tikras in SHA256.items():
        k = json.load(open(os.path.join(CIA, 'balsai', onnx + '.json'), encoding='utf-8'))
        if k.get('phoneme_type') != 'espeak' or k.get('audio', {}).get('sample_rate') != 22050:
            problemos.append('Netinkami balso nustatymai: %s.json' % onnx)
        if su_sha:
            h = hashlib.sha256()
            with open(os.path.join(CIA, 'balsai', onnx), 'rb') as f:
                for gabalas in iter(lambda: f.read(1 << 20), b''):
                    h.update(gabalas)
            if h.hexdigest() != tikras:
                problemos.append('Balso failas pakeistas ar sugadintas: %s' % onnx)
    if len(skaiciu_pletiklis._ZODZIU_SARASAS or ()) < 30000:
        problemos.append('Žodžių sąrašas neįkeltas iš programos katalogo')
    if not skaiciu_pletiklis._yra_tikras_zodis('ORAI'):
        problemos.append('Didžiosiomis rašyti žodžiai būtų skaitomi raidėmis')
    return problemos

# raktas: (rodomas vardas, bazinis tempas `length_scale`, garsumo sulyginimas)
# Tempai: Reginutės receptas išmatuotas ant diktorės (1,30); Ingutės 1,15 — aklas pasirinkimas
# iš trijų (09-16). Sulyginimas — SpeakDream matavimas į LUFS medianą (09-18).
BALSAI = {
    'lt_LT-ingute-medium': ('Ingutė', 1.15, 1.05),
    'lt_LT-reginute1-medium': ('Reginutė', 1.30, 0.51),
}

# Langas ateičiai paruoštas kelioms kalboms (Robertas 10-28: „pirma versija tik lietuvių, bet
# GUI gali paruošti iš anksto"): kalba → jos balsai. Nauja kalba = nauja eilutė čia.
KALBOS = {'lt': ('Lietuvių', ['lt_LT-ingute-medium', 'lt_LT-reginute1-medium'])}

ILGIAUSIAS_GABALAS = 400    # simbolių be skyrybos ženklo, žr. `_apsauga_ilgiems`

_kesas = {}


def _ikrauk(raktas):
    """Modelis + fonemizatorius krauname vieną kartą (~2 s) ir laikom."""
    if raktas not in _kesas:
        voice = PiperVoice.load(os.path.join(CIA, 'balsai', raktas + '.onnx'),
                                os.path.join(CIA, 'balsai', raktas + '.onnx.json'))
        fonemos = LithuanianPhonemizer(
            dictionary_path=os.path.join(LT, 'lt_kirciai.tsv'),
            letters_path=os.path.join(LT, 'lt_raides.tsv'),
            vocatives_path=os.path.join(LT, 'lt_kreipiniai.tsv'),
            expand_text=None)       # plečia receptas — PRIEŠ skaidymą ties skyryba
        _kesas[raktas] = (voice, fonemos)
    return _kesas[raktas]


def skaityk_teksta(kelias):
    """txt failas → tekstas. Mokytojų failai būna trijų rūšių: UTF-8 (su BOM ar be),
    „Unicode" iš Notepad (UTF-16) ir senas Windows baltiškas cp1257."""
    with open(kelias, 'rb') as f:
        b = f.read()
    if b.startswith(b'\xff\xfe') or b.startswith(b'\xfe\xff'):
        return b.decode('utf-16')
    try:
        return b.decode('utf-8-sig')
    except UnicodeDecodeError:
        return b.decode('cp1257', errors='replace')


# Eilutė iš trijų ar daugiau brūkšnių („---") dalija tekstą į atskirus mp3 — dėstytojui po failą
# kiekvienai skaidrei (kokoro-tts-gui ir Balabolka skaido pagal žymą — ta pati idėja, 10-28).
SKIRTUKAS = re.compile(r'^[ \t]*-{3,}[ \t]*$', re.M)


def dalys(tekstas):
    """Tekstas → dalys pagal „---" eilutes. Tuščios praleidžiamos; be skirtuko — viena dalis."""
    return [d for d in SKIRTUKAS.split(tekstas or '') if d.strip()]


def taikyk_tarima(tekstas, zodynas):
    """Vartotojo tarimo žodynėlis „rašoma → tariama" (Piper-Read `replace.dict`, Balabolka
    taisyklės — 10-28 žvalgyba). Tik ištisi žodžiai, didžiosios raidės nesvarbu; ilgesni įrašai
    pirmi, kad „Home Assistant" nesuskiltų per „Home". Taikoma PRIEŠ plėtiklį."""
    poros = sorted(((str(r).strip(), str(t).strip()) for r, t in zodynas if str(r).strip()),
                   key=lambda p: -len(p[0]))
    for rasoma, tariama in poros:
        tekstas = re.sub(r'(?<!\w)' + re.escape(rasoma) + r'(?!\w)', lambda _m, t=tariama: t,
                         tekstas, flags=re.IGNORECASE)
    return tekstas


def pastraipos(tekstas):
    """Tekstas → pastraipos (eilutės, kurias balsas skaito su pauze tarp jų).

    Iš PDF nukopijuotas tekstas laužomas sakinio viduryje; tokia eilutė balse virstų pauze
    pusiau žodžio. Eilutės jungiamos TIK kai ankstesnė nesibaigia skyrybos ženklu IR kita
    prasideda mažąja raide — antraštė („Fotosintezė") taip lieka atskira.
    """
    eilutes = [e.strip() for e in tekstas.replace('\r\n', '\n').replace('\r', '\n').split('\n')]
    out = []
    for e in eilutes:
        if not e:
            continue
        if out and not re.search(r'[.!?:;…]$', out[-1]) and e[0].islower():
            out[-1] += ' ' + e
        else:
            out.append(e)
    return [_apsauga_ilgiems(p) for p in out]


def _apsauga_ilgiems(p):
    """Gabalas be . ! ? : ; virš ILGIAUSIAS_GABALAS simbolių pjaunamas kabliataškiu ties tarpu.

    Receptas skaido tik ties šiais ženklais; ilgas sąrašas be skyrybos nueitų į modelį viena
    seka, o VITS dėmesio atmintis auga kvadratiškai (kolonėlę 09-16 tai nuvertė). Kabliataškis
    duoda 0,2 s pauzę — geriau nei griūtis.
    """
    out = []
    for d in re.split(r'([.!?:;…])', p):
        while len(d) > ILGIAUSIAS_GABALAS:
            k = d.rfind(' ', 0, ILGIAUSIAS_GABALAS)
            if k <= 0:
                break
            out.append(d[:k] + ';')
            d = d[k:]
        out.append(d)
    return ''.join(out)


class Balsas:
    def __init__(self, raktas, greitis=1.0):
        """`greitis`: 1,0 — balso numatytasis tempas; mažiau — lėčiau, daugiau — greičiau
        (kaip SpeakDream slankiklis, 0,6–1,4)."""
        self.vardas, bazinis, self.stiprinimas = BALSAI[raktas]
        voice, fonemos = _ikrauk(raktas)
        self.sinteze = ReginuteSynth(voice, fonemos, length_scale=bazinis / max(0.3, greitis),
                                     expand_text=isplesk)
        self.daznis = self.sinteze.sr

    def pastraipa(self, pastraipa):
        """Visa pastraipa vienu masyvu BE uodegos tylos. Recepto pabaigos tyla (taškas 0,45 +
        eilutė 0,15 + pabaiga 0,7 s) yra grynas nulis, todėl nukerpama tiksliai; pauzę tarp
        pastraipų deda kviečiantysis — vartotojo nustatymas sekundėmis."""
        dalys = [a for a in self.gabalai(pastraipa) if a.size]
        if not dalys:
            return np.zeros(0, dtype='float32')
        return np.trim_zeros(np.concatenate(dalys), 'b')

    def gabalai(self, pastraipa):
        """Pastraipos garsas gabalais (float32), jau sulygintas ir be kirpimo."""
        for a in self.sinteze.gabalai(pastraipa):
            if self.stiprinimas != 1.0 and a.size:
                a = a * self.stiprinimas
                pikas = float(np.max(np.abs(a)))
                if pikas > 0.95:
                    a = a * (0.95 / pikas)
            yield a.astype('float32')
