# -*- coding: utf-8 -*-
"""Skaityklė — русский интерфейс (2026-10-29). Ключ = литовская фраза (kalba.py).
Проверка: `_bandymai\\patikra_vertimu.py` — все ключи на месте, места %s/%d совпадают."""
ZODYNAS = {
    ' Spėjo: %s.': ' Успели: %s.',
    ' · darbas ≈ %s': ' · работа ≈ %s',
    '%d min': '%d мин',
    '%d val. %02d min': '%d ч %02d мин',
    '%s kalbos balsai dar neparsisiųsti (%d MB). Spauskite „Parsisiųsti balsą…" — tai daroma '
    'vieną kartą.':
        'Голоса для языка «%s» ещё не загружены (%d MB). Нажмите «Загрузить голос…» — это '
        'нужно сделать один раз.',
    '%s simb.%s · %s': '%s симв.%s · %s',
    '%s — tekstas į mp3': '%s — текст в mp3',
    '.txt failas — spauskite „Pasirinkti…"': 'Файл .txt — нажмите «Выбрать…»',
    'Apie programą': 'О программе',
    'Apie...': 'О программе...',
    'Atstatyti': 'Сбросить',
    'Atšaukiama…': 'Отмена…',
    'Atšaukta.%s Nebaigto failo ankstesnė versija (jei buvo) nepaliesta.':
        'Отменено.%s Прежняя версия незавершённого файла (если была) не тронута.',
    'Atšaukta: %s. Pusiau parsiųstų failų nelieka.':
        'Отменено: %s. Недокачанных файлов не остаётся.',
    'Atšaukti': 'Отмена',
    'Balsai dar siunčiami. Nutraukti siuntimą ir uždaryti langą?':
        'Голоса ещё загружаются. Прервать загрузку и закрыть окно?',
    'Balsai parsisiunčiami vieną kartą — po to programa veikia be interneto.\n\nParsisiųsti '
    'dabar?\n\n%s\n\nIš viso %d MB, iš Piper balsų katalogo (huggingface.co).':
        'Голоса загружаются один раз — после этого программа работает без интернета.\n\n'
        'Загрузить сейчас?\n\n%s\n\nВсего %d MB, из каталога голосов Piper (huggingface.co).',
    'Balsai paruošti. Pasirinkite .txt failą arba įklijuokite tekstą, tada „Daryti mp3".':
        'Голоса готовы. Выберите файл .txt или вставьте текст, затем нажмите «Сделать mp3».',
    'Balsas': 'Голос',
    'Balsas „%s" dar neparsisiųstas. Parsisiųskite jį: ⚙ → Kalbos ir balsai.':
        'Голос «%s» ещё не загружен. Загрузите его: ⚙ → Языки и голоса.',
    'Balso numatytasis greitis (1,00×)': 'Скорость голоса по умолчанию (1,00×)',
    'Balso „%s" failas sugadintas. Parsisiųskite jį iš naujo: ⚙ → Kalbos ir balsai.':
        'Файл голоса «%s» повреждён. Загрузите его заново: ⚙ → Языки и голоса.',
    'Dar nėra ką klausyti — pirma spauskite „Daryti mp3".':
        'Пока нечего слушать — сначала нажмите «Сделать mp3».',
    'Daryti mp3': 'Сделать mp3',
    'Didžiosiomis rašyti žodžiai būtų skaitomi raidėmis':
        'Слова, написанные заглавными, читались бы по буквам',
    'Ekvalaizeris': 'Эквалайзер',
    'Ekvalaizeris lygus, garsumas +%d dB, pauzė %s s':
        'Эквалайзер ровный, громкость +%d дБ, пауза %s с',
    'Garsumas': 'Громкость',
    'Greitis': 'Скорость',
    'Groja pavyzdys — garso nustatymus (⚙) galima keisti grojant.':
        'Звучит образец — настройки звука (⚙) можно менять прямо во время прослушивания.',
    'Instrukcija': 'Инструкция',
    'Iš failo': 'Из файла',
    'Iš lango': 'В окне',
    'Išvalyti': 'Очистить',
    'Išvalyti pasirinktą šaltinį: failą arba lango tekstą':
        'Очистить выбранный источник: файл или текст в окне',
    'Jau yra %s:\n%s\n\nPerrašyti?': 'Уже есть (%s):\n%s\n\nПерезаписать?',
    'Jei tekste yra „---", failai bus numeruojami: vardas_01.mp3, vardas_02.mp3…':
        'Если в тексте есть «---», файлы будут пронумерованы: имя_01.mp3, имя_02.mp3…',
    'Jungiamasi prie Piper balsų katalogo…': 'Подключение к каталогу голосов Piper…',
    'Kairėje — kaip parašyta tekste, dešinėje — kaip turi skambėti, pvz. „Home Assistant" → '
    '„Hom Asistent". Galioja ištisiems žodžiams, didžiosios raidės nesvarbu. Pažymėkite eilutę ir '
    'spauskite ▸ — išgirsite, kaip skamba.':
        'Слева — как написано в тексте, справа — как должно звучать, например «HTML» → '
        '«эйч ти эм эль». Действует для целых слов, регистр не важен. Выделите строку и нажмите '
        '▸ — услышите, как звучит.',
    'Kalba': 'Язык',
    'Kalbos ir balsai': 'Языки и голоса',
    'Kalbėjimo greitis — tas pats, kas pagrindiniame lange. Grojant pavyzdys persidaro nauju '
    'greičiu.':
        'Скорость речи — та же, что в главном окне. Звучащий образец пересоздаётся с новой '
        'скоростью.',
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
        'Что произойдёт после нажатия OK:\n\n'
        '1. Откроется браузер со страницей ИИ-помощника claude.ai.\n'
        '   В поле сообщения уже будет английское вступление —\n'
        '   рассказ о том, что это за программа.\n'
        '2. НЕ ПУГАЙТЕСЬ красного предупреждения над сообщением —\n'
        '   claude.ai показывает его всегда, когда текст приходит по ссылке.\n'
        '3. В конце сообщения, после слов «My question:», напишите СВОЙ\n'
        '   вопрос — можно по-русски! — и отправьте.\n'
        '4. Если ИИ ответит по-английски, попросите: «ответь\n'
        '   по-русски».\n\n'
        'Примечание: claude.ai может попросить войти (бесплатный\n'
        'аккаунт). Без вашего нажатия ничего не отправляется.',
    'Kiekvienos kalbos balsai parsisiunčiami vieną kartą iš Piper balsų katalogo '
    '(huggingface.co). Po to viskas veikia be interneto.':
        'Голоса каждого языка загружаются один раз из каталога голосов Piper (huggingface.co). '
        'После этого всё работает без интернета.',
    'Kraunamas balsas…': 'Подготовка голоса…',
    'Kur įrašyti mp3': 'Куда сохранить mp3',
    'Kūrėjo puslapis:': 'Страница разработчика:',
    'Nepavyko atidaryti instrukcijos: %s': 'Не удалось открыть инструкцию: %s',
    'Nepavyko atidaryti:\n%s\n\n%s': 'Не удалось открыть:\n%s\n\n%s',
    'Nepavyko paleisti garso.': 'Не удалось воспроизвести звук.',
    'Nepavyko parsisiųsti balsų: %s.\n\nPatikrinkite interneto ryšį ir bandykite dar '
    'kartą.\n\n(%s)':
        'Не удалось загрузить голоса: %s.\n\nПроверьте подключение к интернету и попробуйте '
        'ещё раз.\n\n(%s)',
    'Nepavyko parsisiųsti: %s.': 'Не удалось загрузить: %s.',
    'Nepavyko perskaityti failo:\n%s\n\n%s': 'Не удалось прочитать файл:\n%s\n\n%s',
    'Nepavyko įrašyti failo:\n%s\n\nGal jis atidarytas kitoje programoje (grotuve)? Uždarykite '
    'ją ir bandykite dar kartą.':
        'Не удалось сохранить файл:\n%s\n\nВозможно, он открыт в другой программе (плеере)? '
        'Закройте её и попробуйте ещё раз.',
    'Nepavyko.': 'Не получилось.',
    'Neradote atsakymo? Klauskite DI': 'Не нашли ответа? Спросите ИИ',
    'Netinkami balso nustatymai: %s': 'Неверные настройки голоса: %s',
    'Nustatymai': 'Настройки',
    'Nustatymai: ekvalaizeris, garsumas, pauzės, kalbų balsai':
        'Настройки: эквалайзер, громкость, паузы, голоса языков',
    'Nėra teksto, kurį būtų galima perskaityti.': 'Нет текста, который можно прочитать.',
    'Pagalba': 'Справка',
    'Parsisiųsta: %s. Balsai patikrinti (SHA256) ir paruošti.':
        'Загружено: %s. Голоса проверены (SHA256) и готовы.',
    'Parsisiųsti': 'Загрузить',
    'Parsisiųsti balsą…': 'Загрузить голос…',
    'Paruošta: %s, iš viso %s. Paklausykite; nepatiko — pakeiskite greitį, balsą ar garsą (⚙) '
    'ir darykite iš naujo.':
        'Готово: %s, всего %s. Послушайте; не понравилось — измените скорость, голос или звук '
        '(⚙) и сделайте заново.',
    'Pasiklausyti: pažymėtą tekstą arba teksto pradžią, su dabartiniais nustatymais':
        'Прослушать: выделенный текст или начало текста, с текущими настройками',
    'Pasirinkite .txt failą arba įklijuokite tekstą, tada „Daryti mp3".':
        'Выберите файл .txt или вставьте текст, затем нажмите «Сделать mp3».',
    'Pasirinkite .txt failą — arba pažymėkite „Iš lango" ir įklijuokite tekstą.':
        'Выберите файл .txt — или отметьте «В окне» и вставьте текст.',
    'Pasirinkti…': 'Выбрать…',
    'Pauzė tarp pastraipų': 'Пауза между абзацами',
    'Pavyzdys paruoštas.': 'Образец готов.',
    'Pavyzdžio paruošti nepavyko.': 'Не удалось подготовить образец.',
    'Pašalinti': 'Удалить',
    'Pridėti': 'Добавить',
    'Programai trūksta dalių — įdiekite ją iš naujo.':
        'Не хватает частей программы — переустановите её.',
    'Programai trūksta dalių, todėl balsai neskambėtų taip, kaip turi:':
        'Не хватает частей программы, поэтому голоса звучали бы не так, как должны:',
    'Rašoma': 'Пишется',
    'Reginutė — mokyta iš LIEPA garsyno (CC BY 4.0)\n'
    'Ingutė — išaugo iš Reginutės modelio (NewGenLTU OpenRAIL-D, žr. LICENSE-VOICE)\n'
    'Dmitri — OHF-Voice voice-datasets (CC0)\n'
    'Cori — LibriVox įrašai (vieša nuosavybė)\n'
    'Thorsten — Thorsten-Voice (CC0)\n'
    'Balsai parsisiunčiami iš Piper balsų katalogo (huggingface.co)\n'
    'Varikliai — Piper (GPL-3.0), pedalboard (GPL-3.0)':
        'Reginutė — обучена на корпусе LIEPA (CC BY 4.0)\n'
        'Ingutė — выросла из модели Reginutė (NewGenLTU OpenRAIL-D, см. LICENSE-VOICE)\n'
        'Dmitri — OHF-Voice voice-datasets (CC0)\n'
        'Cori — записи LibriVox (общественное достояние)\n'
        'Thorsten — Thorsten-Voice (CC0)\n'
        'Голоса загружаются из каталога голосов Piper (huggingface.co)\n'
        'Движки — Piper (GPL-3.0), pedalboard (GPL-3.0)',
    'Ruošiamas pavyzdys…': 'Готовится образец…',
    'Siunčiama: %s — %d iš %d MB': 'Загрузка: %s — %d из %d MB',
    'Spauskite „Pasiklausyti" ir judinkite slankiklius — garsas keičiasi iš karto. Užveskite '
    'pelę ant juostos vardo — pamatysite, už ką ji atsakinga.':
        'Нажмите «Прослушать» и двигайте ползунки — звук меняется сразу. Наведите мышь на '
        'название полосы — увидите, за что она отвечает.',
    'Sukurta naudojant DI: kodą rašė Claude, ikona — DI.\n'
    'Įgarsinti įrašai yra sintetiniai — mp3 faile tai pažymėta.':
        'Создано с помощью ИИ: код написал Claude, иконку — ИИ.\n'
        'Озвученные записи синтетические — это отмечено в mp3-файле.',
    'Tariama': 'Произносится',
    'Tarimas…': 'Произношение…',
    'Tarimo žodynėlis': 'Словарь произношения',
    'Tarimo žodynėlis: kaip parašyta → kaip turi skambėti':
        'Словарь произношения: как написано → как должно звучать',
    'Tekstas': 'Текст',
    'Tekstas (*.txt);;Visi failai (*)': 'Текст (*.txt);;Все файлы (*)',
    'Tekstas į mp3 lietuvių, rusų, anglų ar vokiečių balsu. Tekstas niekur\nnesiunčiamas, '
    'viskas lieka kompiuteryje; į internetą programa eina\ntik parsisiųsti balsų ir paspaudus '
    '„Klauskite DI".':
        'Текст в mp3 литовским, русским, английским или немецким голосом.\nТекст никуда '
        'не отправляется, всё остаётся на компьютере; в интернет\nпрограмма выходит только для '
        'загрузки голосов и по кнопке «Спросите ИИ».',
    'Tekstas, kurį įgarsinti': 'Текст для озвучивания',
    'Tokio aplanko nėra:\n%s': 'Такой папки нет:\n%s',
    'Trūksta failo: %s': 'Не хватает файла: %s',
    'Tyla tarp pastraipų. Skaidrėms dažnai patogu ilgesnė.':
        'Тишина между абзацами. Для слайдов часто удобнее подлиннее.',
    'Uždaryti': 'Закрыть',
    'Versija %s': 'Версия %s',
    'Viso įrašo garsumas. Garsiausios vietos apsaugotos nuo traškėjimo.':
        'Громкость всей записи. Самые громкие места защищены от треска.',
    'Vėliau': 'Позже',
    '[… rodoma tik pradžia — įgarsinamas visas failas]':
        '[… показано только начало — озвучивается весь файл]',
    'greičiau': 'быстрее',
    'igarsinta': 'озвучка',
    'kur įrašyti .mp3 (paklausiu, jei tuščia)': 'куда сохранить .mp3 (спрошу, если пусто)',
    'laukia eilėje': 'в очереди',
    'lėčiau': 'медленнее',
    'parsisiųsta': 'загружено',
    'Čia bus rodoma failo pradžia.': 'Здесь будет показано начало файла.',
    'Įdiekite Skaityklę iš naujo.': 'Переустановите Skaityklė.',
    'Įgarsinta pastraipų: %d iš %d': 'Озвучено абзацев: %d из %d',
    'Įrašyti į': 'Сохранить в',
    'Šios kalbos balsai dar neparsisiųsti (⚙ → Kalbos ir balsai)':
        'Голоса этого языка ещё не загружены (⚙ → Языки и голоса)',
    'Žodžių sąrašas neįkeltas iš programos katalogo':
        'Список слов не загружен из папки программы',
    '≈ %s garso': '≈ %s звука',
    '■  Sustabdyti': '■  Стоп',
    '▶  Pasiklausyti': '▶  Прослушать',
    '▶  Perklausyti': '▶  Прослушать файл',
    '▸  Pasiklausyti': '▸  Прослушать',
    # main.PAVYZDYS ir main.LANGO_UZUOMINA (per kintamąjį)
    'Laba diena. Šiandien kalbėsime apie fotosintezę, procesą, kurio metu augalai, naudodami '
    'saulės šviesą, gamina deguonį. Pasiklausykite, kaip skamba balsas, ir pasirinkite, kas jūsų '
    'ausiai maloniausia.':
        'Добрый день. Сегодня мы поговорим о фотосинтезе — процессе, в котором растения с '
        'помощью солнечного света производят кислород. Послушайте, как звучит голос, и выберите '
        'то, что приятнее вашему уху.',
    'Įklijuokite ar įrašykite tekstą čia.\n\n'
    'Tuščia eilutė — pauzė tarp pastraipų.\n'
    'Eilutė  ---  padalins įrašą į kelis mp3 (pvz., po vieną kiekvienai skaidrei).\n'
    'Pažymėkite fragmentą ir spauskite ▸ — išgirsite tik jį.':
        'Вставьте или напишите текст здесь.\n\n'
        'Пустая строка — пауза между абзацами.\n'
        'Строка  ---  разделит запись на несколько mp3 (например, по одному на слайд).\n'
        'Выделите фрагмент и нажмите ▸ — услышите только его.',
    # garsas.JUOSTOS: vardai ir užuominos
    'Gylis': 'Глубина',
    'Šiluma': 'Теплота',
    'Pilnumas': 'Полнота',
    'Vidurys': 'Середина',
    'Aiškumas': 'Чёткость',
    'Ryškumas': 'Яркость',
    'S garsai': 'Шипящие',
    'Balso kūnas ir sodrumas. Per daug — balsas dunda.':
        'Тело и насыщенность голоса. Слишком много — голос гудит.',
    'Šiltumas. Per daug — balsas tampa neaiškus, „purvinas".':
        'Теплота. Слишком много — голос становится неясным, «грязным».',
    'Balso pilnumas. Per daug — skamba kaip iš kartoninės dėžės.':
        'Полнота голоса. Слишком много — звучит как из картонной коробки.',
    'Balso branduolys. Per daug — nosinis, „telefoninis" skambesys.':
        'Ядро голоса. Слишком много — гнусавый, «телефонный» звук.',
    'Žodžių suprantamumas — čia gyvena priebalsiai.':
        'Разборчивость слов — здесь живут согласные.',
    'Artumas, balsas „prie ausies". Per daug — rėžia ausį.':
        'Близость, голос «у самого уха». Слишком много — режет слух.',
    'Gaivumas, s, š, z, ž. Per daug — švilpia; per mažai — duslu.':
        'Свежесть: с, ш, з, ж. Слишком много — свистит; слишком мало — глухо.',
}
