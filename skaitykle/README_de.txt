SKAITYKLĖ — Text zu MP3
=======================

Das Programm liest Text mit der gewählten Stimme vor und speichert ihn als
MP3. Geeignet für Folienkommentare ebenso wie für ein ganzes Buch. Alles
geschieht auf Ihrem Computer: ohne Konto, ohne Grafikkarte. Der Text wird
nirgendwohin gesendet. Internet wird nur einmal gebraucht — zum
Herunterladen der Stimmen der gewählten Sprache.


SO GEHT ES
----------

1. Sprache und Stimme
   Sprachen: Litauisch, Russisch, Englisch, Deutsch. Wenn Sie die Sprache
   wechseln, wechselt auch das ganze Programmfenster. Litauische Stimmen —
   Ingutė und Reginutė, Russisch — Dmitri, Englisch — Cori, Deutsch —
   Thorsten. Mit der Taste ▸ daneben hören Sie, wie die Stimme mit den
   aktuellen Einstellungen klingt. Fehlen die Stimmen der Sprache noch,
   erscheint daneben „Stimme herunterladen…“.

2. Tempo
   Schieberegler: nach links — langsamer, nach rechts — schneller. 1,00×
   ist das normale Tempo der Stimme; ↺ setzt es zurück.

3. Text — woher er kommt
   ● Aus Datei   — „Auswählen…“ klicken und eine .txt-Datei wählen. Das
                   Programm zeigt Dateiname, Größe, wie lange Aufnahme und
                   Bearbeitung ungefähr dauern, und im Fenster nur den
                   Textanfang. Ein ganzes Buch wird nicht angezeigt, aber
                   ganz vorgelesen. Korrigieren Sie die Datei im Editor,
                   müssen Sie sie nicht neu wählen — beim nächsten „MP3
                   erstellen“ wird der korrigierte Text genommen.
   ● Im Fenster  — Text direkt ins Fenster einfügen oder tippen (z. B. aus
                   Folien kopiert). Die Dateizeile ist dabei abgedunkelt.
   „Leeren“ leert die gewählte Quelle.

   In beiden Fällen:
   - eine leere Zeile zwischen Absätzen = Pause (Länge in ⚙ einstellen);
   - eine Zeile aus drei Bindestrichen  ---  teilt die Aufnahme in MEHRERE
     MP3-Dateien: name_01.mp3, name_02.mp3… — praktisch, eine pro Folie;
   - markieren Sie ein Textstück und drücken Sie ▸ — Sie hören nur dieses.

4. Aussprache…
   Ein Wörterbuch „wie geschrieben → wie es klingen soll“. Für Fachbegriffe,
   Namen, Fremdwörter, z. B. „Nginx“ → „Engine X“. Zeile markieren und ▸
   drücken — Sie hören, wie es klingt. Jede Sprache hat ihr eigenes
   Wörterbuch; es wird gespeichert.

5. Speichern in
   Wenn eine Datei gewählt ist, füllt sich der MP3-Ort von selbst: derselbe
   Ordner, derselbe Name. Bei Text aus dem Fenster fragt das Programm nach,
   wenn das Feld leer ist.

6. MP3 erstellen
   Das Programm liest den Text Absatz für Absatz und zeigt den Fortschritt.
   Während der Arbeit wird die Taste zu „Abbrechen“ — fertige Dateien
   bleiben, und die frühere Version einer unfertigen Datei bleibt
   unverändert.

7. Abspielen
   Spielt die gerade erstellten Dateien ab (mehrere — nacheinander).
   Gefällt es nicht? Tempo, Stimme oder Klang (⚙) ändern und noch einmal
   „MP3 erstellen“ klicken.


EINSTELLUNGEN (⚙)
-----------------

Tempo — derselbe Regler wie im Hauptfenster, damit er beim Einstellen zur
Hand ist (ändern Sie einen, folgt der andere). Bewegen Sie ihn während
einer Hörprobe, wird die Probe einen Moment später im neuen Tempo neu
erstellt.

Equalizer — sieben Bänder von tief (125 Hz) bis hoch (8 kHz). Fahren Sie
mit der Maus über einen Bandnamen, um zu sehen, wofür es zuständig ist.
Klicken Sie auf „Anhören“ und bewegen Sie die Regler: Der Klang ändert sich
sofort.

  Tiefe (125 Hz)     — Körper der Stimme; zu viel — sie dröhnt
  Wärme (250 Hz)     — Wärme; zu viel — undeutlich
  Fülle (500 Hz)     — zu viel — klingt wie aus einer Kiste
  Mitten (1 kHz)     — zu viel — nasaler, „telefonartiger“ Klang
  Klarheit (2 kHz)   — Wortverständlichkeit
  Präsenz (4 kHz)    — Nähe; zu viel — schneidet ins Ohr
  S-Laute (8 kHz)    — s, sch, z; zu viel — es zischt

Lautstärke — Lautstärke der ganzen Aufnahme. Die lautesten Stellen sind
vor Knacksen geschützt.

Pause zwischen Absätzen — Stille in Sekunden. Für Folien ist eine längere
oft praktisch.

„Zurücksetzen“ stellt die Standardwerte wieder her: neutraler Equalizer,
Lautstärke +6 dB, Pause 1,3 s.

Sprachen und Stimmen — die Stimmen jeder Sprache werden einmal aus dem
Piper-Stimmenkatalog (huggingface.co) geladen: Litauisch 128 MB, die
anderen je 64 MB. Eine geladene Stimme wird geprüft (SHA256) — eine
beschädigte oder unfertige Datei wird nie behalten. Die bei der
Installation angehakten Sprachen bietet das Programm beim ersten Start zum
Herunterladen an; jede andere jederzeit hier.


WIE LANGE ES DAUERT
-------------------

Unter dem Text steht eine Schätzung: „≈ 2 Std. 22 Min. Audio ·
Bearbeitung ≈ 7 Min.“. Das ist ein grober Wert nach der Zeichenzahl. Ein
Buch (100 Seiten) dauert meist einige Minuten; den Computer können Sie
währenddessen weiter benutzen.


TIPPS FÜR DEN TEXT
------------------

* Absatz = Pause. Eine leere Zeile zwischen Gedanken lässt die Stimme
  „Luft holen“.
* Text aus einem PDF ist oft mitten im Satz umbrochen. Das Programm
  verbindet solche Zeilen selbst, wenn die nächste Zeile mit einem
  Kleinbuchstaben beginnt.
* Zahlen und Uhrzeiten liest die Stimme selbst („15:25“ — „fünfzehn Uhr
  fünfundzwanzig“). Klingt etwas falsch, schreiben Sie es so aus, wie es
  klingen soll, oder tragen Sie es unter „Aussprache“ ein.
* Abkürzungen in Großbuchstaben werden unter Umständen buchstabiert.


WENN ETWAS NICHT KLAPPT
-----------------------

* „Datei konnte nicht gespeichert werden“ — diese MP3 ist wahrscheinlich
  in einem Player geöffnet. Player schließen und erneut versuchen.
* „Ton konnte nicht abgespielt werden“ — prüfen Sie, ob der Windows-Ton
  funktioniert und nicht stummgeschaltet ist.
* „Stimmen konnten nicht heruntergeladen werden“ — Internetverbindung
  prüfen und noch einmal „Herunterladen“ klicken (⚙ → Sprachen und
  Stimmen).
* Alles andere: ? → „Keine Antwort gefunden? KI fragen“.


WICHTIG
-------

Die Aufnahmen sind synthetisch (mit einer Stimme der künstlichen
Intelligenz erstellt). In der MP3-Datei ist das mit der Markierung
„Synthetische Stimme (KI)“ vermerkt.
