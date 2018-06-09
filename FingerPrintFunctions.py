'''Funciones'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

kernel1 = np.matrix([[-1 ,-1 ,-1], [-1, 9, -1],[-1, -1, -1]])
kernel2 = np.matrix([[-2 ,-1 ,0], [-1, 1, 1],[0, 1, 2]])
kernel3 = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
kernel4 = np.array([[1,1,1], [1,-7,1], [1,1,1]])
kernel = kernel = np.ones((2,2),np.uint8)
#-----------------------------------------------------------------------------#
def build_filters():
     filters = []
     ksize = 31
     for theta in np.arange(0, np.pi, np.pi / 16):
         kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 11.0, 0.5, 0, ktype=cv2.CV_32F)
         kern /= 1.5*kern.sum()
         filters.append(kern)
     return filters
 
def process(img, filters):
     accum = np.zeros_like(img)
     for kern in filters:
         fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
         np.maximum(accum, fimg, accum)
     return accum
#-----------------------------------------------------------------------------#
def fingerMask(image):#Funcion que creara una mascara para el dedo
    #Convirtiendo imagen de BGR a LAB.
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    #Aplicando metodo de otsu y binarizando.
    ret, imgf = cv2.threshold(lab_image[:,:,2], 0, 255, cv2.THRESH_BINARY+\
                cv2.THRESH_OTSU)
    #Aplicando close a la imagen para eliminar huecos.
    ee = np.ones((20,20),np.uint8)
    imgf = cv2.morphologyEx(imgf, cv2.MORPH_CLOSE, ee)
    #Aplicando open a la imagen para eliminar areas basura.
    ee = np.ones((20,20),np.uint8)
    imgf = cv2.morphologyEx(imgf, cv2.MORPH_OPEN, ee)
    #Difuminando imagen.
    imgf = cv2.blur(imgf,(10,10))
    #Convirtiendo imagen entrada a gray
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Aplicando mascara
    image = cv2.bitwise_and(image,image,mask = imgf);
    #Retornando imagen enmascarada
    return image 
#-----------------------------------------------------------------------------#
def fingerBW(image):#Funcion para binarizaqr imagen con Thresh adaptativo
    #image = cv2.bitwise_not(image)
    #image = cv2.filter2D(image,-1,kernel1)
#    image_bw = cv2.Laplacian(image,cv2.CV_64F)
#    image_bw = np.uint8(np.absolute(image_bw))
    
    #image_bw = cv2.equalizeHist(image)
    #image = cv2.filter2D(image,-1,kernel1)
    #image = cv2.blur(image,(5,5))
    img_bw = cv2.adaptiveThreshold(image,1,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,51,2)
    #img_bw = cv2.morphologyEx(img_bw, cv2.MORPH_OPEN, kernel)
    #Image Skeleton
#    size = np.size(img_bw)
#    skel = np.zeros(img_bw.shape,np.uint8)
#    
#    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
#    done = False
#    img = img_bw
#    while( not done):
#        eroded = cv2.erode(img,element)
#        temp = cv2.dilate(eroded,element)
#        temp = cv2.subtract(img,temp)
#        skel = cv2.bitwise_or(skel,temp)
#        img = eroded.copy()
#        zeros = size - cv2.countNonZero(img)
#        if zeros==size:
#            done = True
    return img_bw
#-----------------------------------------------------------------------------#     
#img_name = '../Huellas/huella2.jpg'#Ruta de la huella  
#img = cv2.imread(img_name,3)#Leyendo la huella
#img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
#img_return = fingerMask(img)#Imagen enmascarada
#img_bw = fingerBW(img_return)#Skelton Imagen
#filters = build_filters()#Construir filtro Gabor 
#res1 = process(img_return, filters)#Aplicar filtro Gabor
#img_bw = fingerBW(res1)
#-----------------------------------------------------------------------------#
#Mostrar resultados.
#plt.imshow(img_return, cmap='gray')
#plt.show()
#-----------------------------------------------------------------------------#
#cv2.imshow('image',cv2.resize(img_bw, (0, 0), None, .2, .2))
#cv2.imshow('image1',cv2.resize(img_return, (0, 0), None, .2, .2))
#
##cv2.namedWindow('image',cv2.WINDOW_NORMAL);
##cv2.resizeWindow('image', 400,600);
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#-----------------------------------------------------------------------------#