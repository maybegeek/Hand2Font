import os
import glob
import cv2
import argparse

ap = argparse.ArgumentParser(description='DEBUG!!')
ap.add_argument('-s', '--scans', help='Ordner der Scans.', type=str, required=True)

args = ap.parse_args()

pfad = args.scans
pfad = pfad.rstrip('/') + '/'

def get_contour_precedence(contour, cols):
    tolerance_factor = 300
    origin = cv2.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

testBilder = [f for f in glob.glob( pfad + "*.jpg")]
for f in testBilder :
    img = cv2.imread(f)

    #cv2.putText(img, f, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 10)

    minHoehe = img.shape[0] * 0.06
    minBreite = img.shape[1] * 0.06
    minFlaeche = minHoehe * minBreite

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ## debug
    #img1 = cv2.resize(blur.copy(),None,fx=0.14,fy=0.14)
    #cv2.imshow('Test',img1)
    #cv2.waitKey(0)
    ## /debug
    (_, binary) = cv2.threshold(blur, 190, 255, cv2.THRESH_BINARY_INV)
    ## debug
    #img2 = cv2.resize(binary.copy(),None,fx=0.14,fy=0.14)
    #cv2.imshow('Test',img2)
    #cv2.waitKey(0)
    ## /debug
    #kern = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
    kern = cv2.getStructuringElement(cv2.MORPH_RECT,(11,11))
    #binary = cv2.dilate(binary, kern)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kern)
    ## debug
    #img3 = cv2.resize(binary.copy(),None,fx=0.14,fy=0.14)
    #cv2.imshow('Test',img3)
    #cv2.waitKey(0)
    ## /debug
    (contours, _) = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    hand2FontBoxes = []
    for i, contour in enumerate(contours) :
        if 5000 < cv2.contourArea(contour) :
            approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
            if len(approx) == 4 and cv2.contourArea(contour) > minFlaeche :
                hand2FontBoxes.append(contour)
                #cv2.drawContours(img, contour, -1, (0, 0, 255), 10)
                cv2.fillPoly(img, pts =[contour], color=(133, 160, 22))

    hand2FontBoxes.sort(key=lambda x:get_contour_precedence(x, img.shape[1]))



    for i, cnt in enumerate(hand2FontBoxes) :
        # compute the center of the contour
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.putText(img, str(i), (cX - 60, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 10)

    ## debug
    #print("Konturen insgesamt: " + str(len(contours)) )
    #print("Konturen passend: " + str(len(eigenecnt)) )

    img = cv2.resize(img,None,fx=0.14,fy=0.14)
    cv2.imshow('Test',img)
    cv2.waitKey(0)
