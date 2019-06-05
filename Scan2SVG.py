#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Umwandlung von vorliegenden Bildern in Vektorbilder der Einzelglyphen (bzw. in einen Font).

Entweder über den Aufruf dieser Datei (`Scan2SVG.py`) auch den zweiten Schritt der Font-Erstellung mitbestimmen, oder aber nur dieses Skript verwenden für die Vektorisierung und `SVG2Font.py` nachher manuell starten.
"""

import os
import glob
import subprocess
import argparse
import cv2 as cv
from PIL import Image

__author__ = "Christoph Pfeiffer"
__license__ = "CC-BY-NC-SA-4.0"

ap = argparse.ArgumentParser(description='Umwandlung jpg@600dpi in SVG-Dateien zum weiteren Import in FontForge.')
ap.add_argument("-t", "--threshold", help="Schwellwert (1--255).", type=int, required=True)
ap.add_argument("-A", "--blattA", help="Blatt A", required=False, type=str)
ap.add_argument("-B", "--blattB", help="Blatt B", required=False, type=str)
ap.add_argument("-C", "--blattC", help="Blatt C", required=False, type=str)
ap.add_argument("-p", "--pattern", help="Namensaufbau für Output-Dateien.", required=True, type=str)
ap.add_argument("-o", "--output", help="Zielordner", required=True, type=str)
ap.add_argument("-n", "--name", help="Name der Schrift", required=False, type=str)
ap.add_argument("-v", "--version", help="Version des Eingabebogens.", required=False, type=int)
ap.add_argument("--rmppm", help="PPM-Dateien löschen.", action="store_true")
ap.add_argument("--rmjpg", help="JPG-Dateien löschen.", action="store_true")
ap.add_argument("--rmsvg", help="SVG-Dateien löschen.", action="store_true")

args = ap.parse_args()

t = args.threshold
naming = args.pattern
pathWD = args.output
pathWD = pathWD.rstrip('/') + '/'
name = args.name
version = args.version

images_list = []
if args.blattA:
    images_list.append(args.blattA)
else:
    images_list.append(False)
if args.blattB:
    images_list.append(args.blattB)
else:
    images_list.append(False)
if args.blattC:
    images_list.append(args.blattC)
else:
    images_list.append(False)

# Output-Pfad/Ordner ggfs. anlegen
if not os.path.exists(pathWD):
    os.makedirs(pathWD)

for stepper, image_from_list in enumerate(images_list):
    # falls Blatt {A,B,C}
    if image_from_list == False:
        continue
    # Bild/Scan importieren
    img = cv.imread(image_from_list)
    # debug
    #bild = img.copy()

    # Boxen haben ca. Min-/Max-Werte bzgl. DIN-A4.
    minHoehe = img.shape[0] * 0.06
    minBreite = img.shape[1] * 0.06
    minFlaeche = minHoehe * minBreite

    # Graustufen
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Blur
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    # invers
    (t, binary) = cv.threshold(blur, t, 255, cv.THRESH_BINARY_INV)
    # Konturen finden
    (contours, _) = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Konturen sortieren (links->rechts, oben->unten)
    # !!! funktioniert nicht immer, deswegen doch anderer Weg.
    sorted_contours = sorted(contours, key=lambda ctr: cv.boundingRect(ctr)[0] + cv.boundingRect(ctr)[1] * img.shape[1] )

    # was nun tun mit den Schachteln
    glyphBoxes = []
    for i, cnt in enumerate(sorted_contours):
        approx = cv.approxPolyDP(cnt,0.01*cv.arcLength(cnt,True),True)
        if len(approx) == 4 and cv.contourArea(cnt) > minFlaeche :
            glyphBoxes.append(cnt)

    targetBoxList = []
    for i, box in enumerate(glyphBoxes):
        x, y, w, h = cv.boundingRect(box)
        # debug
        #print("i: ", i, "\nx: ", x, "\ny: ", y, "\nw: ", w, "\nh: ", h, "\n")

        # manuelle Korrektur:
        y = int(round(y + (0.0433 * h)))
        x = int(round(x + (0.0433 * h)))
        h = int(round(h - (0.0693 * h)))
        w = int(round(w - (0.0693 * h)))
        boxInner = x, y, w, h
        targetBoxList.append(boxInner)

    targetBoxSort = sorted(targetBoxList, key=lambda item: ( item[0]+(item[2]/2), item[1]+(item[3]/2) ))

    if stepper == 0:
        blattCounter = 1
    elif stepper == 1:
        blattCounter = 50
    elif stepper == 2:
        blattCounter = 99

    for i, tbs in enumerate(targetBoxSort, blattCounter):
        # debug
        # print("i: ", i, "\nx: ", tbs[0], "\ny: ", tbs[1], "\nw: ", tbs[2], "\nh: ", tbs[3], "\n")
        subImg = img[tbs[1] : tbs[1] + tbs[3], tbs[0] : tbs[0] + tbs[2], :]
        cv.imwrite(pathWD + naming + "-{:03}.jpg".format(i), subImg)

    # debug
    #bild = cv.resize(img,None,fx=0.11,fy=0.11)
    #cv.imshow('Test',bild)
    #cv.waitKey(0)
    #exit(1)

# JPG nach PPM konvertieren
filesJPG = [f for f in glob.glob(pathWD + "*.jpg")]
for f in filesJPG:
    bild = Image.open(f)
    new_name = pathWD + os.path.splitext(os.path.basename(f))[0] + '.ppm'
    bild.save(new_name,'ppm')

# PPM nach SVG konvertieren
filesPPM = [f for f in glob.glob(pathWD + "*.ppm")]
def potrace(input_fname, output_fname):
    subprocess.check_call(['potrace', '--flat', '-s', input_fname, '-o', output_fname])
for f in filesPPM:
    new_name = pathWD + os.path.splitext(os.path.basename(f))[0] + '.svg'
    potrace(f, new_name)

print('Zeichen aus Scan extrahiert und vektorisiert.')

# falls `name` und `version` als Argument gegeben sind wird dann auch noch die Umwandlung in einen Font angegangen (`SVG2Font.py` mit Argumenten aufgerufen)
if name and version:
    print('Font wird erstellt, da --name und --version angebeben wurden ...')
    subprocess.check_call(["python2", "SVG2Font.py", "--name", name, "--version", str(version), "--svgordner", pathWD])
    print("... fertig!\n")
    print("* Erfassungsbogen in Version: " + str(version))
    print("* Schriftname: " + name)
    print("* im Ordner: " + pathWD)
    print("* Dateiname: " + name + "-Regular.sfd")

# tidy up
# ggfs. ppm-Dateien löschen
if args.rmppm:
    for rmPPM in filesPPM:
        os.remove(rmPPM)
    print("* " + str(len(filesPPM)) + " PPM-Dateien wurden gelöscht")

# ggfs. jpg-Dateien löschen
if args.rmjpg:
    for rmJPG in filesJPG:
        os.remove(rmJPG)
    print("* " + str(len(filesJPG)) + " JPG-Dateien wurden gelöscht")

# ggfs. svg-Dateien löschen
if args.rmsvg:
    filesSVG = [f for f in glob.glob(pathWD + "*.svg")]
    for rmSVG in filesSVG:
        os.remove(rmSVG)
    print("* " + str(len(filesSVG)) + " SVG-Dateien wurden gelöscht")
