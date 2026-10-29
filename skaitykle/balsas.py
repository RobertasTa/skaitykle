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

NUO 0.2 (2026-10-29) — keturios kalbos: LT, RU, EN, DE. Balsų `.onnx` parsisiunčiami pagal poreikį
(`balsu_siuntimas.py`), o konfigai, tempai ir garsumo sulyginimas lieka čia. Rusų, anglų ir
vokiečių tekstą balsas taria per Piper `espeak` kelią (skaičius skaito pats espeak); lietuvių
receptas, kirčiai ir plėtiklis — tik lietuviams.
"""
import json
import os
import re

import numpy as np
from piper import PiperVoice, SynthesisConfig

CIA = os.path.dirname(os.path.abspath(__file__))
LT = os.path.join(CIA, 'lietuviskai')

import balsu_siuntimas
import kalba as K
from lietuviskai import skaiciu_pletiklis
from lietuviskai.phonemize_lithuanian import LithuanianPhonemizer
from lietuviskai.skaiciu_pletiklis import isplesk
from lietuviskai.synth_reginute import ReginuteSynth, nukirpk_tyla

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

# raktas: (rodomas vardas, kalba, bazinis tempas `length_scale`, garsumo sulyginimas)
# Tempai: Reginutės receptas išmatuotas ant diktorės (1,30); Ingutės 1,15 — aklas pasirinkimas
# iš trijų (09-16); kitų — Piper numatytasis 1,0. Sulyginimas — į visų balsų LUFS medianą
# (−24,35, SpeakDream 09-18); naujieji keturi pamatuoti 10-29 tuo pačiu būdu ant vieno paskaitos
# teksto (`balsu_perklausa.py` scratchpad'e). Lessac ir Ruslano NĖRA dėl licencijų (PASAS 11).
BALSAI = {
    'lt_LT-ingute-medium': ('Ingutė', 'lt', 1.15, 1.05),
    'lt_LT-reginute1-medium': ('Reginutė', 'lt', 1.30, 0.51),
    'ru_RU-dmitri-medium': ('Dmitri', 'ru', 1.0, 0.91),     # Roberto pasirinkimas 10-29 (ne Denis)
    'en_GB-cori-medium': ('Cori', 'en', 1.0, 1.31),
    'de_DE-thorsten-medium': ('Thorsten', 'de', 1.0, 0.98),
}

# „HA" (Home Assistant) Reginutė sakydavo kaip varna — „KAAA" (Roberto ausis 10-29). Kaltas ne [h], o
# DVIEJŲ VIENODŲ BALSIŲ sandūra raidžių vardų virtinėje: „ha" + „a" modelis sulieja į vieną
# girgždantį „aaa". Pamatuota lt_ausys, po 8 kartus: dabar „ha" girdi 1/8 („cha" 4, „ką" 2);
# [h]→[ɣ] 0/8 („ką" 7); raidės atskirai („ha - a", recepto 0,1 s pauzė) — 6/8 (+„hha a" 1).
# Ingutė „HA A" taria gerai — jai nekeičiam. Kitos santrumpos (ES, LRT…) — kaip buvo.
ATSKIRTI_VIENODUS_BALSIUS = {'lt_LT-reginute1-medium'}
_RAIDZIU_VARDAI = sorted(set(skaiciu_pletiklis.RAIDZIU_VARDAI.values()), key=len, reverse=True)
_BALSES = 'aąeęėiįyouųū'


def atskirk_vienodus_balsius(tekstas):
    """Plėtiklio raidžių santrumpose („ - ha a - ") tarp dviejų raidžių vardų, kai pirmas
    baigiasi, o antras prasideda TUO PAČIU balsiu, įterpia „ - " (recepte — 0,1 s pauzė).
    Liečia tik tarpus, kurie VISI sudaryti iš raidžių vardų; paprastas tekstas su brūkšniais
    lieka nepaliestas."""
    def raides(m):
        likutis, vardai = m.group(1).strip(), []
        while likutis:
            v = next((v for v in _RAIDZIU_VARDAI
                      if likutis == v or likutis.startswith(v + ' ')), None)
            if v is None:
                return m.group(0)
            vardai.append(v)
            likutis = likutis[len(v):].strip()
        out = vardai[:1]
        for a, b in zip(vardai, vardai[1:]):
            if a[-1] in _BALSES and b[0] == a[-1]:
                out.append('-')
            out.append(b)
        return ' - %s - ' % ' '.join(out)
    return re.sub(r' - ([^-]+?) - ', raides, ' %s ' % tekstas)[1:-1]


# Kalba → (vardas SAVO kalba, jos balsai). Paketas = visi kalbos balsai, siunčiami kartu.
KALBOS = {
    'lt': ('Lietuvių', ['lt_LT-ingute-medium', 'lt_LT-reginute1-medium']),
    'ru': ('Русский', ['ru_RU-dmitri-medium']),
    'en': ('English', ['en_GB-cori-medium']),
    'de': ('Deutsch', ['de_DE-thorsten-medium']),
}

# Programos viduje turi būti VISŲ balsų konfigai (net neparsiųstų — kad parsiuntus nieko nereikėtų
# atspėti) ir lietuviški žodynai. Patys `.onnx` čia netikrinami: jų gali nebūti, o maiša
# tikrinama kraunant balsą (`balsu_siuntimas.patikrintas_kelias`).
BUTINI = (['balsai/%s.onnx.json' % r for r in BALSAI]
          + ['balsai/LICENSE-VOICE-ingute', 'lietuviskai/lt_kirciai.tsv',
             'lietuviskai/lt_raides.tsv', 'lietuviskai/lt_kreipiniai.tsv',
             'lietuviskai/zodziai_trumpi.txt'])


def savitikra():
    """Ar programa turi VISKĄ, ko reikia, kad balsai skambėtų taip, kaip išmatuota.
    Grąžina problemų sąrašą (tuščias — viskas gerai). Roberto reikalavimas 10-28: „kad
    nesigautų, jog kažkoks parametras ne taip įsikrovė, ir paskui verks, kad skamba blogai"."""
    problemos = []
    for f in BUTINI:
        if not os.path.isfile(os.path.join(CIA, *f.split('/'))):
            problemos.append(K.t('Trūksta failo: %s') % f)
    if problemos:
        return problemos
    for raktas in BALSAI:
        k = json.load(open(os.path.join(CIA, 'balsai', raktas + '.onnx.json'), encoding='utf-8'))
        if k.get('phoneme_type') != 'espeak' or k.get('audio', {}).get('sample_rate') != 22050:
            problemos.append(K.t('Netinkami balso nustatymai: %s') % (raktas + '.onnx.json'))
    if len(skaiciu_pletiklis._ZODZIU_SARASAS or ()) < 30000:
        problemos.append(K.t('Žodžių sąrašas neįkeltas iš programos katalogo'))
    if not skaiciu_pletiklis._yra_tikras_zodis('ORAI'):
        problemos.append(K.t('Didžiosiomis rašyti žodžiai būtų skaitomi raidėmis'))
    return problemos


def kalbos_mb(kalba):
    """Kiek megabaitų sveria kalbos paketas (žmogui, apvalinta į didesnę pusę)."""
    return -(-sum(balsu_siuntimas.FAILAI[r][2] for r in KALBOS[kalba][1]) // 1000000)


def kalba_yra(kalba):
    """Ar visi kalbos balsai parsiųsti (dydžio patikra — pigi; maiša — kraunant)."""
    return all(balsu_siuntimas.yra(r) for r in KALBOS[kalba][1])


class BalsoNera(Exception):
    """Balsas neparsiųstas arba jo failas sugadintas — žinutė jau išversta žmogui."""


ILGIAUSIAS_GABALAS = 400    # simbolių be skyrybos ženklo, žr. `_apsauga_ilgiems`

_kesas = {}


def _ikrauk(raktas):
    """Modelis (+ lietuviams fonemizatorius) krauname vieną kartą (~2 s) ir laikom."""
    if raktas not in _kesas:
        vardas = BALSAI[raktas][0]
        if not balsu_siuntimas.yra(raktas):
            raise BalsoNera(K.t('Balsas „%s" dar neparsisiųstas. Parsisiųskite jį: ⚙ → '
                              'Kalbos ir balsai.') % vardas)
        kelias = balsu_siuntimas.patikrintas_kelias(raktas)
        if kelias is None:
            # Sugadintą PARSIŲSTĄ failą ištrinam — kitaip jo dydis tinka, ir ⚙ rodytų
            # „parsisiųsta" be mygtuko iš naujo. Programos kataloge esančio neliečiam.
            sugadintas = balsu_siuntimas.kelias(raktas)
            if sugadintas and os.path.dirname(sugadintas) == balsu_siuntimas.KATALOGAS:
                try:
                    os.remove(sugadintas)
                except OSError:
                    pass
            raise BalsoNera(K.t('Balso „%s" failas sugadintas. Parsisiųskite jį iš naujo: ⚙ → '
                              'Kalbos ir balsai.') % vardas)
        voice = PiperVoice.load(kelias, os.path.join(CIA, 'balsai', raktas + '.onnx.json'))
        fonemos = None
        if BALSAI[raktas][1] == 'lt':
            fonemos = LithuanianPhonemizer(
                dictionary_path=os.path.join(LT, 'lt_kirciai.tsv'),
                letters_path=os.path.join(LT, 'lt_raides.tsv'),
                vocatives_path=os.path.join(LT, 'lt_kreipiniai.tsv'),
                expand_text=None)       # plečia receptas — PRIEŠ skaidymą ties skyryba
        _kesas[raktas] = (voice, fonemos)
    return _kesas[raktas]


# Senų txt failų koduotė pagal kalbą: Windows „ANSI" lietuviams cp1257, rusams cp1251,
# vokiečiams ir anglams cp1252. UTF-8 ir UTF-16 atpažįstami visada.
SENA_KODUOTE = {'lt': 'cp1257', 'ru': 'cp1251', 'en': 'cp1252', 'de': 'cp1252'}


def skaityk_teksta(kelias, kalba='lt'):
    """txt failas → tekstas. Mokytojų failai būna trijų rūšių: UTF-8 (su BOM ar be),
    „Unicode" iš Notepad (UTF-16) ir senas Windows „ANSI" (cp1257 baltiškas ir t. t.)."""
    with open(kelias, 'rb') as f:
        b = f.read()
    if b.startswith(b'\xff\xfe') or b.startswith(b'\xfe\xff'):
        return b.decode('utf-16')
    try:
        return b.decode('utf-8-sig')
    except UnicodeDecodeError:
        return b.decode(SENA_KODUOTE.get(kalba, 'cp1257'), errors='replace')


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


class PiperSakiniais:
    """Rusų, anglų, vokiečių balsai: Piper `espeak` kelias, bet su TOMIS PAČIOMIS pauzėmis kaip
    lietuvių recepte (taškas 0,45 s ir t. t.). Pamatuota 10-29: Piper sakinius skaido pats, o tarp
    jų palieka tik 0,15–0,35 s modelio tylos — paskaitai per tankiai, ir kiekvienam sakiniui vis
    kitaip. Todėl tyla nukerpama tuo pačiu `nukirpk_tyla` ir dedama sava, vienoda.

    Ilga pastraipa pirma pjaunama ties sakinio galu į ≤ RIBA simbolių gabalus — VITS dėmesio
    atmintis auga kvadratiškai (SpeakDream `_dalyk`, kolonėlės 09-16 pamoka)."""
    RIBA = 250
    PAUZE = {'.': 0.45, '!': 0.45, '?': 0.45, '…': 0.45, ':': 0.20, ';': 0.20}

    def __init__(self, voice, length_scale):
        self.voice = voice
        self.sr = voice.config.sample_rate
        self.syn = SynthesisConfig(length_scale=length_scale, noise_scale=0.667,
                                   noise_w_scale=0.8, normalize_audio=False)

    def _tyla(self, s):
        return np.zeros(int(self.sr * s), dtype=np.float32)

    def _gabalai_tekstui(self, pastraipa):
        dalys, dabar = [], ''
        for s in [x for x in re.split(r'(?<=[.!?…;:])\s+', pastraipa.strip()) if x.strip()]:
            if dabar and len(dabar) + 1 + len(s) > self.RIBA:
                dalys.append(dabar)
                dabar = s
            else:
                dabar = ('%s %s' % (dabar, s)).strip()
        if dabar:
            dalys.append(dabar)
        return dalys

    def gabalai(self, pastraipa):
        for tekstas in self._gabalai_tekstui(pastraipa):
            for c in self.voice.synthesize(tekstas, self.syn):
                a = np.frombuffer(c.audio_int16_bytes, dtype='int16').astype(np.float32) / 32768.0
                a = nukirpk_tyla(a, self.sr)
                if not a.size:
                    continue
                yield a
                # AudioChunk teksto neturi, bet jo fonemos baigiasi tuo pačiu skyrybos ženklu
                # („prʲidɭʌʒˈɛnʲijɪ." — pamatuota 10-29).
                galas = ''.join(c.phonemes or []).rstrip()[-1:]
                yield self._tyla(self.PAUZE.get(galas, 0.25))
        yield self._tyla(0.7)


class Balsas:
    def __init__(self, raktas, greitis=1.0):
        """`greitis`: 1,0 — balso numatytasis tempas; mažiau — lėčiau, daugiau — greičiau
        (kaip SpeakDream slankiklis, 0,6–1,4)."""
        self.vardas, self.kalba, bazinis, self.stiprinimas = BALSAI[raktas]
        voice, fonemos = _ikrauk(raktas)
        if self.kalba == 'lt':
            self.sinteze = ReginuteSynth(voice, fonemos,
                                         length_scale=bazinis / max(0.3, greitis),
                                         expand_text=(
                                             (lambda t: atskirk_vienodus_balsius(isplesk(t)))
                                             if raktas in ATSKIRTI_VIENODUS_BALSIUS else isplesk))
        else:
            self.sinteze = PiperSakiniais(voice, bazinis / max(0.3, greitis))
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
