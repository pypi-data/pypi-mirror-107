#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 20:06:36 2021

@author: CrisGalvan
"""

import rpy2.robjects as ro


# Función para saber si un número es primo o no
# mediante el uso único de python
def isPrimoPy(num):
    if (num == 1): return False
    for i in range (2, num):
        if (num%i == 0): return False
    return True

#Función para saber el conjunto de números de primos 
#desde 1 hasta el número introducido por el usuario
#mediante el uso único de Python
def numPrimosPy(numero):
    listaPrimos = []
    for i in range(1,numero+1):
        if (isPrimoPy(i)):
            listaPrimos.append(i)
    return listaPrimos


#Función para saber la lista de números primos
#desde 1 hasta el número introducido por el 
#usuarios mediante el uso de R
def numPrimosR(num):
    codigo_R="""
    primo <- function (n){
       if (n==1){return (1)}
        if(n==2){
            return(0)
                }
        for (i in 3:n-1){
            if (n%%i==0){
                return(1)
                }
            }
    return(0)
    } 
    
    numPrimosR <- function (n){
        for (i in 1:n){
            if (primo(i)==0){
                 print(paste(i," es primo"))
                 }
            }
        }
    """
    ro.r(codigo_R)
    listaPrimos_py = ro.globalenv['numPrimosR']
    return listaPrimos_py(num)