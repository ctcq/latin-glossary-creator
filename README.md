Dieses Programm dient der Analyse von lateinischsprachigen Texten. Es kann zur Erstellung eines Glossars im HTML-Format sowie auch interaktiv in der Kommandozeile verwendet werden.

**Installation:**

Zum Ausführen wird **Python 3** benötigt.
Externe Module sind das **Classical Language Toolkit** und **Unidecode**.

Diese Software kann mit pip jeweils mit

>> pip install -r requirements.txt

installiert werden.

**Benutzung:**

Zum starten des Programms führe folgenden Befehl in der Kommandozeile aus:

>> python3 latin_glossary_creator.py <OPTION 1> <OPTION 2>

<OPTION 1> ist der Pfad zum Ordner mit den lateinischen Texten. Diese Dateien sollten im Plaintext (also im Format .txt) gespeichert sein, nicht in (.doc, .docx, .pdf, o.ä.). Zusätzlich sollten die Dateinamen in einer sinnvollen Weise (nach Lektionen, nach Seitenzahl,...) alphabetisch geordnet sein.

Der Inhalt dieser Dateien sollte nur lateinische Wörter enthalten. Zwar berücksichtigt das Programm Satzzeichen oder auch Akzente für die Betonung, jedoch wird nicht garantiert dass dies fehlerfrei geschieht.

**Wichtig:** In dem übergebenen Ordner sollten sich keine weiteren Dateien befinden.

Für eine valide Form des Übergebenen Ordners siehe den Ordner **Beispieltexte**.

<OPTION 2> bestimmt den Ordner, in dem das Glossar im HTML-Format geschrieben werden soll. 

Wird <OPTION 2> weggelassen, so wird das Programm im interaktiven Modus gestartet. Zur Eingabe eines Wortes und der entsprechenden Lektion (Position der Datei im übergebenen Ordner) gibt das Programm entsprechende Werte aus dem Glossar zurück.

