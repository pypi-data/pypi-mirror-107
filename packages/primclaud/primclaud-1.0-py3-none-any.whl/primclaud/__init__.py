#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 19:52:31 2021

@author: ramon
"""
import math

def es_primo(n):

     cont=0

     for i in range(2,n):

        if(n%i==0):

             cont=cont+1

     if cont==0:

         return True

 
# bucle while

while True:

     try:

         n = int(input("insertar un numero: "))

         if (n==0  or  n==1  or  n<=1 ):

             break

         print("\nLos numeros primos son:")

         for j in range(2,n):

             if es_primo(j):

                print("\n %s " % j)

         break

     except:

         print("\nEl numero tiene que ser entero")