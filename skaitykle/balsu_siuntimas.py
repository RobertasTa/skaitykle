# -*- coding: utf-8 -*-
"""BALSŲ SIUNTIMAS: kiekvienas kalbos paketas parsisiunčiamas tada, kai jo reikia (2026-10-29).

Roberto sprendimas 10-29: *„kažkam reikės tik lietuvių, kažkam tik rusų … per dantratį padaryk,
kad parsisiųsti būtų galima reikiamą paketą"* — kaip Diktuoklėje: instaliatoriuje varnelės, ko
pradžioje nepasiėmei — vėliau per ⚙.

Kas iš tinklo, o kas iš paketo (Roberto reikalavimas 10-28 — „kad niekas neįsikrautų ne taip iš
nežinojimo"):
  * iš tinklo ateina TIK balso svoriai (`.onnx`), tas pats failas, kurį platina Piper katalogas;
  * viskas kita — programos viduje: konfigai (`balsai\\*.onnx.json`), tempai ir garsumo
    sulyginimas (`balsas.BALSAI`), lietuviški žodynai;
  * kiekvieno failo SHA256 ir dydis įrašyti ČIA. Siunčiama į `<failas>.dalis`, maiša skaičiuojama
    siunčiant, ir tik sutapus failas pervadinamas. Nesutapo, nutrūko ar atšaukta — `.dalis`
    ištrinama; pusinio balso diske nelieka niekada.

Kodėl ne `huggingface_hub` (SpeakDream, Diktuoklė): kiekvienas balsas yra VIENAS failas su žinoma
maiša, o maišą tikrinti ir progresą rodyti reikia vis tiek. Paprastas HTTPS — be naujų bibliotekų
pakete ir be tqdm spąstų langinėje programoje (Diktuoklės 09-11 pamoka).

Kur guli: `%LOCALAPPDATA%\\Skaitykle\\balsai\\`; pašalinant programą instaliatorius jį ištrina
(balsus visada galima parsisiųsti iš naujo). Antroji vieta — programos `balsai\\` (paleidžiant iš
šaltinių ir po atnaujinimo iš 0.1.x, kurios balsus vežėsi pakete). `SKAITYKLE_BALSAI` aplinkos
kintamasis — patikroms (diagnostinis jungiklis, kad bandymas neliestų tikrų balsų).
"""
import hashlib
import os
import threading
import urllib.request

CIA = os.path.dirname(os.path.abspath(__file__))
PAKETO = os.path.join(CIA, 'balsai')
KATALOGAS = os.environ.get('SKAITYKLE_BALSAI') or os.path.join(
    os.environ.get('LOCALAPPDATA') or os.path.expanduser('~'), 'Skaitykle', 'balsai')

KATALOGO_URL = 'https://huggingface.co/rhasspy/piper-voices/resolve/main/'

# raktas: (kelias Piper kataloge, SHA256, baitai). Visi — HF API 2026-10-28/29, failai parsiųsti
# ir maišos sutikrintos (`sha256sum`) tą pačią dieną.
FAILAI = {
    'lt_LT-ingute-medium': (
        'lt/lt_LT/ingute/medium/lt_LT-ingute-medium.onnx',
        '31bdf1df5339e7da0e0f8c8e847e0f9e720bb732c0ffc7fb3d81970844b441d8', 63516051),
    'lt_LT-reginute1-medium': (
        'lt/lt_LT/reginute1/medium/lt_LT-reginute1-medium.onnx',
        '0417c4ef351686ec0b0e7bf63426aefc72faea4a7693cfcb2f01ea8f6ee986ee', 63516051),
    'ru_RU-dmitri-medium': (
        'ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx',
        'f073356ebc4bd0f80c5af58df2953a5988bd5bdab1eb38635ce960b071fbefcb', 63201294),
    'en_GB-cori-medium': (
        'en/en_GB/cori/medium/en_GB-cori-medium.onnx',
        '1899f98e5fb8310154f3c2973f4b8a929ba7245e722b3d3a85680b833d95f10d', 63531379),
    'de_DE-thorsten-medium': (
        'de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx',
        '7e64762d8e5118bb578f2eea6207e1a35a8e0c30595010b666f983fc87bb7819', 63201294),
}

GABALAS = 1 << 20           # 1 MB: atšaukimas sureaguoja per sekundės dalį
LAUKTI_S = 30               # kiek laukti tylinčio serverio, kol sakysim „nepavyko"

_patikrinti = {}            # kelias → (dydis, mtime), kurio SHA šiame procese jau sutapo
_uzraktas = threading.Lock()


class SiuntimoKlaida(Exception):
    pass


def _vietos(raktas):
    vardas = raktas + '.onnx'
    return [os.path.join(KATALOGAS, vardas), os.path.join(PAKETO, vardas)]


def kelias(raktas):
    """Balso failas, jei jis yra IR tinkamo dydžio; kitaip None. Pigu — tinka sąrašams."""
    dydis = FAILAI[raktas][2]
    for k in _vietos(raktas):
        try:
            if os.path.getsize(k) == dydis:
                return k
        except OSError:
            pass
    return None


def yra(raktas):
    return kelias(raktas) is not None


def sha256(kelias_):
    h = hashlib.sha256()
    with open(kelias_, 'rb') as f:
        for gabalas in iter(lambda: f.read(GABALAS), b''):
            h.update(gabalas)
    return h.hexdigest()


def patikrintas_kelias(raktas):
    """Kelias į balsą, kurio SHA256 sutampa su `FAILAI` (tikrinama kartą per procesą); None —
    balso nėra arba jis sugadintas."""
    k = kelias(raktas)
    if k is None:
        return None
    st = os.stat(k)
    zyme = (st.st_size, st.st_mtime_ns)
    with _uzraktas:
        if _patikrinti.get(k) == zyme:
            return k
    if sha256(k) != FAILAI[raktas][1]:
        return None
    with _uzraktas:
        _patikrinti[k] = zyme
    return k


def parsisiusk(raktas, pranesk=None, stabdyk=None):
    """Vienas balsas į `KATALOGAS`. `pranesk(gauta, viso)` — baitais; `stabdyk` — threading.Event.
    Grąžina kelią; atšaukus — None. Klaida — `SiuntimoKlaida` su žmogui suprantama priežastimi
    (tekstą verčia kviečiantysis — šis modulis Qt ir kalbų nežino)."""
    kelias_kataloge, tikra_sha, dydis = FAILAI[raktas]
    os.makedirs(KATALOGAS, exist_ok=True)
    galutinis = os.path.join(KATALOGAS, raktas + '.onnx')
    dalis = galutinis + '.dalis'
    h = hashlib.sha256()
    gauta = 0
    try:
        uzklausa = urllib.request.Request(KATALOGO_URL + kelias_kataloge,
                                          headers={'User-Agent': 'Skaitykle'})
        with urllib.request.urlopen(uzklausa, timeout=LAUKTI_S) as atsakymas, \
                open(dalis, 'wb') as f:
            while True:
                if stabdyk is not None and stabdyk.is_set():
                    break
                gabalas = atsakymas.read(GABALAS)
                if not gabalas:
                    break
                f.write(gabalas)
                h.update(gabalas)
                gauta += len(gabalas)
                if pranesk:
                    pranesk(gauta, dydis)
        if stabdyk is not None and stabdyk.is_set():
            return None
        if gauta != dydis:
            raise SiuntimoKlaida('dydis %d B, turi būti %d B' % (gauta, dydis))
        if h.hexdigest() != tikra_sha:
            raise SiuntimoKlaida('SHA256 nesutampa')
        os.replace(dalis, galutinis)
        with _uzraktas:
            st = os.stat(galutinis)
            _patikrinti[galutinis] = (st.st_size, st.st_mtime_ns)
        return galutinis
    except SiuntimoKlaida:
        raise
    except Exception as e:
        raise SiuntimoKlaida('%s: %s' % (type(e).__name__, e))
    finally:
        if os.path.exists(dalis):
            try:
                os.remove(dalis)
            except OSError:
                pass
