from sys import argv
from random import uniform, randint
from numpy import *

MIN = -1
MAX = 1
C = 0 # punto medio del rango del kinect

class neurona(object):
#	def generaE(self, entra):
#		archivo = open("entrada.dat", "a")
#		entrada = zeros(entra)
#		for i in range(entra):
#			entrada[i] = uniform(MIN, MAX)
#			print >> archivo, entrada[i], ' ',
#		print >> archivo, ""
#		entrada = append(entrada, -1)
#		archivo.close()
#		return entrada

	def leerNuevoArchivo(self):
		archivo = open("archivoPrueba.txt")
		otraLista = []
		
		for lineas in archivo.readlines():
			lineas = lineas.split()
			otraLista.append(lineas)
		archivo.close()
		
		entr = len(otraLista[0])
		num = len(otraLista)

		res = zeros(num)

		for num, valor in enumerate(otraLista):
			for dato in valor:
				
				
		
		#print res
				return (res, num, entr) # debe ser un vector

	def leerE(self, archivo):
		archivo = open(archivo, "r")
		nuevo = open("archivoPrueba.txt", "w")
		lista = [] # es una lista por mientras
		num = 0

		for lineas in archivo.readlines():
			num += 1
			lineas = lineas.rstrip()
			lista.append(lineas)
			lista.append("-1")

		for num, linea in enumerate(lista):
			print >> nuevo, linea,
			if num%2 != 0:
				print >> nuevo, "" 
		archivo.close()
		nuevo.close()
		
 		(res, num, entr) = self.leerNuevoArchivo()
					
		return (res, num, entr)#modificar el 3 parametro para que siempre sea 3

	def generaW(self, aux):	
		vectorW = zeros(aux + 1)
		for i in range(aux + 1):
			vectorW[i] = uniform(MIN, MAX)
		return vectorW

	def activar(self, entrada, pesos, n):
		if n == 2:
			suma = sum(entrada * pesos)
			if suma >= C:
				y = 1 # significa que solo puede ser el 3 o 4 cuadrante
			else:   
				y = 0 # significa que solo puede ser el 1 o 2 cuadrante
		else:
			suma = sum(entrada * pesos)
			if suma >= 0: #cambiar esta condicion, de hecho seran varias
				y = 1 
			else:
				y = 0
		return y

#	def activar2(self, entrada, pesos):
#		suma = sum(entrada * pesos)
#		if suma >= 0:
#			y = 1
#		else:   
#			y = 0
#		return y

	def imprimir(self, res):
		for i in range(len(res)-1):
			print res[i],
		return

	def recalculaW(self, entr, pesos, res, alfa, y, t):
		nuevoVW = zeros(entr + 1)
		for i in range(entr + 1):
			nuevoVW[i] = pesos[i] + (alfa * (t - y) * res[i])	
		return nuevoVW

	def comparar(self,entr, pesos, res, alfa):
		archivo = open("activacion.dat", "r")
		correctos = open("correctos.dat", "w")
		incorrectos = open("incorrectos.dat", "w")
		datos = []
		nuevoW = zeros(entr) # checar esto

		for linea in archivo.readlines():
			linea = linea.rstrip()
			t = randint(MIN+1, MAX)
			if int(linea) != t:
				pesos = self.recalculaW(entr, pesos, res, alfa, int(linea), t)
				print res
				print pesos
				Yesperada = self.activar(res, pesos, entr+1)
				if Yesperada == t:
					print >> correctos, str(res)
				else:
					print >> incorrectos, str(res)
			else:
				print >> correctos, str(res)
	
		archivo.close()
		correctos.close()
		incorrectos.close()
		return Yesperada

	def __init__(self, archivo,alfa):
		#print entr
		salidaY = open("activacion.dat", "w")
		(res, interaciones, entr) = self.leerE(archivo)
		pesos = self.generaW(interaciones)		
		# for vuelta in range(iteraciones):
		# res = self.generaE(entr)
		#
		activacion = self.activar(res, pesos, entr)
		self.imprimir(res)
		print activacion
		print >> salidaY, "%d" % activacion
		salidaY.close()
		print "Guardando activacion en 'activacion.dat'..."
		self.comparar(entr, pesos, res, alfa) # es un vector	


nue = neurona(argv[1] ,float(argv[2]))