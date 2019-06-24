#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Umwandlung von vorliegenden Bildern in Vektorbilder der Einzelglyphen (bzw. in einen Font).

Entweder über den Aufruf dieser Datei (`Scan2SVG.py`) auch den zweiten Schritt der Font-Erstellung mitbestimmen, oder aber nur dieses Skript verwenden für die Vektorisierung und `SVG2Font.py` nachher manuell starten.
"""

import os
import glob
import subprocess
import argparse
import cv2 as cv
from PIL import Image
import numpy as np
from skimage.morphology import square
from skimage.morphology import skeletonize as skl
from skimage.morphology import dilation as dil

__author__ = "Christoph Pfeiffer"
__license__ = "CC-BY-NC-SA-4.0"

ap = argparse.ArgumentParser(description='Umwandlung jpg@600dpi in SVG-Dateien zum weiteren Import in FontForge.')
ap.add_argument("-t", "--threshold", help="Schwellwert (1--255).", default=160, type=int, required=False)
ap.add_argument("-a", "--blattA", help="Blatt A", required=False, type=str)
ap.add_argument("-b", "--blattB", help="Blatt B", required=False, type=str)
ap.add_argument("-c", "--blattC", help="Blatt C", required=False, type=str)
ap.add_argument("-s", "--scans", help="Ordner mit per Namen sortierten Scans (*.jpg)", required=False, type=str)
ap.add_argument("--blur", help="Weichzeichner", default=3, required=False, type=int)
ap.add_argument("-o", "--output", help="Zielordner", required=False, type=str)
ap.add_argument("-n", "--name", help="NameDerSchrift", required=False, type=str)
ap.add_argument("-v", "--version", help="Version des Eingabebogens.", default=2, required=False, type=int)
ap.add_argument("--rmppm", help="PPM-Dateien löschen.", action="store_true")
ap.add_argument("--rmjpg", help="JPG-Dateien löschen.", action="store_true")
ap.add_argument("--rmsvg", help="SVG-Dateien löschen.", action="store_true")
ap.add_argument("--skel", help="Skeletonization! Extra Font.", action="store_true")
ap.add_argument("--buntstift", help="Buntstift, Farbe, uneinheitliche Deckkraft.", action="store_true")
ap.add_argument("--debug", help="Debug-Informationen.", action="store_true")

args = ap.parse_args()

t = args.threshold

name = args.name
blurring = args.blur
version = args.version
pot_buntstift = args.buntstift
show_debug = args.debug
do_skelet = args.skel

if args.scans :
    sortedDir = args.scans
    sortedDir = sortedDir.rstrip('/') + '/'

if args.output :
    pathWD = args.output
    pathWD = pathWD.rstrip('/') + '/'
elif args.scans :
    pathWD = sortedDir + 'FONT/'
else :
    print('Keine Ordnerinformationen angegeben.')
    exit()

pathWDSKEL = pathWD + 'SKEL/'

def get_contour_precedence(contour, cols) :
    tolerance_factor = 300
    origin = cv.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

kern = cv.getStructuringElement(cv.MORPH_RECT,(11,11))

if sortedDir :
    filesSortedDir = [f for f in glob.glob(sortedDir + "*.jpg")]
    filesSortedDir.sort()
    images_list = filesSortedDir

if images_list == None :
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

if not os.path.exists(pathWD):
    os.makedirs(pathWD)

for stepper, image_from_list in enumerate(images_list):
    if image_from_list == False:
        continue

    img = cv.imread(image_from_list)

    minHoehe = img.shape[0] * 0.06
    minBreite = img.shape[1] * 0.06
    minFlaeche = minHoehe * minBreite

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    (_, binary) = cv.threshold(blur, t, 255, cv.THRESH_BINARY_INV)
    binary = cv.morphologyEx(binary, cv.MORPH_CLOSE, kern)

    (contours, _) = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    hand2FontBoxes = []
    for i, contour in enumerate(contours) :
        if 5000 < cv.contourArea(contour) :
            approx = cv.approxPolyDP(contour,0.01*cv.arcLength(contour,True),True)
            if len(approx) == 4 and cv.contourArea(contour) > minFlaeche :
                hand2FontBoxes.append(contour)
                #cv.drawContours(img, contour, -1, (0, 0, 255), 10)
                #cv.fillPoly(img, pts =[contour], color=(133, 160, 22))

    hand2FontBoxes.sort(key=lambda x:get_contour_precedence(x, img.shape[1]))

    ## debug
    #for i, cnt in enumerate(hand2FontBoxes) :
    #    # compute the center of the contour
    #    M = cv.moments(cnt)
    #    cX = int(M["m10"] / M["m00"])
    #    cY = int(M["m01"] / M["m00"])
    #    cv.putText(img, str(i), (cX - 60, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 10)

    # debug einbauen!
    #BILDA = cv.resize(BILD.copy(),None,fx=0.14,fy=0.14)
    #cv.imshow('BLaBLaBLa',BILDA)
    #cv.waitKey(0)

    targetBoxList = []
    for i, box in enumerate(hand2FontBoxes):
        x, y, w, h = cv.boundingRect(box)
        # debug
        #print("i: ", i, "\nx: ", x, "\ny: ", y, "\nw: ", w, "\nh: ", h, "\n")

        # manuelle Korrektur bzgl. Inhalt der Box:
        y = int(round(y + (0.0433 * h)))
        x = int(round(x + (0.0433 * h)))
        h = int(round(h - (0.0693 * h)))
        w = int(round(w - (0.0693 * h)))
        boxInner = x, y, w, h
        targetBoxList.append(boxInner)

    if stepper == 0:
        blattCounter = 1
    elif stepper == 1:
        blattCounter = 50
    elif stepper == 2:
        blattCounter = 99

    for i, tbs in enumerate(targetBoxList, blattCounter):
        # debug
        # print("i: ", i, "\nx: ", tbs[0], "\ny: ", tbs[1], "\nw: ", tbs[2], "\nh: ", tbs[3], "\n")
        subImg = img[tbs[1] : tbs[1] + tbs[3], tbs[0] : tbs[0] + tbs[2], :]
        if blurring :
            subImg = cv.GaussianBlur(subImg, ( blurring , blurring ), 0)
        cv.imwrite(pathWD + name + "-{:03}.jpg".format(i), subImg)

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
    if pot_buntstift:
        subprocess.check_call(['potrace', '--flat', '--longcurve', '--alphamax', '1.34', '--turdsize', '120', '--blacklevel', '0.95', '-s', input_fname, '-o', output_fname])
    else:
        subprocess.check_call(['potrace', '--flat', '--turdsize', '120', '-s', input_fname, '-o', output_fname])

for f in filesPPM:
    new_name = pathWD + os.path.splitext(os.path.basename(f))[0] + '.svg'
    potrace(f, new_name)



# if `--skel`
if args.skel :
    if not os.path.exists(pathWDSKEL):
        os.makedirs(pathWDSKEL)

    filesJPG = [f for f in glob.glob(pathWD + "*.jpg")]
    for f in filesJPG:
        path = f
        skelimg = cv.imread(path, 0)
        skelimg = cv.bilateralFilter(skelimg, 5, 35, 10)
        skelimg = cv.GaussianBlur(skelimg, (19, 19), 5)

        th = cv.adaptiveThreshold(skelimg, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 35, 11)
        th = cv.bitwise_not(th)

        kernel = np.array([[0, 1, 1],
                           [0, 1, 0],
                           [1, 1, 0]], dtype='uint8')

        th = cv.morphologyEx(th, cv.MORPH_CLOSE, kernel)

        th = th == 255
        th = skl(th)
        th = th.astype(np.uint8)*255
        th = dil(th, square(9))
        th = cv.bitwise_not(th)
        new_name = pathWDSKEL + os.path.splitext(os.path.basename(f))[0] + '.jpg'
        cv.imwrite(new_name, th)

    # JPG nach PPM konvertieren
    filesJPG = [f for f in glob.glob(pathWDSKEL + "*.jpg")]
    for f in filesJPG:
        bild = Image.open(f)
        new_name = pathWDSKEL + os.path.splitext(os.path.basename(f))[0] + '.ppm'
        bild.save(new_name,'ppm')

    # PPM nach SVG konvertieren
    filesPPM = [f for f in glob.glob(pathWDSKEL + "*.ppm")]
    def potrace(input_fname, output_fname):
        if pot_buntstift:
            subprocess.check_call(['potrace', '--flat', '--longcurve', '--alphamax', '1.34', '--turdsize', '120', '--blacklevel', '0.95', '-s', input_fname, '-o', output_fname])
        else:
            subprocess.check_call(['potrace', '--flat', '--turdsize', '120', '-s', input_fname, '-o', output_fname])

    for f in filesPPM:
        new_name = pathWDSKEL + os.path.splitext(os.path.basename(f))[0] + '.svg'
        potrace(f, new_name)



print('Zeichen aus Scan extrahiert und vektorisiert.')

# falls `name` und `version` als Argument gegeben sind wird dann auch noch die Umwandlung in einen Font angegangen (`SVG2Font.py` mit Argumenten aufgerufen)
if name and version:
    print('\nNun wird der Font erstellt, \nda --name und --version angegeben wurden:')
    subprocess.check_call(["python2", "SVG2Font.py", "--name", name, "--version", str(version), "--svgordner", pathWD])
    print("... fertig!\n")
    print("* Erfassungsbogen in Version: " + str(version))
    print("* Schriftname: " + name)
    print("* im Ordner: " + pathWD)
    print("* Dateiname: " + name + "-Regular.sfd")
    info_datei = open(pathWD + "info.txt", "a")
    info_datei.write(str(args))
    info_datei.close()

    if args.skel :
        print('\nNun wird der SKEL-Font erstellt, \nda --name und --version angegeben wurden:')
        subprocess.check_call(["python2", "SVG2Font.py", "--name", name, "--version", str(version), "--svgordner", pathWDSKEL])
        print("... fertig!\n")
        print("* Erfassungsbogen in Version: " + str(version))
        print("* Schriftname: " + name)
        print("* im Ordner: " + pathWDSKEL)
        print("* Dateiname: " + name + "-Regular.sfd")
        info_datei = open(pathWDSKEL + "info.txt", "a")
        info_datei.write(str(args))
        info_datei.close()

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
