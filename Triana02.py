#!/usr/bin/python

global Zxpos = 230 #Valor deseado EN +X
global Zxneg = 30 #Valor deseado EN -X
global Zypos = 600 #Valor deseado EN +Y
global Zyneg = 40 #Valor deseado EN -Y
"""
Enviar valor de z, enviar valor de vector de pesos, enviar

******************DESCRIPCIONES*************************
Errores = [d1, d2, d3, dn]
z = valor deseado
vecP = vector de pesos
"""
#640x480
def enviarValores():
	#Zxpos = 600  #Valor deseado EN +X
	#Zxneg = 40 #Valor deseado EN -X
	#Zypos = 440 #Valor deseado EN +Y
	#Zyneg = 40 #Valor deseado EN -Y
	print '>>>Enviando valores...'
	vecP = [0.5, 0.6, 0.7, 0.8]
	print vecP[0]
	valorObtenidoX = int(raw_input('Ingresa el valor obtenido en X: '))
	valorObtenidoY = int(raw_input('Ingresa el valor obtenido en Y: '))	
	err = Zxpos-valorObtenido
	err = Zxneg-valor
	error(err, vecP)

def error(err, vecP):
	vectorErrores = []
	#Errores = [d1, d2, d3, dn]
	#z = valor deseado
	#vecP = vector de pesos
	"""
	Se debe tener: dx1, dx2, dx3, dx4, dx5
	Se debe tener: dy1, dy2, dy3, dy4, dy5
	"""
	print err
	print vecP
	#return vectorErrores

def main():
	enviarValores()

main()
