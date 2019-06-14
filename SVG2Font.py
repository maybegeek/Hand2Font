#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Import vorliegender SVG-Dateien und Erstellung einer Font-Datei."""

import os
import sys
import math
import glob
import psMat
import fontforge
import tempfile
import argparse

__author__ = "Christoph Pfeiffer"
__license__ = "CC-BY-NC-SA-4.0"

ap = argparse.ArgumentParser(description='Import der SVG-Dateien in FontForge ... + magic.')
ap.add_argument('-svg', '--svgordner', help='Ordner der SVG-Dateien.', type=str, required=True)
ap.add_argument("-n", "--name", help="Name der Schrift.", required=True, type=str)
ap.add_argument("-v", "--version", help="Version des Eingabebogens.", required=True, type=int)

args = ap.parse_args()

pfad = args.svgordner
pfad = pfad.rstrip('/') + '/'
name = args.name
version = args.version

glyphsSVG = [f for f in glob.glob(pfad + "*.svg")]
glyphsSVG.sort()

# Reihenfolge der Glyphen.
# Für die unterschiedlichen Versionen der Erfassungsbögen
if version == 1:
  glyphsUTF8 = [['A', 65], ['B', 66], ['C', 67], ['D', 68], ['E', 69], ['F', 70], ['G', 71], ['H', 72], ['I', 73], ['J', 74], ['K', 75], ['L', 76], ['M', 77], ['N', 78], ['O', 79], ['P', 80], ['Q', 81], ['R', 82], ['S', 83], ['T', 84], ['U', 85], ['V', 86], ['W', 87], ['X', 88], ['Y', 89], ['Z', 90], ['Ä', 196], ['Ö', 214], ['Ü', 220], ['ẞ', 7838], ['a', 97], ['b', 98], ['c', 99], ['d', 100], ['e', 101], ['f', 102], ['g', 103], ['h', 104], ['i', 105], ['j', 106], ['k', 107], ['l', 108], ['m', 109], ['n', 110], ['o', 111], ['p', 112], ['q', 113], ['r', 114], ['s', 115], ['t', 116], ['u', 117], ['v', 118], ['w', 119], ['x', 120], ['y', 121], ['z', 122], ['ä', 228], ['ö', 246], ['ü', 252], ['ß', 223], ['1', 49], ['2', 50], ['3', 51], ['4', 52], ['5', 53], ['6', 54], ['7', 55], ['8', 56], ['9', 57], ['0', 48], ['!', 33], ['?', 63], ['§', 167], ['$', 36], ['%', 37], ['&', 38], ['/', 47], ['(', 40], [')', 41], ['{', 123], ['}', 125], ['[', 91], [']', 93], ['=', 61], ['<', 60], ['>', 62], ['|', 124], ['\\', 92], [',', 44], [';', 59], ['*', 42], ['.', 46], [':', 58], ['-', 45], ['–', 8211], ['#', 35], ['+', 43], ['~', 126], ['"', 34], ["'", 39], ['@', 64], ['^', 94], ['_', 95], ['`', 96], ['·', 183], ['«', 171], ['»', 187], ['¼', 188], ['½', 189], ['¾', 190], ['‚', 8218], ['‘', 8216], ['„', 8222], ['“', 8220], ['…', 8230], ['€', 8364], ['ﬀ', 64256], ['ﬁ', 64257], ['ﬂ', 64258], ['ﬃ', 64259], ['c_k.liga', 993082], ['Q_u.liga', 993083], ['s_s.liga', 993084], ['e_i.liga', 993085], ['t_t.liga', 993086], ['a.ss01', 993070], ['a.ss02', 993071], ['d.ss01', 993072], ['e.ss01', 993073], ['e.ss02', 993074], ['i.ss01', 993075], ['m.ss01', 993076], ['n.ss01', 993077], ['o.ss01', 993078], ['r.ss01', 993079], ['s.ss01', 993080], ['t.ss01', 993081]]
elif version == 2:
  glyphsUTF8 = [['A', 65], ['B', 66], ['C', 67], ['D', 68], ['E', 69], ['F', 70], ['G', 71], ['H', 72], ['I', 73], ['J', 74], ['K', 75], ['L', 76], ['M', 77], ['N', 78], ['O', 79], ['P', 80], ['Q', 81], ['R', 82], ['S', 83], ['T', 84], ['U', 85], ['V', 86], ['W', 87], ['X', 88], ['Y', 89], ['Z', 90], ['Ä', 196], ['Ö', 214], ['Ü', 220], ['ẞ', 7838], ['a', 97], ['b', 98], ['c', 99], ['d', 100], ['e', 101], ['f', 102], ['g', 103], ['h', 104], ['i', 105], ['j', 106], ['k', 107], ['l', 108], ['m', 109], ['n', 110], ['o', 111], ['p', 112], ['q', 113], ['r', 114], ['s', 115], ['t', 116], ['u', 117], ['v', 118], ['w', 119], ['x', 120], ['y', 121], ['z', 122], ['ä', 228], ['ö', 246], ['ü', 252], ['ß', 223], ['1', 49], ['2', 50], ['3', 51], ['4', 52], ['5', 53], ['6', 54], ['7', 55], ['8', 56], ['9', 57], ['0', 48], ['!', 33], ['?', 63], ['§', 167], ['$', 36], ['%', 37], ['&', 38], ['/', 47], ['(', 40], [')', 41], ['{', 123], ['}', 125], ['[', 91], [']', 93], ['=', 61], ['<', 60], ['>', 62], ['|', 124], ['\\', 92], [',', 44], [';', 59], ['*', 42], ['.', 46], [':', 58], ['-', 45], ['–', 8211], ['#', 35], ['+', 43], ['~', 126], ['"', 34], ["'", 39], ['@', 64], ['^', 94], ['_', 95], ['`', 96], ['·', 183], ['«', 171], ['»', 187], ['¼', 188], ['½', 189], ['¾', 190], ['‚', 8218], ['‘', 8216], ['„', 8222], ['“', 8220], ['…', 8230], ['€', 8364], ['ﬀ', 64256], ['ﬁ', 64257], ['ﬂ', 64258], ['ﬃ', 64259], ['c_k.liga', 993082], ['Q_u.liga', 993083], ['s_s.liga', 993084], ['e_i.liga', 993085], ['t_t.liga', 993086], ['a.ss01', 993070], ['a.ss02', 993071], ['d.ss01', 993072], ['e.ss01', 993073], ['e.ss02', 993074], ['i.ss01', 993075], ['m.ss01', 993076], ['n.ss01', 993077], ['o.ss01', 993078], ['r.ss01', 993079], ['s.ss01', 993080], ['t.ss01', 993081], ['copyright', 0xa9], ['registered', 0xae], ['logicalnot', 0xac], ['paragraph', 0xb6], ['divide', 0xf7], ['multiply', 0xd7], ['uni203d', 0x203d], ['arrowright', 0x2192], ['arrowleft', 0x2190], ['long', 0x17f]]

# grobe Überprüfung, ob soviele SVG-Dateien da sind,
# wie im Font platziert werden sollen.
if len(glyphsSVG) == len(glyphsUTF8):
    print('könnte passen ... los gehts!')
elif len(glyphsSVG) != len(glyphsUTF8):
    print('ungleiche Ausgangslage!')
    exit()

# Font-Erstellung + einige Einstellungen.
font = fontforge.font()
font.encoding = 'UnicodeFull'
font.version = '1.0'
font.weight = 'Regular'
font.fontname = name + '-Regular'
font.familyname = name
font.fullname = name + ' Regular'
# font.ascent = ##864
# font.descent = ##144
font.comment = 'FONT_COMMENT'
font.copyright = 'FONT_LICENSE'

font.em = 2048

font.layers[0].is_quadratic = 0
font.layers[1].is_quadratic = 0

font.addLookup('"ss01" Style Set 1 lookup', 'gsub_single', 1, [[b'ss01', [[b'latn', [b'dflt']],]],],)
font.addLookupSubtable('"ss01" Style Set 1 lookup', 'ss01')

font.addLookup('"ss02" Style Set 2 lookup', 'gsub_single', (), [[b'ss02', [[b'latn', [b'dflt']]]]])
font.addLookupSubtable('"ss02" Style Set 2 lookup', 'ss02')

font.addLookup('ligatures', 'gsub_ligature', (), [[b'liga', [[b'latn', [b'dflt']]]]])
font.addLookupSubtable('ligatures', 'liga')

font.addLookup('extra-ligatures', 'gsub_ligature', (), [[b'dlig', [[b'latn', [b'dflt']]]]])
font.addLookupSubtable('extra-ligatures', 'dlig')


# weitere ausprobieren
# https://github.com/fontforge/fontforge/issues/2988

# Ein paar Leerzeichen.
# NUL, Default Character
char = font.createChar( 0x0 )
char.width = 390
# C0 COntrol Character
char = font.createChar( 0xd, 'CR' )
char.width = 390
# Space
char = font.createChar( 0x20, 'space' )
char.width = 390
# NO-Break Space
char = font.createChar( 0xa0, 'uni00A0' )
char.width = 390
# Figure Space
char = font.createChar( 0x2007, 'uni2007' )
char.width = 1000
# Punctuation Space
char = font.createChar( 0x2008, 'uni2008' )
char.width = 390
# Thin Space
char = font.createChar( 0x2009, 'uni2009' )
char.width = 200
# Hair Space
char = font.createChar( 0x200a, 'uni200A' )
char.width = 100
# Zero Width Space
char = font.createChar( 0x200b, 'uni200B' )
char.width = 10
# Narrow NO-Break Space
char = font.createChar( 0x202f, 'uni202F' )
char.width = 390

# Glyphen platzieren
for i, f in enumerate(glyphsSVG):
    if glyphsUTF8[i][1] < 993000:
        char = font.createChar( glyphsUTF8[i][1] )
    elif glyphsUTF8[i][1] > 993000:
        char = font.createChar( glyphsUTF8[i][1], glyphsUTF8[i][0] )
    char.importOutlines(f)
    char.simplify()
    char.left_side_bearing = char.right_side_bearing = 48
    char.round()
    char.addExtrema()

# Konturen der Katzenpfoten ... und damit eine Möglichkeit
# des Einbettens von Zeicheninformationen im Skript
contour01 = [[5300.34, 1036.19],
[5320.85, 1019.84, 5347.91, 992.853, 5338.59, 953.574], [5325.98, 900.205, 5264.84, 868.537, 5193.96, 870.44], [5133.45, 872.166, 5081.55, 897.599, 5055.28, 938.638], [5026.91, 983.048, 5057.27, 1029.44, 5092.14, 1050.5], [5153.45, 1087.86, 5250.42, 1076.07, 5300.34, 1036.19]]

contour02 = [[5195.38, 1327.65], [5255.78, 1328.83, 5321.01, 1297.07, 5305.5, 1232.8], [5291.16, 1172.89, 5227.5, 1125.67, 5148.11, 1117.32], [5084.16, 1110.6, 5010.56, 1144.02, 5019.55, 1202.75], [5031.1, 1278.14, 5117.42, 1325.81, 5195.38, 1327.65]]

contour03 = [[5064.52, 857.56], [5108.5, 831.579, 5158.82, 763.1, 5101.08, 714.075], [5020.6, 645.417, 4842.01, 716.914, 4857.13, 813.681], [4869.43, 897.886, 5000.01, 895.218, 5064.52, 857.56]]

contour04 = [[4917.68, 1456.77], [4986.21, 1474.46, 5056.17, 1448.3, 5044.79, 1375.9], [5035.08, 1310.39, 4959.98, 1256.1, 4889.12, 1250.94], [4829.01, 1246.79, 4779.39, 1279.52, 4791.29, 1335.62], [4804.87, 1397.65, 4857.47, 1441.32, 4917.68, 1456.77]]

contour05 = [[4908.21, 966.015], [4877.98, 908.501, 4771.38, 802.499, 4682.57, 770.841], [4624.39, 750.075, 4581.83, 782.293, 4576.26, 835.201], [4574.22, 854.653, 4576.22, 865.482, 4591.15, 913.988], [4620.39, 1008.83, 4607.97, 1034.68, 4571.12, 1107.96], [4551.29, 1147.38, 4545.49, 1162.46, 4541.3, 1185.06], [4531.02, 1238.7, 4571.51, 1275.11, 4613.3, 1279.51], [4627.5, 1281, 4664.7, 1276.1, 4693.07, 1269.07], [4735.43, 1258.68, 4778.97, 1240.45, 4821.67, 1215.38], [4896.71, 1171.47, 4960.91, 1066.09, 4908.21, 966.015]]

# Eine Pfote
contours = []
contours.append(contour01)
contours.append(contour02)
contours.append(contour03)
contours.append(contour04)
contours.append(contour05)

# Erstellen der Einzelpfote als Zeichen
pfote = font.createChar(0xF273F, "pfote")
pfote.comment = u'Gerne den Vorschlag von Christine Fraunhofer hier umgesetzt!'
pen = pfote.glyphPen();

for i, cnts in enumerate(contours):
    for x, cnt in enumerate(cnts):
        if x == 0:
            pen.moveTo( cnt[0], cnt[1] )
        else:
            pen.curveTo( (cnt[0], cnt[1]), (cnt[2], cnt[3]), (cnt[4], cnt[5]) )
            if x == ( len(cnts) -1 ):
                pen.closePath()
pen = None

# Nun Einzelpfote kopieren, drehen ändern und ein weiteres Zeichen erstellen.
pfote.left_side_bearing = pfote.right_side_bearing = 120
t1 = psMat.compose(psMat.rotate(math.radians(2)), psMat.translate(0, -50))
t2 = psMat.compose(psMat.scale(0.95), psMat.translate(-1500, -500))
t3 = psMat.compose(psMat.scale(0.9), psMat.translate(-3000, -100))
t4 = psMat.compose(psMat.scale(0.85), psMat.translate(-4500, -600))
pfotelig = font.createChar(0xF2740, 'pfote.lig')
pfotelig.addReference("pfote", t1)
pfotelig.addReference("pfote", t2)
pfotelig.addReference("pfote", t3)
pfotelig.addReference("pfote", t4)
pfotelig.unlinkRef
pfotelig.left_side_bearing = pfotelig.right_side_bearing = 240
pfotelig.comment = u'Hier wurde die Pfote aus "pfote" übernommen, vervielfältigt und transformiert.'

# Weitere Methode zur Einbettung eines Zeichens:
# SVG inline + tempfile
svg_notdef = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg  PUBLIC "-//W3C//DTD SVG 1.1//EN"  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" viewBox="0 -410 1437 2048" xmlns="http://www.w3.org/2000/svg">
<g transform="matrix(1 0 0 -1 0 1638)">
<path d="m120 1609h1197v-1990h-1197v1990zm771-818c-19.146 0-35.663-6.9688-48.204-19-16.226-15.566-25.796-39.608-25.796-68 0-19 5-37 14-52 14.526-23.042 31.06-42.069 54-55.322 22.856-13.205 52.073-20.678 92-20.678h243c5 8 48 26 48 35 0 0.15332-129-5-129-5l-1 1-204 862c39.008 0 115.19 4.3369 118 24h-91c-169 0-297 11-447 11-69.382 0-124.94-33.19-163-74.565-26.673-28.993-44.76-62.006-53-90.435-9-37-13-72-13-111 0-120.28 73-209.13 73-317 0-8-1-16-1-23-6-50-41-142-63-142-1 0-3 0-4 1 0 1 4 17 4 32 0 29.87-27.211 45-51 45-32.613 0-55-31.419-55-61v-4c3.6914-30.763 33.041-55 63-55 43.703 0 87.129 23.289 124 55.122 33.154 28.624 61.009 64.156 79 95.878 7 18 10 31 10 45 0 5 1 10 0 16-3.4043 22.981-11.699 44.83-22.648 66-14.214 27.48-32.901 53.817-51.173 80-33.801 48.436-66.179 96.346-66.179 150 0 5 3 7 5 7 8.1768 0 19.186-48.815 26-65 6.6504-16.151 21.424-49.677 42.499-86 16.178-27.883 36.069-57.414 58.849-82 10.016-10.81 20.59-20.663 31.652-29 17.163-14.043 35.68-17.807 54-20.998 16.904-2.9453 33.644-5.4043 49-15.002v15c0 35-14 72-34 97-16.056 20.219-31.443 35.644-46 47.926-18.846 15.901-36.297 26.536-52 35.486-33.358 19.014-58.826 30.427-73 68.588-17 49-20 55-26 78-1 2-1 3-1 4 0 2 1 3 3 3 27-34 53-45 76-45 44.057 0 96 45.034 96 79 0 3-1 5-4 6-18-21-41-31-62-31-18.748 0-34.352 7.8623-46.034 20-15.385 15.984-23.966 39.382-23.966 62 0 23 8 48 26 73 21 28 43 40 76 40-11-27-28-60-28-88 0-40.121 37.28-60 74-60 60.208 0 98 58.732 98 105v9c0 1-1 0-1 0-6 0-26-33-26-33-9-17-34-35-55-35-29.096 0-40 32.585-40 59 0 17.711 3.4394 41 19 41 59.522 0 136.8-4 203-4l-11-42c-4.5752-17.156-21.36-34.749-40.38-53-13.85-13.289-28.885-26.928-41.252-41-15.197-17.291-26.368-35.238-26.368-54v-6c0-29 14-52 50-52h6l-34-174-54 73c-4 4-5 7-5 11 0 11 12 24 12 41 0 29.261-33.666 54-58 54h-3c-15.488 0-32.508-5.2676-46-14.77-14.552-10.249-25-25.424-25-44.23 0-13.622 4.0234-28.9 11.265-41 7.6426-12.772 18.871-22 32.735-22 14.412 0 24.504-1.7451 32-4.7314 18.509-7.375 21.188-22.321 34-37.269 18-22 56-71 56-71l-32-107c-5.998-17.112-13.023-30.365-20.73-41-16.259-22.438-35.549-33.22-54.623-44-23.132-13.074-45.946-26.146-62.648-60 35 4 56 11 73 11 19.643 0 30-16.54 30-37 0-25-18-46-36-60-42-34-84-44-157-75 1.5391 0.03125 202.74 2 275 2 20.139 0 38.683 4.4248 55 12.301 20.715 10 37.84 25.562 50.077 44.699 13.384 20.927 20.923 46.128 20.923 73 0 29.999-11.199 55.33-29.485 71-12.592 10.79-28.544 17-46.515 17h-1c-10 0-20-2-30-5-13 15-23 31-23 52 0 8 1 16 5 26l19 68 68-102c8-9 14-15 21-15s15 7 26 26l104 195 51-265c-15 9-32 14-48 14zm-6 676l195-856h-60l-171 856h36zm-117 0h34l37.977-184 10.32-50 15.48-75 7.2236-35-13.274-25-20.177-38-26.549-50-97 141 11 61c12-2 22-4 31-4 35 0 46 21 46 50v3c0 26.951-16.106 62.152-28.13 96-7.1592 20.155-12.87 39.831-12.87 57v8zm-64-382l84-121-33-60-69 95zm-92-402c0 28.731 11.707 48 40 48 14 0 30-7 48-22-5 19-7 47-18 60 5 1 9 1 13 1h2c15.94 0 27.386-5.2881 34.744-16 6.9522-10.12 10.256-25.082 10.256-45 0-14-4-19-9-30-7.9707 11.07-18.883 17.827-31 21.92-15.246 5.1484-32.399 6.0801-48 6.0801-7 0-13 1-19 0 43-18 60-32 60-66 0-15-23-27-40-27-31.975 0-43 40.368-43 69zm293 86c12 0 24-4 37-11l8-51c-12 0-23 2-34 2-22 0-42-7-59-30-5 10-8 15-8 28v2c0 17.639 7.4463 34.63 19.76 46 9.3272 8.6123 21.448 14 35.24 14h1zm34-77c4 0 8 0 13-1l11-80h-4c-18.746 0-40.073 4.1953-55 11.852-11.351 5.8223-19 13.646-19 23.148v5c0 11.568 4.4248 22.308 14 29.891 8.6338 6.8379 21.456 11.109 39 11.109h1z" fill="currentColor"/>
</g>
</svg>'''

temp = tempfile.NamedTemporaryFile(suffix=".svg", mode="w+t")
temp.writelines( svg_notdef )
temp.seek(0)
gl_notdef = font.createChar(0x25A1, '.notdef')
gl_notdef.importOutlines( temp.name )
gl_notdef.left_side_bearing = gl_notdef.right_side_bearing = 90

# Stylistic Sets, normale und besondere Ligaturen.
# ss01
char = font.createChar(0x61)
char.addPosSub('ss01', 'a.ss01')
char = font.createChar(0x64)
char.addPosSub('ss01', 'd.ss01')
char = font.createChar(0x65)
char.addPosSub('ss01', 'e.ss01')
char = font.createChar(0x69)
char.addPosSub('ss01', 'i.ss01')
char = font.createChar(0x6D)
char.addPosSub('ss01', 'm.ss01')
char = font.createChar(0x6E)
char.addPosSub('ss01', 'n.ss01')
char = font.createChar(0x6F)
char.addPosSub('ss01', 'o.ss01')
char = font.createChar(0x72)
char.addPosSub('ss01', 'r.ss01')
char = font.createChar(0x73)
char.addPosSub('ss01', 's.ss01')
char = font.createChar(0x74)
char.addPosSub('ss01', 't.ss01')

# ss02
char = font.createChar(0x61)
char.addPosSub('ss02', 'a.ss02')
char = font.createChar(0x65)
char.addPosSub('ss02', 'e.ss02')

# liga
char = font.createChar(64256)
char.addPosSub('liga', tuple(['f', 'f']))
char = font.createChar(64257)
char.addPosSub('liga', tuple(['f', 'i']))
char = font.createChar(64258)
char.addPosSub('liga', tuple(['f', 'l']))
char = font.createChar(64259)
char.addPosSub('liga', tuple(['f', 'f', 'i']))
pfotelig.addPosSub('liga', tuple(['S', 'a', 'm', 't', 'p', 'f', 'o', 't', 'e']))

# dlig
char = font.createChar(0xF273A)
char.addPosSub('dlig', tuple(['c', 'k']))
char = font.createChar(0xF273B)
char.addPosSub('dlig', tuple(['Q', 'u']))
char = font.createChar(0xF273C)
char.addPosSub('dlig', tuple(['s', 's']))
char = font.createChar(0xF273D)
char.addPosSub('dlig', tuple(['e', 'i']))
char = font.createChar(0xF273E)
char.addPosSub('dlig', tuple(['t', 't']))

# Hier der Versuch bestimmte durchschnittliche Annahmen über die Zeichengrößen
# automagisch umzusetzen.
# get Font-Spezifika
fEm = font.em
fDesc = font.descent
fAsc = font.ascent

# set Font-Spezifika
xHeight = round((fAsc/1.9),1)
baseToX = xHeight
baseToMax = round((fAsc/1.03),1)
baseToMaxLess = round((fAsc/1.09),1)
baseMin = round((fDesc/1.08),1)
minToX = baseMin + xHeight
minToMax = baseMin + baseToMax
minToMaxLess = baseMin + baseToMaxLess

baseToMaxGlyphs = ["exclam", "numbersign", "dollar", "percent", "ampersand", "parenleft", "parenright", "slash", "question",  "A", "B", "C", "D", "E", "F", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "bracketleft", "backslash", "bracketright", "braceleft", "bar", "braceright", "section", "Adieresis", "Odieresis", "Udieresis", "Euro", "Q_u.liga"]

baseToXGlyphs = ["at", "a", "c", "e", "i", "m", "n", "o", "r", "s", "u", "v", "w", "x", "z", "adieresis", "odieresis", "udieresis", "a.ss01", "a.ss02", "e.ss01", "e.ss02", "i.ss01", "m.ss01", "n.ss01", "o.ss01", "r.ss01", "s.ss01", "s_s.liga", "e_i.liga"]

baseToMaxLessGlyphs = ["b", "d", "h", "k", "l", "t", "onequarter", "onehalf", "threequarters", "d.ss01", "t.ss01", "c_k.liga", "t_t.liga", "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

minToXGlyphs = ["g", "j", "p", "q", "y"]

minToMaxLessGlyphs = ["f", "germandbls", "uniFB00", "uniFB01", "uniFB02", "uniFB03"]

adjustGlyphs = []
adjustGlyphs.append( baseToMaxGlyphs )
adjustGlyphs.append( baseToXGlyphs )
adjustGlyphs.append( baseToMaxLessGlyphs )
adjustGlyphs.append( minToXGlyphs )
adjustGlyphs.append( minToMaxLessGlyphs )

for i, glyphs in enumerate( adjustGlyphs ):
    for j, glyph in enumerate( glyphs ):
        # jeweiliges Zeichen
        gl = font[ glyph ]
        # Koordinaten des Zeichens
        glBox = gl.boundingBox()
        (xMin, yMin, xMax, yMax) = gl.boundingBox()
        xMin = round( xMin, 1 )
        yMin = round( yMin, 1 )
        xMax = round( xMax, 1 )
        yMax = round( yMax, 1 )
        # Versatz von jeweiliger Grundlinie
        if i == 0:
            glToBase = -yMin -15
            glToHeight = round((baseToMax / (yMax - yMin)),1)
            baseAndScale = psMat.compose(psMat.translate( 0, glToBase ), psMat.scale( glToHeight ))
        elif i == 1:
            glToBase = -yMin -15
            glToHeight = round((baseToX / (yMax - yMin)),1)
            baseAndScale = psMat.compose(psMat.translate( 0, glToBase ), psMat.scale( glToHeight ))
        elif i == 2:
            glToBase = -yMin -15
            glToHeight = round((baseToMaxLess / (yMax - yMin)),1)
            baseAndScale = psMat.compose(psMat.translate( 0, glToBase ), psMat.scale( glToHeight ))
        elif i == 3:
            glToHeight = round((minToX / (yMax - yMin)),1)
            negCorr = psMat.translate( 0, -yMin );
            baseAndScale = psMat.compose(negCorr, psMat.compose(psMat.scale( glToHeight ), psMat.translate( 0, -baseMin )))
        elif i == 4:
            glToHeight = round((minToMaxLess / (yMax - yMin)),1)
            negCorr = psMat.translate( 0, -yMin );
            baseAndScale = psMat.compose(negCorr, psMat.compose(psMat.scale( glToHeight ), psMat.translate( 0, -baseMin )))
        gl.transform( baseAndScale )
        gl.left_side_bearing = gl.right_side_bearing = 48

# tidy
font.selection.all()
font.correctDirection()
font.removeOverlap()
font.simplify()
font.round()
font.addExtrema()

# Ausgabe
font.save(pfad + name + "-Regular.sfd")
# font.generate(pfad + name + "-Regular.otf")

font.close()
