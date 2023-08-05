# -*- coding: utf-8 -*-
"""
Created on Sun May 23 11:58:39 2021

@author: catig
"""

import rpy2.robjects as ro

primos_r = """
primos <- function(n){
mostrar <- paste("---Calculo de primos que hay hasta ", n)
print(mostrar)
    for (i in 2:n){
		esprimo <- TRUE
        tope <- i-1
		for (j in 2:tope){
			if (i%%j == 0){
				esprimo <- FALSE
            }
        }
		if (isTRUE(esprimo)){
			print(i)
        }
    }
}
"""
ro.r(primos_r)

primos_py = ro.globalenv['primos']
n = input("Cuantos primos quieres?")
primos_py(n)