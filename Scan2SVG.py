# -*- coding: utf-8 -*-

from PIL import Image
import cv2 as cv
import os
import glob
import subprocess
import argparse

ap = argparse.ArgumentParser(description='Umwandlung jpg@600dpi in SVG-Dateien zum weiteren Import in FontForge.')
ap.add_argument("-t", "--threshold", help="Schwellwert (1--255).", type=int, required=True)
ap.add_argument("-A", "--blattA", help="Blatt A", required=False, type=str)
ap.add_argument("-B", "--blattB", help="Blatt B", required=False, type=str)
ap.add_argument("-C", "--blattC", help="Blatt C", required=False, type=str)
ap.add_argument("-p", "--pattern", help="Namensaufbau für Output-Dateien.", required=True, type=str)
ap.add_argument("-o", "--output", help="Zielordner", required=True, type=str)
ap.add_argument("-n", "--name", help="Name der Schrift", required=False, type=str)
ap.add_argument("-v", "--version", help="Version des Eingabebogens.", required=False, type=int)
args = vars(ap.parse_args())

t = args["threshold"]
naming = args["pattern"]
pathWD = args["output"]
pathWD = pathWD.rstrip('/') + '/'
name = args["name"]
version = args["version"]

images_list = []
if args["blattA"]:
    images_list.append(args["blattA"])
else:
    images_list.append(False)
if args["blattB"]:
    images_list.append(args["blattB"])
else:
    images_list.append(False)
if args["blattC"]:
    images_list.append(args["blattC"])
else:
    images_list.append(False)

# Output-Pfad/Ordner anlegen
if not os.path.exists(pathWD):
    os.makedirs(pathWD)

for stepper, image_from_list in enumerate(images_list):

    if image_from_list == False:
        continue

    # Bild/Scan importieren
    img = cv.imread(image_from_list)
    #bild = img.copy()

    minHoehe = img.shape[0] * 0.06
    minBreite = img.shape[1] * 0.06
    minFlaeche = minHoehe * minBreite

    # Graustufen
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Blur
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    # sw/ws
    (t, binary) = cv.threshold(blur, t, 255, cv.THRESH_BINARY_INV)
    # Konturen finden lassen
    (contours, _) = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Konturen sortieren (links->rechts, oben->unten) !!! funktioniert nicht
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
        #print("i: ", i, "\nx: ", x, "\ny: ", y, "\nw: ", w, "\nh: ", h, "\n")
        # manuelle Korrektur:
        #y = y + 20 #x = x + 20 #h = h - 32 #w = w - 32
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
        # print("i: ", i, "\nx: ", tbs[0], "\ny: ", tbs[1], "\nw: ", tbs[2], "\nh: ", tbs[3], "\n")
        subImg = img[tbs[1] : tbs[1] + tbs[3], tbs[0] : tbs[0] + tbs[2], :]
        cv.imwrite(pathWD + naming + "-{:03}.jpg".format(i), subImg)

    # bild = cv.resize(img,None,fx=0.11,fy=0.11)
    # cv.imshow('Test',bild)
    # cv.waitKey(0)
    #exit(1)

filesJPG = [f for f in glob.glob(pathWD + "*.jpg")]

for f in filesJPG:
    bild = Image.open(f)
    new_name = pathWD + os.path.splitext(os.path.basename(f))[0] + '.ppm'
    bild.save(new_name,'ppm')

filesPPM = [f for f in glob.glob(pathWD + "*.ppm")]

def potrace(input_fname, output_fname):
    subprocess.check_call(['potrace', '--flat', '-s', input_fname, '-o', output_fname])

for f in filesPPM:
    new_name = pathWD + os.path.splitext(os.path.basename(f))[0] + '.svg'
    potrace(f, new_name)

for rmJPG in filesJPG:
    os.remove(rmJPG)

for rmPPM in filesPPM:
    os.remove(rmPPM)

print('Dateien aus Scan extrahiert und umgewandelt.')

if name and version:
    print('Nun wird noch der font erstellt ...')
    subprocess.check_call(["python2", "SVG2Font.py", "--name", name, "--version", str(version), "--svgordner", pathWD])
    print("fertig!")
    print("...")
    print("* im Ordner: " + pathWD + "liegt: " + name + "-Regular.sfd")
    print("* Version " + version + " des Eingabebogens wurde verwendet")
    print("* Schriftname: " + name)
    print("...")
    print("Viel Vergnügen bei den weiteren Schrifterstellungsschritten.")
