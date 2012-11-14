from random import *
from numpy import *

class neurona():
    def __init__(self):
        self.entrada = zeros(3)
        self.pesoen = self.gpesos(3,3)
        self.pesoca = self.gpesos(3,2)
        self.capa = zeros(3)
        self.csalida = zeros(2)

    def neentrada(self,x,y):
        self.entrada[0] = (x) 
        self.entrada[1] = (y)
        self.entrada[2] = (-1)
        
    def gpesos(self,fila,colum):
        vec = zeros(shape=(fila,colum))
        for i in range(fila):
            for j in range(colum):
                vec[i][j] = (random.random())
        return vec

    def sumatoria(self,fila,colum,vece,vecp):
        print "AQUI"
        print vece
        print vecp
        print "ACA"
        vecs = zeros(fila)
        for i in range(fila):
            vecs[i] = sum(vece[i]*vecp[i])
        return vecs    

x = int(raw_input("dame el valor de x: "))
y = int(raw_input("dame el valor de y: "))

def main():
    nueva = neurona()
    nueva.neentrada(x,y)
    nueva.capa = nueva.sumatoria(3,3, nueva.entrada,nueva.pesoen)
    nueva.csalida = nueva.sumatoria(3,2,nueva.capa,nueva.pesoca)

    print "entrada = ",nueva.entrada    
    print "peso entrada",nueva.pesoen
    print "valor de la caoa",nueva.capa 
    print "valor de la salida",nueva.csalida

main()
