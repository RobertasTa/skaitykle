# -*- coding: utf-8 -*-
"""Skaityklė — English interface (2026-10-29). Key = the Lithuanian sentence (kalba.py).
Checked by `_bandymai\\patikra_vertimu.py`: every key present, %s/%d places identical."""
ZODYNAS = {
    ' Spėjo: %s.': ' Finished in time: %s.',
    ' · darbas ≈ %s': ' · processing ≈ %s',
    '%d min': '%d min',
    '%d val. %02d min': '%d h %02d min',
    '%s kalbos balsai dar neparsisiųsti (%d MB). Spauskite „Parsisiųsti balsą…" — tai daroma '
    'vieną kartą.':
        '%s voices are not downloaded yet (%d MB). Click “Download voice…” — this is needed '
        'only once.',
    '%s simb.%s · %s': '%s chars%s · %s',
    '%s — tekstas į mp3': '%s — text to mp3',
    '.txt failas — spauskite „Pasirinkti…"': '.txt file — click “Choose…”',
    'Apie programą': 'About',
    'Apie...': 'About...',
    'Atstatyti': 'Reset',
    'Atšaukiama…': 'Cancelling…',
    'Atšaukta.%s Nebaigto failo ankstesnė versija (jei buvo) nepaliesta.':
        'Cancelled.%s The previous version of the unfinished file (if there was one) is '
        'untouched.',
    'Atšaukta: %s. Pusiau parsiųstų failų nelieka.':
        'Cancelled: %s. No half-downloaded files are left behind.',
    'Atšaukti': 'Cancel',
    'Balsai dar siunčiami. Nutraukti siuntimą ir uždaryti langą?':
        'Voices are still downloading. Stop the download and close the window?',
    'Balsai parsisiunčiami vieną kartą — po to programa veikia be interneto.\n\nParsisiųsti '
    'dabar?\n\n%s\n\nIš viso %d MB, iš Piper balsų katalogo (huggingface.co).':
        'Voices are downloaded once — after that the program works offline.\n\nDownload '
        'now?\n\n%s\n\n%d MB in total, from the Piper voice catalogue (huggingface.co).',
    'Balsai paruošti. Pasirinkite .txt failą arba įklijuokite tekstą, tada „Daryti mp3".':
        'The voices are ready. Choose a .txt file or paste text, then click “Make mp3”.',
    'Balsas': 'Voice',
    'Balsas „%s" dar neparsisiųstas. Parsisiųskite jį: ⚙ → Kalbos ir balsai.':
        'The voice “%s” is not downloaded yet. Download it: ⚙ → Languages and voices.',
    'Balso numatytasis greitis (1,00×)': 'The voice’s default speed (1.00×)',
    'Balso „%s" failas sugadintas. Parsisiųskite jį iš naujo: ⚙ → Kalbos ir balsai.':
        'The file of the voice “%s” is damaged. Download it again: ⚙ → Languages and voices.',
    'Dar nėra ką klausyti — pirma spauskite „Daryti mp3".':
        'Nothing to play yet — click “Make mp3” first.',
    'Daryti mp3': 'Make mp3',
    'Didžiosiomis rašyti žodžiai būtų skaitomi raidėmis':
        'Words in capitals would be spelled out letter by letter',
    'Ekvalaizeris': 'Equalizer',
    'Ekvalaizeris lygus, garsumas +%d dB, pauzė %s s': 'Flat equalizer, volume +%d dB, pause %s s',
    'Garsumas': 'Volume',
    'Greitis': 'Speed',
    'Groja pavyzdys — garso nustatymus (⚙) galima keisti grojant.':
        'Playing a sample — the sound settings (⚙) can be changed while it plays.',
    'Instrukcija': 'Instructions',
    'Iš failo': 'From file',
    'Iš lango': 'In the window',
    'Išvalyti': 'Clear',
    'Išvalyti pasirinktą šaltinį: failą arba lango tekstą':
        'Clear the selected source: the file or the text in the window',
    'Jau yra %s:\n%s\n\nPerrašyti?': 'Already there (%s):\n%s\n\nOverwrite?',
    'Jei tekste yra „---", failai bus numeruojami: vardas_01.mp3, vardas_02.mp3…':
        'If the text contains “---”, the files will be numbered: name_01.mp3, name_02.mp3…',
    'Jungiamasi prie Piper balsų katalogo…': 'Connecting to the Piper voice catalogue…',
    'Kairėje — kaip parašyta tekste, dešinėje — kaip turi skambėti, pvz. „Home Assistant" → '
    '„Hom Asistent". Galioja ištisiems žodžiams, didžiosios raidės nesvarbu. Pažymėkite eilutę ir '
    'spauskite ▸ — išgirsite, kaip skamba.':
        'Left — as written in the text, right — how it should sound, e.g. “Nginx” → “engine x”. '
        'Applies to whole words; capital letters do not matter. Select a row and press ▸ to hear '
        'how it sounds.',
    'Kalba': 'Language',
    'Kalbos ir balsai': 'Languages and voices',
    'Kalbėjimo greitis — tas pats, kas pagrindiniame lange. Grojant pavyzdys persidaro nauju '
    'greičiu.':
        'Speaking speed — the same as in the main window. A sample that is playing is redone at '
        'the new speed.',
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
    'paskyra). Niekas neišsiunčiama be jūsų rankos.':
        'What happens when you click OK:\n\n'
        '1. Your web browser opens the page of the AI assistant\n'
        '   claude.ai. The message box will already contain an\n'
        '   introduction explaining what this program is.\n'
        '2. DON’T WORRY about the red notice above the message —\n'
        '   claude.ai always shows it when text arrives via a link.\n'
        '3. At the end of the message, after the words “My question:”,\n'
        '   type YOUR question — in any language — and send it.\n'
        '4. The AI answers in the language you write in.\n\n'
        'Note: claude.ai may ask you to sign in (free account).\n'
        'Nothing is sent without your own click.',
    'Kiekvienos kalbos balsai parsisiunčiami vieną kartą iš Piper balsų katalogo '
    '(huggingface.co). Po to viskas veikia be interneto.':
        'The voices for each language are downloaded once from the Piper voice catalogue '
        '(huggingface.co). After that everything works offline.',
    'Kraunamas balsas…': 'Loading the voice…',
    'Kur įrašyti mp3': 'Where to save the mp3',
    'Kūrėjo puslapis:': 'Developer page:',
    'Nepavyko atidaryti instrukcijos: %s': 'Could not open the instructions: %s',
    'Nepavyko atidaryti:\n%s\n\n%s': 'Could not open:\n%s\n\n%s',
    'Nepavyko paleisti garso.': 'Could not play the sound.',
    'Nepavyko parsisiųsti balsų: %s.\n\nPatikrinkite interneto ryšį ir bandykite dar '
    'kartą.\n\n(%s)':
        'Could not download the voices: %s.\n\nCheck your internet connection and try '
        'again.\n\n(%s)',
    'Nepavyko parsisiųsti: %s.': 'Download failed: %s.',
    'Nepavyko perskaityti failo:\n%s\n\n%s': 'Could not read the file:\n%s\n\n%s',
    'Nepavyko įrašyti failo:\n%s\n\nGal jis atidarytas kitoje programoje (grotuve)? Uždarykite '
    'ją ir bandykite dar kartą.':
        'Could not save the file:\n%s\n\nIs it open in another program (a player)? Close it and '
        'try again.',
    'Nepavyko.': 'Failed.',
    'Neradote atsakymo? Klauskite DI': 'No answer here? Ask an AI',
    'Netinkami balso nustatymai: %s': 'Wrong voice settings: %s',
    'Nustatymai': 'Settings',
    'Nustatymai: ekvalaizeris, garsumas, pauzės, kalbų balsai':
        'Settings: equalizer, volume, pauses, voices for each language',
    'Nėra teksto, kurį būtų galima perskaityti.': 'There is no text to read.',
    'Pagalba': 'Help',
    'Parsisiųsta: %s. Balsai patikrinti (SHA256) ir paruošti.':
        'Downloaded: %s. The voices are verified (SHA256) and ready.',
    'Parsisiųsti': 'Download',
    'Parsisiųsti balsą…': 'Download voice…',
    'Paruošta: %s, iš viso %s. Paklausykite; nepatiko — pakeiskite greitį, balsą ar garsą (⚙) '
    'ir darykite iš naujo.':
        'Done: %s, %s in total. Have a listen; if you don’t like it, change the speed, voice or '
        'sound (⚙) and make it again.',
    'Pasiklausyti: pažymėtą tekstą arba teksto pradžią, su dabartiniais nustatymais':
        'Listen: the selected text or the beginning of the text, with the current settings',
    'Pasirinkite .txt failą arba įklijuokite tekstą, tada „Daryti mp3".':
        'Choose a .txt file or paste text, then click “Make mp3”.',
    'Pasirinkite .txt failą — arba pažymėkite „Iš lango" ir įklijuokite tekstą.':
        'Choose a .txt file — or select “In the window” and paste the text.',
    'Pasirinkti…': 'Choose…',
    'Pauzė tarp pastraipų': 'Pause between paragraphs',
    'Pavyzdys paruoštas.': 'Sample ready.',
    'Pavyzdžio paruošti nepavyko.': 'Could not prepare the sample.',
    'Pašalinti': 'Remove',
    'Pridėti': 'Add',
    'Programai trūksta dalių — įdiekite ją iš naujo.':
        'Parts of the program are missing — please reinstall it.',
    'Programai trūksta dalių, todėl balsai neskambėtų taip, kaip turi:':
        'Parts of the program are missing, so the voices would not sound as they should:',
    'Rašoma': 'Written',
    'Reginutė — mokyta iš LIEPA garsyno (CC BY 4.0)\n'
    'Ingutė — išaugo iš Reginutės modelio (NewGenLTU OpenRAIL-D, žr. LICENSE-VOICE)\n'
    'Dmitri — OHF-Voice voice-datasets (CC0)\n'
    'Cori — LibriVox įrašai (vieša nuosavybė)\n'
    'Thorsten — Thorsten-Voice (CC0)\n'
    'Balsai parsisiunčiami iš Piper balsų katalogo (huggingface.co)\n'
    'Varikliai — Piper (GPL-3.0), pedalboard (GPL-3.0)':
        'Reginutė — trained on the LIEPA corpus (CC BY 4.0)\n'
        'Ingutė — grown from the Reginutė model (NewGenLTU OpenRAIL-D, see LICENSE-VOICE)\n'
        'Dmitri — OHF-Voice voice-datasets (CC0)\n'
        'Cori — LibriVox recordings (public domain)\n'
        'Thorsten — Thorsten-Voice (CC0)\n'
        'Voices are downloaded from the Piper voice catalogue (huggingface.co)\n'
        'Engines — Piper (GPL-3.0), pedalboard (GPL-3.0)',
    'Ruošiamas pavyzdys…': 'Preparing a sample…',
    'Siunčiama: %s — %d iš %d MB': 'Downloading: %s — %d of %d MB',
    'Spauskite „Pasiklausyti" ir judinkite slankiklius — garsas keičiasi iš karto. Užveskite '
    'pelę ant juostos vardo — pamatysite, už ką ji atsakinga.':
        'Click “Listen” and move the sliders — the sound changes right away. Hover over a band '
        'name to see what it does.',
    'Sukurta naudojant DI: kodą rašė Claude, ikona — DI.\n'
    'Įgarsinti įrašai yra sintetiniai — mp3 faile tai pažymėta.':
        'Made with AI: the code was written by Claude, the icon by AI.\n'
        'The recordings are synthetic — this is marked in the mp3 file.',
    'Tariama': 'Spoken',
    'Tarimas…': 'Pronunciation…',
    'Tarimo žodynėlis': 'Pronunciation list',
    'Tarimo žodynėlis: kaip parašyta → kaip turi skambėti':
        'Pronunciation list: as written → as it should sound',
    'Tekstas': 'Text',
    'Tekstas (*.txt);;Visi failai (*)': 'Text (*.txt);;All files (*)',
    'Tekstas į mp3 lietuvių, rusų, anglų ar vokiečių balsu. Tekstas niekur\nnesiunčiamas, '
    'viskas lieka kompiuteryje; į internetą programa eina\ntik parsisiųsti balsų ir paspaudus '
    '„Klauskite DI".':
        'Text to mp3 in a Lithuanian, Russian, English or German voice.\nThe text is never sent '
        'anywhere, everything stays on this computer; the program\ngoes online only to download '
        'voices and when you click “Ask an AI”.',
    'Tekstas, kurį įgarsinti': 'Text to read aloud',
    'Tokio aplanko nėra:\n%s': 'This folder does not exist:\n%s',
    'Trūksta failo: %s': 'Missing file: %s',
    'Tyla tarp pastraipų. Skaidrėms dažnai patogu ilgesnė.':
        'Silence between paragraphs. For slides a longer one is often handy.',
    'Uždaryti': 'Close',
    'Versija %s': 'Version %s',
    'Viso įrašo garsumas. Garsiausios vietos apsaugotos nuo traškėjimo.':
        'Volume of the whole recording. The loudest parts are protected from crackling.',
    'Vėliau': 'Later',
    '[… rodoma tik pradžia — įgarsinamas visas failas]':
        '[… only the beginning is shown — the whole file is read aloud]',
    'greičiau': 'faster',
    'igarsinta': 'speech',
    'kur įrašyti .mp3 (paklausiu, jei tuščia)': 'where to save the .mp3 (I’ll ask if empty)',
    'laukia eilėje': 'queued',
    'lėčiau': 'slower',
    'parsisiųsta': 'downloaded',
    'Čia bus rodoma failo pradžia.': 'The beginning of the file will be shown here.',
    'Įdiekite Skaityklę iš naujo.': 'Please reinstall Skaityklė.',
    'Įgarsinta pastraipų: %d iš %d': 'Paragraphs read: %d of %d',
    'Įrašyti į': 'Save to',
    'Šios kalbos balsai dar neparsisiųsti (⚙ → Kalbos ir balsai)':
        'The voices for this language are not downloaded yet (⚙ → Languages and voices)',
    'Žodžių sąrašas neįkeltas iš programos katalogo':
        'The word list was not loaded from the program folder',
    '≈ %s garso': '≈ %s of audio',
    '■  Sustabdyti': '■  Stop',
    '▶  Pasiklausyti': '▶  Listen',
    '▶  Perklausyti': '▶  Play back',
    '▸  Pasiklausyti': '▸  Listen',
    # main.PAVYZDYS ir main.LANGO_UZUOMINA (per kintamąjį)
    'Laba diena. Šiandien kalbėsime apie fotosintezę, procesą, kurio metu augalai, naudodami '
    'saulės šviesą, gamina deguonį. Pasiklausykite, kaip skamba balsas, ir pasirinkite, kas jūsų '
    'ausiai maloniausia.':
        'Good afternoon. Today we will talk about photosynthesis, the process in which plants use '
        'sunlight to produce oxygen. Listen to how the voice sounds and choose what pleases your '
        'ear most.',
    'Įklijuokite ar įrašykite tekstą čia.\n\n'
    'Tuščia eilutė — pauzė tarp pastraipų.\n'
    'Eilutė  ---  padalins įrašą į kelis mp3 (pvz., po vieną kiekvienai skaidrei).\n'
    'Pažymėkite fragmentą ir spauskite ▸ — išgirsite tik jį.':
        'Paste or type the text here.\n\n'
        'An empty line — a pause between paragraphs.\n'
        'A line  ---  splits the recording into several mp3 files (e.g. one per slide).\n'
        'Select a passage and press ▸ — you will hear only that.',
    # garsas.JUOSTOS: vardai ir užuominos
    'Gylis': 'Depth',
    'Šiluma': 'Warmth',
    'Pilnumas': 'Fullness',
    'Vidurys': 'Mids',
    'Aiškumas': 'Clarity',
    'Ryškumas': 'Presence',
    'S garsai': 'S sounds',
    'Balso kūnas ir sodrumas. Per daug — balsas dunda.':
        'Body and richness of the voice. Too much — the voice booms.',
    'Šiltumas. Per daug — balsas tampa neaiškus, „purvinas".':
        'Warmth. Too much — the voice becomes unclear, “muddy”.',
    'Balso pilnumas. Per daug — skamba kaip iš kartoninės dėžės.':
        'Fullness of the voice. Too much — it sounds as if from a cardboard box.',
    'Balso branduolys. Per daug — nosinis, „telefoninis" skambesys.':
        'The core of the voice. Too much — a nasal, “telephone” sound.',
    'Žodžių suprantamumas — čia gyvena priebalsiai.':
        'Word intelligibility — this is where the consonants live.',
    'Artumas, balsas „prie ausies". Per daug — rėžia ausį.':
        'Closeness, the voice “right at your ear”. Too much — it grates.',
    'Gaivumas, s, š, z, ž. Per daug — švilpia; per mažai — duslu.':
        'Freshness: s, sh, z, zh. Too much — it whistles; too little — muffled.',
}
