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

		for num, linea in enumerate(otraLista):
			for valor in linea:
				linea[num] = otraLista[int(valor)]
				
		
		#print res
				return (res, num, entr) # debe ser un vector

	def leerE(self, archivo):
		archivo = open(archivo, "r")
		nuevo = open("archivoPrueba.txt", "w")
		lista = [] # es una lista por mientras

		for lineas in archivo.readlines(): # recorremos el archivo 
			lineas = lineas.rstrip() # sirve para quitar los "\n"
			lista.append(lineas) # despues de leer cada linea agregamos
			lista.append("-1") # el -1 al final de la linea

		# una vez que la "lista" esta preparada tenemos que recorrerla de nuevo para sacar 
		#imprimirla en un archivo y ahori si poder leerla bien
		for num, linea in enumerate(lista): 
			print >> nuevo, linea,
			if num%2 != 0:
				print >> nuevo, "" # si no es multiplo, has un "\n"
		archivo.close()
		nuevo.close()
		
 		(res, num, entr) = self.leerNuevoArchivo() # FUNCION AUN EN PROCESO
					
		return (res, num, entr)#modificar el 3 parametro para que siempre sea 3

	def generaW(self, aux):	
		vectorW = zeros(aux + 1) # genera la misma cantidad de pesos que las entradas
		for i in range(aux + 1): # el "+1" es para el "-1" al final de cada linea
			vectorW[i] = uniform(MIN, MAX) 
		return vectorW

	def activar(self, entrada, pesos, n):
		if n == 2: # este es para la primera comparacion
			suma = sum(entrada * pesos)
			if suma >= C:
				y = 1 # significa que solo puede ser el 3 o 4 cuadrante
			else:   
				y = 0 # significa que solo puede ser el 1 o 2 cuadrante
		else: # la segunda comparacion esta nos dira si el entrenamiento esta mejorando
			# aqui tienen que ir los "if's" de los rangons
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

	def imprimir(self, res): # esa funcion es puro show, es para disminuir lineas 
		for i in range(len(res)-1): # en el contructor
			print res[i],
		return

	def recalculaW(self, entr, pesos, res, alfa, y, t):
		nuevoVW = zeros(entr + 1) # crea un nuevo verctor de pesos 
		for i in range(entr + 1): #el "+1" por el "-1" de la 3ra columna
			nuevoVW[i] = pesos[i] + (alfa * (t - y) * res[i]) # para recalcular	
		return nuevoVW

	def comparar(self,entr, pesos, res, alfa):
		archivo = open("activacion.dat", "r") 
		correctos = open("correctos.dat", "w")
		incorrectos = open("incorrectos.dat", "w")
		datos = []
		nuevoW = zeros(entr) # checar esto

		for linea in archivo.readlines(): # leemos el archivo en donde tenemos las 
			linea = linea.rstrip() # eliminamos saltas de linea
			t = randint(MIN+1, MAX)
			if int(linea) != t: # si la t no es la misma a la esperada
				pesos = self.recalculaW(entr, pesos, res, alfa, int(linea), t) #recalcula pesos
				print res # comprobacion
				print pesos # comprobacion 
				Yesperada = self.activar(res, pesos, entr+1) # esta es la "Y" esperada (modificar esa funcion)
				if Yesperada == t: #checar esta parte !!!!!!!!!!!!!
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
		salidaY = open("activacion.dat", "w") # este archivo sirve para guardar las salidas obtenidas
		(res, interaciones, entr) = self.leerE(archivo) # estamos aqui
		pesos = self.generaW(interaciones) # genera pesos		
		# for vuelta in range(iteraciones):
		# res = self.generaE(entr)
		#
		activacion = self.activar(res, pesos, entr) # obtenemos el primer valor de activacion
		self.imprimir(res) # esta funcion no hace nada "imporante"
		print activacion # comprobacion
		print >> salidaY, "%d" % activacion
		salidaY.close()
		print "Guardando activacion en 'activacion.dat'..."
		self.comparar(entr, pesos, res, alfa) # "entr" debe ser un vector	


nue = neurona(argv[1] ,float(argv[2]))