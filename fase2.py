#MODIFICAR LA FUNCION ACTUALIZAR Y FALTA BACKPROPAGATION

from sys import argv
from random import uniform, randint
from numpy import *

MIN = -1
MAX = 1

Zx = 320 # pixeles de la mitad del kinect
Zy = 240 # pixeles de la mitad del kinect
#Zypos = 440 # pixeles de la ventana del kinect
#Zyneg = 40 # pixeles de la ventana del kinect

class neurona(object):

	def leerE(self, archivo):
		archivo = open(archivo, "r")
		
		listaArchi = [] # Lista del contenido del archivo
		listaCoor = [] # Lista con todos los numeros mas el "-1"
		# Leemos el archivo
		for lineas in archivo.readlines(): #recorremos el archivo 	
			lineas = lineas.split()
			listaArchi.append(lineas) # Agregamos las coordenas a la lista.
			
		dimencion = len(listaArchi[0]) + 1 # Para hacer a las dimenciones variables
											#dinamicas
		# Para agregar el (-1) al par de coordenadas 
		#que tenemos hasta el momento
		for i in listaArchi:
			for j in i:
				listaCoor.append(j)
			listaCoor.append(-1) 

		# Hasta este punto tenemos una lista de la forma 
		#<a = ["1","2","-1","3","4","-1","5","6","-1"]>
		#el for siguiente es para convertirla a la forma 
		#que la necesitamos <a = [[1,2,-1],[3,4,-1],[5,6,-1]]>

		largo = len(listaCoor) / dimencion # Variable para controlar el rango del "for"
		# Dividamos la lista en tercias
		#---CUANDO TENGA TIEMPO MODIFICAR ESTA PARTE PARA QUE LAS DIMENCIONES SEAN DINAMICAS
		for i in range(largo):
			num1 = int(listaCoor.pop(0))
			num2 = int(listaCoor.pop(0))
			num3 = int(listaCoor.pop(0))
			listaCoor.append((num1, num2 ,num3))
		#print listaCoorlargo

		vectEntra = zeros((largo, dimencion)) # Creamos una matriz | PARAMETROS => ((filas(-), columnas(|)))
		# Convertimos la lista a NUMPY
		for i, valor1 in enumerate(listaCoor):
			for j, valor2 in enumerate(valor1):
				vectEntra[i][j] = valor2

		#print "Vector de Entrada"
		#print vectEntra
		#print ""
		#print "dimencion", dimencion
		return (vectEntra, dimencion)

	def generarP(self, largo, dimencion):	
		vectorP = empty((largo,dimencion)) 
		for i in range(largo):
			for j in range(dimencion):
				vectorP[i][j] = uniform(MIN, MAX)
		return vectorP



	def sumatoria(self, largo, dimencion, vecE, vecP):
		#print vecE
		#print vecP
		vecs = zeros(largo)
		for i in range(largo):
			vecs[i] = sum(vecE[i] * vecP[i])
		return vecs
		###########################################
		#segun AVE
		#vecs =  empty(largo)
		#for i in range(largo):
		#	for j in range(dimencion):
		#		vecs[i] = (vecE[j] * vecP[j])
		#return vecs
		###########################################
		#suma = sum(pesos * entrada)
		#return suma
	
	"""
	#Obteniendo errores ****
	def error(z, vecP)
	'''
	Errores = [d1, d2, d3, dn]
	z = valor deseado
	vecP = vector de pesos
	'''

	'''
	Fin de programa
	'''
	return vectorErrores
	#Fin de obteniendo errores
	"""

	def calcularF123(self, pesoSali, f4, f5):
		f1 = ((pesoSali[0][0] * f4) + (pesoSali[0][1] * f5))
		f2 = ((pesoSali[1][0] * f4) + (pesoSali[1][1] * f5))
		f3 = ((pesoSali[2][0] * f4) + (pesoSali[2][1] * f5))
		return(f1, f2, f3)


	def calcularF(self, capaSali, pesoSali):
		valorX = abs(capaSali[0])
		valorY = abs(capaSali[1])
		f4 = Zx - valorX 
		f5 = Zy - valorY
		(f1, f2, f3) = self.calcularF123(pesoSali, f4, f5) 
		return(f1, f2, f3, f4, f5)

	def __init__(self, archivo):
		(self.entradas, self.dimencion)  = self.leerE(archivo) # Vector de entradas
		########################### PARAMETROS QUE REGRESA ##########################
		# entradas = vector de entradas	                                            #
		# dimencion = numero de elementos de cada elemento del vector de entrada.   #
		#############################################################################
		self.pesoEntra = self.generarP(self.dimencion, self.dimencion)
		self.pesoSali = self.generarP(self.dimencion, self.dimencion - 1)

# argv[1] => archivo con las coordenas del kinect 
def main():
	nueva = neurona(argv[1])
	(vecEntrada, dimencion) = (nueva.entradas, nueva.dimencion)

	for i in vecEntrada:
			nueva.i = i
			#print nueva.i  
			nueva.capa = nueva.sumatoria(nueva.dimencion, nueva.dimencion, \
				nueva.i, nueva.pesoEntra)
			nueva.capaSali = nueva.sumatoria(nueva.dimencion, nueva.dimencion - 1,\
				nueva.capa, nueva.pesoSali)
			(nueva.f1, nueva.f2, nueva.f3, nueva.f4, nueva.f5) = \
				nueva.calcularF(nueva.capaSali, nueva.pesoSali)


	print "***F1", nueva.f1
	print "***F2", nueva.f2
	print "***F3", nueva.f3
	print "***F4", nueva.f4
	print "***F5", nueva.f5

	print "-------------------------"
	print "PESO ENTRADA"
	print nueva.pesoEntra
	print "-------------------------"
	print "VALOR DE LA CAPA", nueva.capa
	print "VALOR DE LA SALIDA", nueva.capaSali
	print "Peso capaSalida", nueva.pesoSali

main()
