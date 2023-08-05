#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 19:52:31 2021

@author: Jesús Patricio
"""
def primo(n):
	for i in range(2, n+1): # Va desde el 1 hasta n
		es_primo = True
		for j in range (2, i):
			if(i%j == 0):
				es_primo = False
		if(es_primo):
			print(f"El número {i} es primo")

#Pedimos que se introduzca un número para pasarlo como parámetro a la función anterior
numero = int(input("Introduce un número entero "))

primo(numero)
