#!/usr/bin/python3

'''
===================================================================================================
  Author        : Emanuel Sánchez
  Company       : Universidad Simón Bolívar
  Email         : emanuelsab@gmail.com

  Description   :
                    Prueba1

===================================================================================================
'''

import argparse
import cv2
import numpy as np
import imutils
from sys import exit

def detector(c):
    circle_flag = False
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c, 0.8 * peri, True)

    if len(approx) != 3 or len(approx) != 4 or len(approx) != 5:
        circle_flag = True

    return circle_flag

def imgAcondition(img):
    # imgResized = imutils.resize(img, width = 300)     # resize the image to obtain a smaller perimeter and so a better factor to approximate the image

    ratio = 1
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ratio = img.shape[0] / float(imgResized.shape[0])
    # imgGray = cv2.cvtColor(imgResized, cv2.COLOR_BGR2GRAY)

    imgFilter = cv2.GaussianBlur(imgGray,(5,5),0)      # filter to eliminate gaussian noise and reduce textures
    imgThresh = cv2.threshold(imgFilter, 20, 255, cv2.THRESH_BINARY)[1]      # convert the image to a binary image to find contours
    return ratio, imgThresh, 0

def circlesDetector(frame, img, imgOriginal, ratio):
    contours = cv2.findContours(img.copy(), 1, 2)   # find external contours

    contours = contours[0] if imutils.is_cv2() else contours[1]

    cv2.drawContours(frame, contours, -1, (0,255,0), 2)

    # print(contours)
    # for c in contours:
    #     M = cv2.moments(c)
    #     try:
    #         cX = int((M["m10"] / M["m00"]) * ratio)
    #         cY = int((M["m01"] / M["m00"]) * ratio)
    #     except:
    #         cX = 0
    #         cY = 0
    #
    #     if(detector(c)):
    #         c.astype("float")
    #         c *= ratio
    #         c.astype("int")
    #         cv2.drawContours(frame, [c], -1, (0,255,0), 2)
    #         cv2.putText(frame, "Circle", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    return frame

def main():
    img = cv2.imread("img0.png")

    ratio, imgAconditioned, imgAux = imgAcondition(img)
    imgDetection = circlesDetector(img, imgAconditioned, imgAux, ratio)
    print((imgAconditioned))
    print((imgDetection))
    while(True):            # main loop to get images from camera continuously
        cv2.imshow('Webcam', np.hstack([imgAconditioned,imgDetection]))           # show the frame in a window
        # cv2.imshow('Detection', imgDetection)
        # cv2.imshow('Detection', imgAconditioned)
        if cv2.waitKey(1) & 0xFF==ord('q'):     # wait for q key to be pressed to end the loop
        	break

    cap.release()   # close comunication with cam
    cv2.destroyAllWindows()     # close all windows

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Este es un programa de Visión por cumputadora para la asignatura: Laboratorio de Proyectos III')
    parser.add_argument("-n", type=int,
                        help="# of clusters")
    parser.add_argument('-c', action='store_false', default=False,
                        dest='boolean_switch',
                        help='Run a clustering algorithm to observe the number of colors')
    parser.add_argument('-r', action='store_true', default=False,
                        dest='boolean_switch',
                        help='Run the software')
    args = parser.parse_args()
    if not(args.boolean_switch):
        #print(pcolors.OKBLUE + "\nMODO: Algoritmo de Agrupación" + pcolors.ENDC)
        assert args.n != 0, "Invalid number of clusters"
        clustering_algorithm()
    else:
        #print(pcolors.OKBLUE + "\nCorriendo el Programa..." + pcolors.ENDC)
        main()
