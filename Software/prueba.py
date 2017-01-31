import numpy as np
import argparse
import cv2
from sys import exit

cap = cv2.VideoCapture(1) # inicia la comunicación con la cámara
assert cap.isOpened() == True, "Error With Camera (No conected)"

def grayTreeChanelCreator(img):
	resolution = img.shape
	imgCreated = np.zeros((resolution[0],resolution[1],3), np.uint8)
	imgCreated[:,:,0] = img
	imgCreated[:,:,1] = img
	imgCreated[:,:,2] = img
	return imgCreated

while(True):
	ret, frame = cap.read()		# leo una image de la cámara
	assert ret == 1, "Error reading the image"

	imgOutput = frame.copy()	# tomo un frma del video y creo una copia para mantener la imagen original
	imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)		# conversión a escala de grises para procesar la imagen

	imgGray = cv2.GaussianBlur(imgGray,(5,5),0);		# aplico un filtro gaussiano para eliminar ruido y reducir las texturas
	# imgGray = cv2.medianBlur(imgGray,5)

	''' podría dejar el threshold adaptativo si lo canfiguro para que no detecte bordes
	de lo contrario tendría que calibrar el umbral a mano siempre '''
	imgGray = cv2.adaptiveThreshold(imgGray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,5,3.5)

	# imgGray = cv2.threshold(imgGray, 60, 255, cv2.THRESH_BINARY)[1]      # convert the image to a binary image to find contours

	# detecto los círculos en la imagen, el resultado viene en la forma: x_centro, y_centro, radio
	circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, 1, 50, param1=200, param2=17, minRadius=2, maxRadius=40)

	imgGray = grayTreeChanelCreator(imgGray)

	# verifico que se haya encontrado algún circulo
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")			# convierto los datos a enteros

		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			cv2.circle(imgOutput, (x, y), r, (0, 255, 0), 4) 	# dibujo los círculos en la imagen

	cv2.imshow('Webcam', np.hstack([imgGray,imgOutput]))           # show the frame in a window
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# cierro la comunicación con la cámara y cierro todas las ventas (imágenes)
cap.release()
cv2.destroyAllWindows()
