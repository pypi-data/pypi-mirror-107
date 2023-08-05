#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 19:52:31 2021

@author: ramon
"""
def sumaEnteros(a,b):
	return(a+b)

def restaEnteros(a,b):
	return(a-b)
	
def multiplicaEnteros(a,b):
	return(a*b)

def factorial(a):
	resultado = 1
	for i in range(1,a+1):
		resultado *= i
	
	return(resultado)
def primos_hasta(a):
    for i in range(1,a+1):
        contador=0
        for j in range(1,i): 
             if i%j==0:contador += 1
        if contador>= 2: print(i, " no es primo") 
        else: print(i, " es primo")
