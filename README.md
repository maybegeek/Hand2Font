# Hand2Font

Von handgekritzelten Zeichen zum weiterbearbeitbaren Font. Drei Blatt mit je 49 Kästchen stehen bereit für die jeweils eigene Umsetzung der jeweiligen Zeichen. Sind die Kästchen ausgefüllt, können die Bögen gescannt werden -- bei **600dpi**, in **Graustufen** und im **jpg-Format**.

Die vorliegenden Bögen können dann umgewandelt werden. Dabei werden die Kästchen per `opencv` erkannt, der Inhalt der Boxen dann ausgeschnitten und die vorliegenden Einzelbilder der Kästcheninhalte werden dann umgewandelt in `*.ppm`-Dateien um diese dann per `potrace` zu vektorisieren.

Je nach Verwendung bestimmter Versionen zur Erfassung (version={1,2}) können damit `139` oder `149` Zeichen erfasst werden. Die erstellten `*.svg`-Dateien werden im nächsten Schritt an vorgesehenen Positionen im `Font` platziert.



## magic

Bei der Erstellung des Fonts werden zu den eigenen Zeichen noch weitere Einstellungen vorgenommen:

* der Zeichensatz festgelegt: `UnicodeFull`
* Versionsnummer für den Font vergeben: `1.0`
* font weight: `Regular`
* `fontname`, `familyname` und `fullname`
* `font.comment = 'FONT_COMMENT'`
* `font.copyright = 'FONT_LICENSE'`
* em-size: `2048`
* Layers: `cubic`
* `stylistic sets`
* `liga`, normale Ligaturen
* `dlig`, discretionary ligatures
* besondere Leerzeichen
* Katzenpfoten!
* `.notdef`-Quisquilie
* side bearings
* Größenanpassung ... automagisch
* Grundlinien- x-Höhen-Anpassung


## Lehre(n)

Wie nicht unschwer zu erkennen, waren und sind unterschiedliche Teile dieses Projekts auch für das eigene Lernen hinsichtlich `python`, `opencv`, `Fontforge` und Typografie im allgemeinen interessant.

Die automatische Umwandlung der Zeichen soll einige Schritte bei der Erstellung einer eigenen Schrift mit `Fontforge` beschleunigen. Es wartet auf jeden Interessierten aber noch genügend (Fein-)Arbeit bei der Verbesserung der automatisch erstellen `*.sfd`-Datei.


## Nutzung

`python3 Scan2SVG.py -A a.jpg -B b.jpg -C c.jpg -t 160 -p Dateien -o Ordner -n Hand2Font -v 2`



## Lizenz

[CC-BY-NC-SA-4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
