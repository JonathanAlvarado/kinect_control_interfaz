#!/usr/bin/python

from sys import argv
from numpy import *
from numpy.random import *

low = -1
high = 1

class neurona(object):

    def getPesos(self,n):
        pesos = uniform(low,high,(1,n+1))
        return pesos

    def getEntradas(self,n):
        entrada = uniform(low,high,(1,n))
	#print entrada
        entrada = append(entrada, -1.0)
        return entrada

    def Activacion(self,pesos,entrada):
        mult = pesos * entrada
        act = mult.sum()
        return act

    def Salida(self,act):
        if(act >= 0):
            y = 1
        else:
            y = 0
        return y

    def __init__(self,n,it):
       pesos = self.getPesos(n)
       for i in range (it):
            entrada = self.getEntradas(n)
            act = self.Activacion(pesos,entrada)
            y = self.Salida(act)
            print entrada[0],entrada[1],y

neu = neurona(int(argv[1]) ,int(argv[2]))
