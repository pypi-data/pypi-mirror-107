#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 20:39:09 2021

@author: CrisGalvan
"""

import rpy2.robjects as ro

def numPrimos(num):
    codigo_R="""
    primo <- function (n){
       if (n==1){return (1)}
        for (i in 2:n){
            if (n%%i==0){
                return(1)
                }
            }
    return(0)
    } 
    
    numPrimosR <- function (n){
        for (i in 1:n+1){
            if (primo(i)==0){
                 print(i)
                 }
            }
        }
    
    """
    ro.r(codigo_R)
    listaPrimos_py = ro.globalenv['numPrimosR']
    return listaPrimos_py(num)