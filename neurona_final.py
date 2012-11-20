from sys import argv
from random import uniform, randint
from numpy import *
import math

MIN = -1
MAX = 1

Zx = 320 # pixeles de la mitad del kinect
Zy = 240 # pixeles de la mitad del kinect
#Zypos = 440 # pixeles de la ventana del kinect
#Zyneg = 40 # pixeles de la ventana del kinect

def autocompletar(largo, dimencion, fill = 0.0):
	vec = []
	for i in range(largo):
		vec.append([fill] * dimencion)
	return vec

def sigmoid(x):
	return math.tanh(x)

def dsigmoid(x):
	return math.tanh(x)

class neurona(object):

	def leerE(self, archivo):
		archivo = open(archivo, "r")
		
		inter = 0 # para ve las veces de interacciones del algoritmo
		listaArchi = [] # Lista del contenido del archivo
		listaCoor = [] # Lista con todos los numeros mas el "-1"
		# Leemos el archivo
		for lineas in archivo.readlines(): #recorremos el archivo 	
			lineas = lineas.split()
			listaArchi.append(lineas) # Agregamos las coordenas a la lista.
			inter += 1

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
		return (vectEntra, dimencion, inter)


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

	def imprimirArchivo(self, pesoEntra):
		archivo = open("vectorPesos.txt", "w")
		for lista in pesoEntra:
			for contenido in lista:
				print >> archivo, contenido,
			print >> archivo, ""
		archivo.close()
		return

	def leerArchivo(self, largo, dimension):
		archivo = open("vectorPesos.txt", "r")
		numeros = []
		for lista in archivo.readlines():
			lista = lista.split()
			numeros.append(lista)

		#convertimos a NUMPY
		pesoSali = empty((largo,dimension))
		for i, valor in enumerate(numeros):
			for j, valor2 in enumerate(valor):
				pesoSali[i][j] = valor2
		return pesoSali

	def backPropagate(self, targets, N, M):
		if len(targets) != self.dimension - 1:
			raise ValueError("No coinciden los largos")

		# calculate error terms for output
		output_deltas = [0.0] * (self.dimension - 1)
		for k in range(self.dimension - 1):
			error = targets[k]-self.ao[k]
			output_deltas[k] = dsigmoid(self.ao[k]) * error

		# calculate error terms for hidden
		hidden_deltas = [0.0] * (self.dimension - 2)
		for j in range(self.dimension - 2):
			error = 0.0
			for k in range(self.dimension - 1):
				error = error + output_deltas[k]*self.pesoSali[j][k]
			hidden_deltas[j] = dsigmoid(self.ah[j]) * error

		# update output weights
		for j in range(self.dimension - 2):
			for k in range(self.dimension - 1):
				change = output_deltas[k]*self.ah[j]
				self.pesoSali[j][k] = self.pesoSali[j][k] + N*change + M*self.momentumSali[j][k]
				self.momentumSali[j][k] = change
				# print N*change, M*self.co[j][k]

		# update input weights
		for i in range(self.dimension):
			for j in range(self.dimension - 2):
				change = hidden_deltas[j]*self.ai[i]
				self.pesoEntra[i][j] = self.pesoEntra[i][j] + N*change + M*self.momentumEntra[i][j]
				self.momentumEntra[i][j] = change

		# calculate error
		error = 0.0
		for k in range(len(targets)):
			error = error + 0.5 * (targets[k] - self.ao[k]) ** 2
		return error

	def prueba(self, entradas):
		for p in entradas:
			print(p, '->', self.cargar(p))

	
	def cargar(self, inputt):
		inputs = list(inputt[:-1])
 
		if len(inputs) != self.dimension-1:
			raise ValueError("No coinciden los largos")

		# input activations
		for i in range(self.dimension - 1):
			# self.ai[i] = sigmoid(inputs[i])
			self.ai[i] = inputs[i]
	    
		# hidden activations
		for j in range(self.dimension - 2):
			sum = 0.0
			for i in range(self.dimension):
				sum = sum + self.ai[i] * self.pesoEntra[i][j]
			self.ah[j] = sigmoid(sum)

		# output activations
		for k in range(self.dimension - 1):
			sum = 0.0
			for j in range(self.dimension - 2):
				sum = sum + self.ah[j] * self.pesoSali[j][k]
			self.ao[k] = sigmoid(sum)
		return self.ao[:]

	def obtenerO(self, entrada, puntoFinal):
		x = entrada[0]
		y = entrada[1]
		xf = puntoFinal[0]
		yf = puntoFinal[1]
		objetivos = []

		val1 = xf - x
		val2 = yf - y

		if val1 > 320:
			objetivos.append(40)
		else:
			objetivos.append(440)
		if val2 > 240:
			objetivos.append(200)
		else:
			objetivos.append(40)
		return objetivos

	def entrenar(self, vecEntrada, inter, N = 0.5, M = 0.1):
		# N: taza de aprendizaje
		# M: momentum
		for o in vecEntrada:
			puntoFinal = o

		for i in range(inter/2):
			error = 0.0
			for p in vecEntrada:
				entrada = p
				objetivo = self.obtenerO(entrada, puntoFinal)
				self.cargar(entrada)
				error = error + self.backPropagate(objetivo, N, M)
			if i % 100 == 0:
				print('error %-.5f' % error)


	def __init__(self, archivo, ENTRENAMIENTO):
		(self.entradas, self.dimension, self.inter)  = self.leerE(archivo) # Vector de entradas
		########################### PARAMETROS QUE REGRESA ##########################
		# entradas = vector de entradas	                                            #
		# dimencion = numero de elementos de cada elemento del vector de entrada.   #
		#############################################################################
		if ENTRENAMIENTO == "1":
			self.pesoEntra = self.generarP(self.dimension, self.dimension) 
			self.imprimirArchivo(self.pesoEntra)
		else:
			self.pesoEntra = self.leerArchivo(self.dimension, self.dimension)

		self.pesoSali = self.generarP(self.dimension, self.dimension - 1)

		self.ai = [1.0] * int(self.dimension)
		self.ah = [1.0] * int(self.dimension - 2)
 		self.ao = [1.0] * int(self.dimension - 1)

		# ultimo cambio a los pesos para el momentum
		self.momentumEntra = autocompletar(self.dimension, self.dimension)
		self.momentumSali = autocompletar(self.dimension, self.dimension -1)	

###############################################################
# argv[1] => es el archivo de las coordenadas                 #
# argv[2] => es la bandera, "1" para entrenamiento nuevo      #
#            "2" para leer el archivo de pesos que se creo    #
###############################################################
def main():
	nueva = neurona(argv[1], argv[2])
	(vecEntrada, dimension, inter) = (nueva.entradas, nueva.dimension, nueva.inter)

	nueva.entrenar(vecEntrada, inter)
	nueva.prueba(vecEntrada)

	#for i in vecEntrada:
			#nueva.i = i
			#print nueva.i  
			#nueva.capa = nueva.sumatoria(nueva.dimencion, nueva.dimencion, \
			#	nueva.i, nueva.pesoEntra)
			#nueva.capaSali = nueva.sumatoria(nueva.dimencion, nueva.dimencion - 1,\
			#	nueva.capa, nueva.pesoSali)
			#### AQUI va un if para verificar si hubo error y reajustar pesos
			#(nueva.f1, nueva.f2, nueva.f3, nueva.f4, nueva.f5) = \
			#	nueva.calcularF(nueva.capaSali, nueva.pesoSali)
			#print "***F1", nueva.f1
			#print "***F2", nueva.f2
			#print "***F3", nueva.f3
			#print "***F4", nueva.f4
			#print "***F5", nueva.f5

	#print "-------------------------"
	print "PESO ENTRADA"
	print nueva.pesoEntra
	#print "-------------------------"
	#print "VALOR DE LA CAPA", nueva.capa
	#print "VALOR DE LA SALIDA", nueva.capaSali
	print "Peso capaSalida", nueva.pesoSali

main()
