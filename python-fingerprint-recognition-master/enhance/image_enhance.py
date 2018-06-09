# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 22:50:30 2016

@author: utkarsh
"""
from ridge_segment import ridge_segment
from ridge_orient import ridge_orient
from ridge_freq import ridge_freq
from ridge_filter import ridge_filter
import cv2
def image_enhance(img):
    blksze = 16;
    thresh = 0.1;
    normim,mask = ridge_segment(img,blksze,thresh);             # normalise the image and find a ROI


    gradientsigma = 1;
    blocksigma = 7;
    orientsmoothsigma = 7;
    orientim = ridge_orient(normim, gradientsigma, blocksigma, orientsmoothsigma);              # find orientation of every pixel


    blksze = 38;
    windsze = 5;
    minWaveLength = 5;
    maxWaveLength = 15;
    freq,medfreq = ridge_freq(normim, mask, orientim, blksze, windsze, minWaveLength,maxWaveLength);    #find the overall frequency of ridges
    
    
    freq = medfreq*mask;
    kx = 0.65;ky = 0.65;
    newim = ridge_filter(normim, orientim, freq, kx, ky);       # create gabor filter and do the actual filtering
    
    
    #th, bin_im = cv2.threshold(np.uint8(newim),0,255,cv2.THRESH_BINARY);
    return(newim < -3)
    
img_name = '../../../Huellas/huella2.jpg'#Ruta de la huella  
img = cv2.imread(img_name,3)#Leyendo la huella

imgE = image_enhance(img[:,:,1])
#Mostrar resultados.
cv2.imshow('image1',cv2.resize(imgE, (0, 0), None, .2, .2))
#cv2.namedWindow('image',cv2.WINDOW_NORMAL);
#cv2.resizeWindow('image', 400,600);
cv2.waitKey(0)
cv2.destroyAllWindows()