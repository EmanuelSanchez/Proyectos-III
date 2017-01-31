'''
===================================================================================================
  Author        : Emanuel Sánchez
  Company       : Universidad Simón Bolívar
  Email         : emanuelsab@gmail.com

  Description   :
  Prgoram to detec circles and then verify they colors

===================================================================================================
'''

import argparse
import cv2
import numpy as np
import imutils
#from sklearn.cluster import KMeans
#import kmeans
from sys import exit

# list of colors to detect:
# [lower limit], [upper limit]
# [R,G,B]
# boundaries = [
# 	([0, 10, 80], [70, 70, 255]),        # blue
#     #([17, 15, 100], [50, 56, 200]),        # blue
# 	([70, 20, 10], [255, 70, 40]),          # orange
# 	([10, 60, 20], [70, 100, 70])          # green
# ]

boundaries = [
	([80, 10, 0], [255, 70, 70]),        # blue
    #([17, 15, 100], [50, 56, 200]),        # blue
	([10, 20, 70], [40, 70, 255]),          # orange
	([20, 60, 10], [70, 100, 70])          # green
]

def clustering_algorithm():
    pass

def imgAcondition(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		# conversión a escala de grises para procesar la imagen
    imgGray = cv2.GaussianBlur(imgGray,(5,5),0);		# aplico un filtro gaussiano para eliminar ruido y reducir las texturas
    imgGray = cv2.adaptiveThreshold(imgGray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,5,3.5)
    return imgGray

def circlesDetector(imgSource, imgOutput):
    # detecto los círculos en la imagen, el resultado viene en la forma: x_centro, y_centro, radio
    circles = cv2.HoughCircles(imgSource, cv2.HOUGH_GRADIENT, 1, 50, param1=200, param2=17, minRadius=4, maxRadius=25)

    # verifico que se haya encontrado algún circulo
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")			# convierto los datos a enteros

        # itero en cada uno de los círuclos
        for (x, y, r) in circles:
            cv2.circle(imgOutput, (x, y), r, (0, 255, 0), 4) 	# dibujo cada círculo en la imagen
        

def grayTreeChanelCreator(img):
	resolution = img.shape
	imgCreated = np.zeros((resolution[0],resolution[1],3), np.uint8)
	imgCreated[:,:,0] = img
	imgCreated[:,:,1] = img
	imgCreated[:,:,2] = img
	return imgCreated

def colorDetector(img):
    for(lower, upper) in boundaries:
        # creo un arreglo numpy para cada limite de color
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(img, lower, upper)
        imgOutput = cv2.bitwise_and(img, img, mask = mask)

        return imgOutput

def main():
    cap = cv2.VideoCapture(1)       # open comunication with cam
    assert cap.isOpened() == True, "Error With Camera (No conected)"

    while(True):            # main loop to get images from camera continuously
        ret, frame = cap.read()     # get an image (frame) from cam
        assert ret == 1, "Error reading the image"

        imgDetection = frame.copy()	# tomo un frma del video y creo una copia para mantener la imagen original

        # imgPixelsList = imgPixelsList.reshape((imgPixelsList.shape[0] * imgPixelsList.shape[1], 3))
        # clt = kmeans(n_clusters =3)
        # clt.fit(imgPixelsList)

        imgAconditioned = imgAcondition(frame)

        circlesDetector(imgAconditioned, imgDetection)

        imgAconditioned = grayTreeChanelCreator(imgAconditioned)

        imgOutput = imgDetection

        imgColorDetection = colorDetector(frame)

        cv2.imshow('Webcam', np.hstack([imgColorDetection,imgOutput]))           # show the frame in a window
        if cv2.waitKey(1) & 0xFF == ord('q'):
        	break

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
