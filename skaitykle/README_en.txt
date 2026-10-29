SKAITYKLĖ — text to mp3
=======================

The program reads text aloud in the voice you choose and saves it as mp3.
Good for slide narration and for a whole book alike. Everything happens on
your computer: no account, no graphics card. The text is never sent
anywhere. Internet is needed only once — to download the voices of the
language you choose.


HOW TO USE
----------

1. Language and Voice
   Languages: Lithuanian, Russian, English, German. When you change the
   language, the whole program window switches to it too. Lithuanian
   voices — Ingutė and Reginutė, Russian — Dmitri, English — Cori, German —
   Thorsten. The ▸ button next to the voice lets you hear how it sounds
   with the current settings. If the language's voices are not there yet,
   a “Download voice…” button appears next to it.

2. Speed
   Slider: to the left — slower, to the right — faster. 1.00× is the
   voice's default pace; ↺ brings it back.

3. Text — where it comes from
   ● From file      — click “Choose…” and pick a .txt file. The program
                      shows the file name, its size, roughly how long the
                      recording and the work will take, and only the
                      beginning of the text in the window. A whole book is
                      not shown, but all of it is read aloud. If you fix
                      the file in Notepad, there is no need to choose it
                      again — the next “Make mp3” takes the fixed text.
   ● In the window  — paste or type the text straight into the window (for
                      example, copied from slides). The file line is
                      dimmed meanwhile.
   “Clear” clears whichever source is selected.

   In both cases:
   - an empty line between paragraphs = a pause (set its length in ⚙);
   - a line of three dashes  ---  splits the recording into SEVERAL mp3
     files: name_01.mp3, name_02.mp3… — handy for one file per slide;
   - select a piece of text and press ▸ — you will hear only that.

4. Pronunciation…
   A list “as written → as it should sound”. For terms, names and foreign
   words, e.g. “Nginx” → “engine x”. Select a row and press ▸ to hear how
   it sounds. Each language has its own list; it is saved.

5. Save to
   When you choose a file, the mp3 location fills in by itself: the same
   folder, the same name. For text in the window the program asks if the
   field is empty.

6. Make mp3
   The program reads the text paragraph by paragraph and shows progress.
   While it works the button turns into “Cancel” — files already finished
   stay, and the earlier version of an unfinished file is left untouched.

7. Play back
   Plays the files just made (several — one after another). Don't like
   it? Change the speed, voice or sound (⚙) and click “Make mp3” again.


SETTINGS (⚙)
------------

Speed — the same slider as in the main window, so it is at hand while
tuning (change one and the other follows). Move it while a sample is
playing and the sample is redone at the new speed a moment later.

Equalizer — seven bands from low (125 Hz) to high (8 kHz). Hover over a
band name to see what it does. Click “Listen” and move the sliders: the
sound changes right away.

  Depth (125 Hz)    — body of the voice; too much — it booms
  Warmth (250 Hz)   — warmth; too much — unclear
  Fullness (500 Hz) — too much — sounds as if from a box
  Mids (1 kHz)      — too much — nasal, “telephone” sound
  Clarity (2 kHz)   — word intelligibility
  Presence (4 kHz)  — closeness; too much — it grates
  S sounds (8 kHz)  — s, sh, z; too much — it whistles

Volume — the volume of the whole recording. The loudest parts are
protected from crackling.

Pause between paragraphs — silence in seconds. A longer one is often handy
for slides.

“Reset” brings back the defaults: flat equalizer, volume +6 dB, pause 1.3 s.

Languages and voices — the voices of each language are downloaded once from
the Piper voice catalogue (huggingface.co): Lithuanian 128 MB, the others
64 MB each. A downloaded voice is verified (SHA256) — a damaged or
unfinished file is never kept. The languages ticked during installation
are offered for download on the first start; any other language can be
downloaded here at any time.


HOW LONG IT TAKES
-----------------

Below the text you see an estimate: “≈ 2 h 22 min of audio · processing
≈ 7 min”. It is a rough figure based on the number of characters. A book
(100 pages) usually takes a few minutes; you can use the computer
meanwhile.


TIPS FOR THE TEXT
-----------------

* A paragraph = a pause. An empty line between thoughts lets the voice
  “take a breath”.
* Text copied from a PDF is often broken in the middle of a sentence. The
  program joins such lines itself when the next line starts with a lower-
  case letter.
* Numbers and times are read by the voice itself (“15:25” — “fifteen
  twenty-five”). If something sounds wrong, write it out the way it should
  sound, or add it to Pronunciation.
* Abbreviations in capitals may be spelled out letter by letter.


WHEN SOMETHING GOES WRONG
-------------------------

* “Could not save the file” — that mp3 is probably open in a player.
  Close the player and try again.
* “Could not play the sound” — check that Windows sound works and is not
  muted.
* “Could not download the voices” — check your internet connection and
  click “Download” again (⚙ → Languages and voices).
* Anything else: ? → “No answer here? Ask an AI”.


IMPORTANT
---------

The recordings are synthetic (made with an artificial-intelligence voice).
This is marked in the mp3 file with the tag “Synthetic voice (AI)”.
