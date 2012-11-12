#MODIFICAR LA FUNCION ACTUALIZAR Y FALTA BACKPROPAGATION

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

#	def leerNuevoArchivo(self, archivo):
#		archivo = open("archivoPrueba.txt")
#		otraLista = []
#		
#		for lineas in archivo.readlines():
#			lineas = lineas.split()
#			otraLista.append(lineas)
#		archivo.close()
#		
#		entr = len(otraLista[0])
#		num = len(otraLista)
#
#		res = zeros(num)
#
#		for num, linea in enumerate(otraLista):
#			for valor in linea:
#				linea[num] = otraLista[int(valor)]
#				
#		
#		#print res
#		return (res, num, entr) # debe ser un vector

	def leerE(self, archivo):
		archivo = open(archivo, "r")
		
		listaArchi = [] # Lista del contenido del archivo
		listaCoor = [] # Lista con todos los numeros mas el "-1"
		# Leemos el archivo
		for lineas in archivo.readlines(): # recorremos el archivo 	
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
		#print listaCoor

		vectEntra = empty((largo, dimencion)) # Creamos una matriz | PARAMETROS => ((filas(-), columnas(|)))
		# Convertimos la lista a NUMPY
		for i, valor1 in enumerate(listaCoor):
			for j, valor2 in enumerate(valor1):
				vectEntra[i][j] = valor2

		print "Vector de Entrada"
		print vectEntra
		print ""
		return (vectEntra, largo, dimencion)

	def generarP(self, largo, dimencion):	
		vectorP = empty((largo, dimencion)) 
		for i in range(largo):
			for j in range(dimencion):
				vectorP[i][j] = uniform(MIN, MAX)

		print "Vector de Pesos"
		print vectorP
		print ""
		return vectorP

	def sumatoria(self, largo, vecE, vecP):

		print "SUMATORIA"
		print vecE
		print ""
		print vecP
		print "FIN"
		print ""
		#vecSali = empty(largo)
		vecSali = sum(vecE* vecP)
		return vecSali


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

	def __init__(self, archivo):
		#salidaY = open("activacion.dat", "w") # este archivo sirve para guardar las salidas obtenidas
		#(res, interaciones, entr) = self.leerE(archivo) # Orignial
		(self.entradas, self.largo, self.dimencion)  = self.leerE(archivo) # Vector de entradas
		########################### PARAMETROS QUE REGRESA ##########################
		# entradas = vector de entradas	                                            #
		# largo = numero de elementos del vector de entrada     					#
		# dimencion = numero de elementos de cada elemento del vector de entrada.	#
		#############################################################################
		self.pesoEntra = self.generarP(self.largo, self.dimencion)
		self.pesoSali = self.generarP(self.largo, self.dimencion - 1)
		#pesos = self.generaW(interaciones) # genera pesos		
		## for vuelta in range(iteraciones):
		## res = self.generaE(entr)
		#
		#activacion = self.activar(res, pesos, entr) # obtenemos el primer valor de activacion
		#self.imprimir(res) # esta funcion no hace nada "imporante"
		#print activacion # comprobacion
		#print >> salidaY, "%d" % activacion
		#salidaY.close()
		#print "Guardando activacion en 'activacion.dat'..."
		#self.comparar(entr, pesos, res, alfa) # "entr" debe ser un vector	



# argv[1] => archivo con las coordenas del kinect 
def main():
	nueva = neurona(argv[1])
	(vecEntrada, largo, dimencion) = (nueva.entradas, nueva.largo, nueva.dimencion)

	for i in vecEntrada:
		print "I = ", i
		nueva.i = i
		nueva.capa = nueva.sumatoria(nueva.i, nueva.pesoEntra)
		nueva.capaSali = nueva.sumatoria(nueva.capa, nueva.pesoSali)

	print "FINAL"
	print "valor de la capa", nueva.capa
	print "valor de la salida", nueva.capaSali

main()