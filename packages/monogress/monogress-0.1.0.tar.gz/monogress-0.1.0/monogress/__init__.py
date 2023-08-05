# -*- coding: utf-8 -*-
"""
Created on Mon May 24 15:54:14 2021

@author: franc
"""


import scipy.optimize as sopt
import numpy as np



def sig_op(z,x):
    
    ypred = np.abs([z[:int(len(z)/2)]]).T*np.array([x]) + \
        np.array([z[int(len(z)/2):]]).T
    ypred = 1/(1+np.exp(-ypred))
    ypred = np.sum(ypred,axis=0)
    
    return ypred


def obj_fct(z,x,y):
    
    ypred = sig_op(z,x)
    return -np.corrcoef(y,ypred)[0,1]




class fit:

    
    def __init__(self,x,y,nb_sigmoids=25,nb_trial=10):
    
        x = np.array(x).flatten()
        y = np.array(y).flatten()
    
        y_ori = y.copy()
    
        # Positive/negative
        corr_w = np.corrcoef(x,y)[0,1]
        corr_w = corr_w / np.abs(corr_w)
        self.corr_w = corr_w.copy()
        y = y * corr_w
        
        # Make trials
        all_corr = []
        all_x = []
        for trial in range(nb_trial):
        
            # Make otpimization
            sol = sopt.minimize(obj_fct,np.random.randn(nb_sigmoids*2),\
                                method="SLSQP",args=(x,y))
            
            all_x.append(sol.x.copy())
            all_corr.append(sol.fun)
            
        pos_best = np.argmin(all_corr)
        self.x = all_x[pos_best].copy()
        self.r2 = np.min(all_corr)**2
        
        # Make prediction
        ypred = self._sig_op_PREDICT(x)
        
        ypred1 = np.append(np.array([ypred]).T,np.array([ypred*0+1]).T,axis=1)
        b = np.linalg.inv(ypred1.T@ypred1)@ypred1.T@np.array([y_ori]).T
        b = b[:,0]
        self.b = b.copy()
            
    
    
    def _sig_op_PREDICT(self,z):
        
        ypred = np.abs([self.x[:int(len(self.x)/2)]]).T*np.array([z]) + \
            np.array([self.x[int(len(self.x)/2):]]).T
        ypred = 1/(1+np.exp(-ypred))
        ypred = np.sum(ypred,axis=0)
        
        return ypred
    
    
    
    def _lin_PREDICT(self,ypred):
        
        ypred = ypred*self.b[0]+self.b[1]
        return ypred
        
        
    
    def predict(self,z):
        
        ypred = self._sig_op_PREDICT(z)
        ypred = self._lin_PREDICT(ypred)
        return ypred

