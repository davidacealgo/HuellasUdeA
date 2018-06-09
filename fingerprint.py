# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 11:32:00 2018

@author: Orion
"""
"""Librerias"""
import cv2
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt

#Leyendo la imagen
Img_Original = cv2.imread('../Huellas/102_2.tif',3)
#Imagen en escala de grises
Img_Original = cv2.cvtColor(Img_Original, cv2.COLOR_BGR2GRAY)
#Imagen en formato binario
ret,BW_Original = cv2.threshold(Img_Original, 127, 1, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU);
#Esqueletizando imagen binaria
skeleton = skeletonize(BW_Original)
#Mostrando imagenes
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8, 4),
                         sharex=True, sharey=True)
ax = axes.ravel()

ax[0].imshow(Img_Original, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('Original', fontsize=20)

ax[1].imshow(BW_Original, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('Binaria', fontsize=20)

ax[2].imshow(skeleton, cmap=plt.cm.gray)
ax[2].axis('off')
ax[2].set_title('Skeleton', fontsize=20)

plt.show()