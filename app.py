#!/usr/bin/env python-fingerprint-recognition-master
"""-------------------------------------------------------------------------------------------
----------  Procesamiento de huellas digitales -----------------------------------------------
----------  Proyecto final PDI ---------------------------------------------------------------
----------  Por: Cristian Dario Pulido   -----------------------------------------------------
----------       David Alejandro Acevedo -----------------------------------------------------
----------       Orion Montoya           -----------------------------------------------------
----------       Alvaro Chacon           -----------------------------------------------------
----------Curso de procesamiento digital de imagenes------------------------------------------
----------Universidad de Antioquia------------------------------------------------------------
----------Medellin 2018-----------------------------------------------------------------------
"""
"""
----------1. Inicializacion del sistema e insercion de librerias---------------------------------"""
import cv2
import os
import web
import sys
import numpy
import matplotlib.pyplot as plt
import base64
from scipy import misc
from skimage.morphology import skeletonize, thin
from FingerPrintFunctions import fingerBW, fingerMask
os.chdir("/home/estudiantes/davida.acevedo/Downloads/Archivospython/python-fingerprint-recognition-master") #Definicion de la ruta master

"""--------------------------------------------------------------------------------------------
----------2. Remover puntos de la imagen (Ruido)-----------------------------------------------
--------------------------------------------------------------------------------------------"""

def removedot(invertThin):
    temp0 = numpy.array(invertThin[:])   #Creacion de variables
    temp0 = numpy.array(temp0)
    temp1 = temp0/255
    temp2 = numpy.array(temp1)
    temp3 = numpy.array(temp2)
    enhanced_img = numpy.array(temp0)   #Arreglo de la imagen
    filter0 = numpy.zeros((10,10))
    W,H = temp0.shape[:2]
    filtersize = 6 #Numero maximo de pixeles
    for i in range(W - filtersize):  #Eliminacion de islas de pixeles #Ciclos de recorrido de la imagen
        for j in range(H - filtersize):
            filter0 = temp1[i:i + filtersize,j:j + filtersize]
            flag = 0
            if sum(filter0[:,0]) == 0:
                flag +=1
            if sum(filter0[:,filtersize - 1]) == 0:
                flag +=1
            if sum(filter0[0,:]) == 0:
                flag +=1
            if sum(filter0[filtersize - 1,:]) == 0:
                flag +=1
            if flag > 3:
                temp2[i:i + filtersize, j:j + filtersize] = numpy.zeros((filtersize, filtersize))

    return temp2


"""--------------------------------------------------------------------------------------------
----------3. Extraccion de minucias -----------------------------------------------------------
--------------------------------------------------------------------------------------------"""
def get_descriptors(img):#Descriptor de la huellas dactilares.
    img = fingerMask(img)#Se envia imagen de la huella, retorna la huella sin fondo y en Gray.
    img = fingerBW(img)#Binarizacion de la huella dactilar.
    img = numpy.array(img, dtype=numpy.uint8)#Convertir matriza de imagen a array.
    # Umbral
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU);#Aplicacion del metodo de OTSU
    img[img == 255] = 1
    #Adelgazamiento
    skeleton = skeletonize(img)
    skeleton = numpy.array(skeleton, dtype=numpy.uint8)
    skeleton = removedot(skeleton)
    # Harris corners aplicado las imagenes para encontrar las bifurcaciones y los finales de cresta
    harris_corners = cv2.cornerHarris(img, 3, 3, 0.04)
    harris_normalized = cv2.normalize(harris_corners, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
    threshold_harris = 125;#umbral para el harris_corners
    # Extracion de los puntos clave(bifurcaciones y finales de cresta)
    keypoints = []
    for x in range(0, harris_normalized.shape[0]):
        for y in range(0, harris_normalized.shape[1]):
            if harris_normalized[x][y] > threshold_harris:
                keypoints.append(cv2.KeyPoint(y, x, 1))
    #Definicion del descriptor
    orb = cv2.ORB_create()
    #Computacion del descriptor 
    _, des = orb.compute(img, keypoints)
    return (keypoints, des)

"""--------------------------------------------------------------------------------------------
----------4. Codigo Principal -----------------------------------------------------------------
--------------------------------------------------------------------------------------------"""
def main(foto):
	#Lectura de la primera imagen
    img1 = base64.decodestring(foto)
    skin = np.zeros((2808,3744,3),dtype='uint8')
    cv2.imshow('imagen',skin)
    print("decodifico")
    plt.imshow(img1)
    plt.savefig('/home/estudiantes/davida.acevedo/Downloads/Archivospython/python-fingerprint-recognition-master/database/foto.png')
    print("guardo")
    img1 = cv2.imread('/home/estudiantes/davida.acevedo/Downloads/Archivospython/python-fingerprint-recognition-master/database/foto.png', 3)
	#Se aplica un resize para mejorar el tiempo de computo
     
    img2=img1
    print("paso 1")
    img1 = cv2.resize(img1, (0,0), fx=0.5, fy=0.5)
 
	#Descriptor de la primera imagen
    kp1, des1 = get_descriptors(img1)

    #Lectura de la segunda imagen
    #img2 = cv2.imread('/home/estudiantes/davida.acevedo/Downloads/Archivospython/python-fingerprint-recognition-master/database/101_1.tif', 3)
	#Se aplica un resize para mejorar el tiempo de computo
    img2 = cv2.resize(img2, (0,0), fx=0.5, fy=0.5)
	#Descriptor de la segunda imagen
    kp2, des2 = get_descriptors(img2)

    print("paso 2")
    # Matching entre descriptores
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = sorted(bf.match(des1, des2), key=lambda match:match.distance)
    #Mostrar dibujar puntos clave en las dos imagenes 
    img4 = cv2.drawKeypoints(img1, kp1, outImage=None)
    img5 = cv2.drawKeypoints(img2, kp2, outImage=None)
    f, axarr = plt.subplots(1,2)
    axarr[0].imshow(img4)
    axarr[1].imshow(img5)
    plt.savefig('/home/estudiantes/davida.acevedo/Downloads/Archivospython/python-fingerprint-recognition-master/database/img4.png')
    #Mostrar Matches
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches, flags=2, outImg=None)
    plt.imshow(img3)
    plt.savefig('/home/estudiantes/davida.acevedo/Downloads/Archivospython/python-fingerprint-recognition-master/database/img3.png')
    print("paso 3")
    #Calcular puntaje
    score = 0
    for match in matches:
        score += match.distance
    score_threshold = 33
    if score/len(matches) < score_threshold:
        matching=0
    else:
        matching=1

    print("paso 4")



	
	
if __name__ == "__main__":
	try:
		main()
	except:
		raise