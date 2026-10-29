# -*- coding: utf-8 -*-
"""SĄSAJOS KALBA — LT / RU / EN / DE (2026-10-29).

Šablonas — SpeakDream `vertejas\\kalba.py` (o tas — iš PHOTO home): **lietuviškas sakinys yra pats
raktas**, `t()` grąžina vertimą arba, jei jo nėra, patį raktą. Nulis Qt priklausomybių.

Skirtumas nuo SpeakDream — vienas, Roberto sprendimas 10-29: *„interfeisas gali keistis nuo to,
kaip langelyje pasirenkam kalbą"*. SpeakDream sąsajos kalbą laiko atskirai nuo pokalbio kalbos;
Skaityklėje jos SUTAMPA — pasirinkta teksto kalba yra ir lango kalba (`nustatyk`). Pasekmė, kurią
Robertas žino: lietuvis, darantis rusišką mp3, mato rusišką langą. Kalbų vardai sąraše todėl
visada rašomi SAVO kalba — kelias atgal matosi, net kai sąsaja nesuprantama.

Kas NEverčiama: kalbų vardai (Lietuvių, Русский…), balsų vardai, programos vardas „Skaityklė".
"""
import os

KALBOS = ('lt', 'ru', 'en', 'de')
VARDAI = {'lt': 'Lietuvių', 'ru': 'Русский', 'en': 'English', 'de': 'Deutsch'}

# Windows pirminiai kalbų ID (LANGID & 0x3FF) — tas pats žemėlapis, kaip SpeakDream/PHOTO home.
_OS_LANGID = {0x27: 'lt', 0x19: 'ru', 0x07: 'de'}


def os_kalba():
    """Pirmam paleidimui: kokia kalba kalba pati Windows. Visos nepažįstamos — anglų."""
    try:
        import ctypes
        langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        return _OS_LANGID.get(langid & 0x3FF, 'en')
    except Exception:
        pass
    try:
        import locale
        loc = (locale.getlocale()[0] or '').lower()
        for pre in ('lt', 'ru', 'de'):
            if loc.startswith(pre):
                return pre
    except Exception:
        pass
    return 'en'


# Patikroms — kad testas nepriklausytų nuo nustatymų (kaip SpeakDream `VERTEJAS_LANG`).
_env = os.environ.get('SKAITYKLE_LANG')
LANG = _env if _env in KALBOS else 'lt'

_ZODYNAI = {}
for _k in ('en', 'ru', 'de'):
    try:
        _ZODYNAI[_k] = __import__('kalba_' + _k).ZODYNAS
    except Exception:
        # Trūkstamas žodynas neturi nuversti programos: matysis lietuviški raktai — blogiau
        # nei vertimas, bet daug geriau nei nepasileidžianti dovana. Pagauna patikra.
        _ZODYNAI[_k] = {}


def nustatyk(kodas):
    """Sąsajos kalba = pasirinkta teksto kalba. Langas po to kuriamas iš naujo (main.py)."""
    global LANG
    LANG = kodas if kodas in KALBOS else 'lt'


def t(tekstas):
    """Lietuviškas sakinys → tos pačios prasmės sakinys pasirinkta kalba."""
    if LANG == 'lt':
        return tekstas
    return _ZODYNAI.get(LANG, {}).get(tekstas, tekstas)


def skaicius(x, formatas='%.2f'):
    """Dešimtainis kablelis lietuviams, rusams ir vokiečiams, taškas — anglams."""
    s = formatas % x
    return s if LANG == 'en' else s.replace('.', ',')


# Daiktavardžio forma pagal skaičių. Lietuvių: 1, 21 failas · 2–9, 22 failai · 10–20 failų;
# rusų: 1, 21 файл · 2–4 файла · 5–20 файлов; anglų ir vokiečių — vienaskaita tik 1.
_FORMOS = {
    'failas': {'lt': ('failas', 'failai', 'failų'), 'ru': ('файл', 'файла', 'файлов'),
               'en': ('file', 'files', 'files'), 'de': ('Datei', 'Dateien', 'Dateien')},
    'mp3 failas': {'lt': ('mp3 failas', 'mp3 failai', 'mp3 failų'),
                   'ru': ('mp3-файл', 'mp3-файла', 'mp3-файлов'),
                   'en': ('mp3 file', 'mp3 files', 'mp3 files'),
                   'de': ('MP3-Datei', 'MP3-Dateien', 'MP3-Dateien')},
}


def kiek(n, zodis):
    """`kiek(3, 'failas')` → „3 failai" / „3 файла" / „3 files" / „3 Dateien"."""
    formos = _FORMOS[zodis][LANG]
    d, s = n % 10, n % 100
    if LANG == 'lt':
        i = 2 if d == 0 or 10 <= s <= 20 else (0 if d == 1 else 1)
    elif LANG == 'ru':
        i = 0 if d == 1 and s != 11 else (1 if 2 <= d <= 4 and not 12 <= s <= 14 else 2)
    else:
        i = 0 if n == 1 else 1
    return '%d %s' % (n, formos[i])
