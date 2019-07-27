# -*- coding=utf-8 -*-  
# Kalman filter example demo in Python  
  
# A Python implementation of the example given in pages 11-15 of "An  
# Introduction to the Kalman Filter" by Greg Welch and Gary Bishop,  
# University of North Carolina at Chapel Hill, Department of Computer  
# Science, TR 95-041,  
# http://www.cs.unc.edu/~welch/kalman/kalmanIntro.html  
  
# by Andrew D. Straw  
#coding:utf-8  
import numpy  
##import pylab  

def KalmanFilter(z,  n_iter = 20):  
    #这里是假设A=1，H=1的情况  
      
    # intial parameters  
     
    sz = (n_iter,) # size of array  
##    x = -0.37727 # truth value (typo in example at top of p. 13 calls this z)  
##    z = numpy.random.normal(x,0.1,size=sz) # observations (normal about x, sigma=0.1)  
      
    #Q = 1e-5 # process variance  
    Q = 1e-6 # process variance   
    # allocate space for arrays  
    xhat=numpy.zeros(sz)      # a posteri estimate of x  
    P=numpy.zeros(sz)         # a posteri error estimate  
    xhatminus=numpy.zeros(sz) # a priori estimate of x  
    Pminus=numpy.zeros(sz)    # a priori error estimate  
    K=numpy.zeros(sz)         # gain or blending factor  
      
    R = 0.1**2 # estimate of measurement variance, change to see effect  
      
    # intial guesses  
    xhat[0] = 0.0  
    P[0] = 1.0  
    A = 1
    H = 1

    for k in range(1,n_iter):  
        # time update  
        xhatminus[k] = A * xhat[k-1]  #X(k|k-1) = AX(k-1|k-1) + BU(k) + W(k),A=1,BU(k) = 0  
        Pminus[k] = A * P[k-1]+Q      #P(k|k-1) = AP(k-1|k-1)A' + Q(k) ,A=1  
      
        # measurement update  
        K[k] = Pminus[k]/( Pminus[k]+R ) #Kg(k)=P(k|k-1)H'/[HP(k|k-1)H' + R],H=1  
        xhat[k] = xhatminus[k]+K[k]*(z[k]-H * xhatminus[k]) #X(k|k) = X(k|k-1) + Kg(k)[Z(k) - HX(k|k-1)], H=1  
        P[k] = (1-K[k] * H) * Pminus[k] #P(k|k) = (1 - Kg(k)H)P(k|k-1), H=1  
    return xhat

if __name__ == '__main__':
    sz = (50,) # size of array
    x = -0.37727 # truth value (typo in example at top of p. 13 calls this z)  
    z = numpy.random.normal(x,0.1,size=sz) # observations (normal about x, sig
    xhat = KalmanFilter(z)
    print('Noise: ', z)
    print('After filte: ', xhat)
