#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
import sqlite3
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from reportlab.pdfgen import canvas
import datetime
import os
__author__ = "Eva Hu Garres"
__copyright__ = "Copyright 2016, Eva Hu Garres"
__credits__ = ["Eva Hu Garres", "Alejandro López García"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Eva Hu Garres"
__email__ = "evahugarres@gmail.com"
__status__ = "Production"

# Cargar nuestro archivo .ui
main = uic.loadUiType(os.getcwd()+"/VirginiaStar/mainwindow.ui")[0]
recibo = uic.loadUiType(os.getcwd()+"/VirginiaStar/recibos.ui")[0]
consulta = uic.loadUiType(os.getcwd()+"/VirginiaStar/consulta.ui")[0]
inventario = uic.loadUiType(os.getcwd()+"/VirginiaStar/inventario.ui")[0]
meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
anos  = ["2016","2017","2018","2019"]
class MyWindowClass(QtWidgets.QMainWindow, main):
	def __init__(self, parent=None):
		QtWidgets.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.btn_Guardar.clicked.connect(self.btn_Guardar_clicked)
		self.btn_Cargar.clicked.connect(self.btn_Cargar_clicked)
		self.btn_Crear_2.clicked.connect(self.btn_Crear_clicked)
		self.recibos.triggered.connect(self.registro_a_recibo)
		self.consultar.triggered.connect(self.registro_a_consulta)
		self.inventario.triggered.connect(self.registro_a_inventario)
		self.setWindowTitle("VirginiaStarApp")
		self.IniciarBase()
	


	def IniciarBase(self):
		self.con = sqlite3.connect("/Users/evahugarres/VirginiaStar/prueba.bd")
		self.cursor = self.con.cursor()
		self.cursor.execute ("""CREATE TABLE IF NOT EXISTS Usuarios(ID INTEGER PRIMARY KEY,
																NOMBRE TEXT NOT NULL, 
																APELLIDO TEXT NOT NULL, 
																DIRECCION TEXT NOT NULL,
																LOCALIDAD TEXT NOT NULL,
																NIF TEXT NOT NULL,
																FECHA_NAC TEXT NOT NULL,
																FECHA_ALTA TEXT NOT NULL,
																FECHA_BAJA TEXT NOT NULL,
																DIAS_LIMITE TEXT NOT NULL)""" )

		self.cursor.execute ("""CREATE TABLE IF NOT EXISTS Facturas(ID INTEGER,
																	PRECIO INTEGER NOT NULL,
																	FECHA INTEGER,
																	FOREIGN KEY (ID) REFERENCES Usuarios (ID)
																	)""" )
		self.con.commit()

	# Evento del boton Guardar
	def btn_Guardar_clicked(self):

		self.con = sqlite3.connect("/Users/evahugarres/VirginiaStar/prueba.bd")
		self.cursor = self.con.cursor()

	# Datos
		self.nombre = self.lineEdit.text()
		self.apellido = self.lineEdit_2.text()
		self.localidad =self.lineEdit_4.text()
		self.direccion = self.lineEdit_3.text()
		self.nif = self.lineEdit_5.text()
		self.fecha_nac = self.lineEdit_6.text()
		self.fecha_alta = str(datetime.datetime.now())
		self.fecha_baja = ""
		self.dias_limite = self.lineEdit_10.text()

		if self.nombre == "" or self.apellido =="" or self.localidad=="" or self.direccion=="" or self.nif=="" or self.fecha_nac=="" or self.dias_limite == "":
			ret = QtWidgets.QMessageBox.critical(self, "Error",'''Debes rellenar todos los campos.''', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)
		else:
			self.datos = (self.nombre, self.apellido, self.localidad, self.direccion,self.nif, self.fecha_nac, self.fecha_alta, self.fecha_baja, self.dias_limite)

		# Inserta los datos en la tabla campos
			self.cursor.execute("INSERT INTO Usuarios (nombre, apellido, direccion,localidad,nif,fecha_nac,fecha_alta,fecha_baja,dias_limite) VALUES (?,?,?,?,?,?,?,?,?)", self.datos)
			self.con.commit()
		# Quedan los campos vacios al guardar cliente
			self.lineEdit.setText("")
			self.lineEdit_2.setText("")
			self.lineEdit_3.setText("")
			self.lineEdit_4.setText("")
			self.lineEdit_5.setText("")
			self.lineEdit_6.setText("")
			self.lineEdit_7.setText("")
			self.lineEdit_10.setText("")

			self.con.commit()
			self.con.close()

# Evento del boton Caragar
	def btn_Cargar_clicked(self):
		self.con = sqlite3.connect("/Users/evahugarres/VirginiaStar/prueba.bd")
		self.cursor = self.con.cursor()

# Se cargan los datos indicados de la tabla
		self.cursor.execute("SELECT ID, NOMBRE, APELLIDO FROM Usuarios")

# Al presionar el boton lo primero es borrar todos los datos
		self.lista.clear()

# Se agregan los elementos al QListWidget
		for i in self.cursor:
			self.id = str(i[0])
			self.nombre = i[1]
			self.apellido =  i[2]
			self.lista.addItem(self.id + " - " + self.nombre + " - " + self.apellido)
			self.con.commit()
		self.con.close()

	def btn_Crear_clicked(self):     
		# Ruta donde quiero crear el PDF
		c = canvas.Canvas(os.getcwd()+"/VirginiaStar/GymVirginia.pdf")
		c.drawImage(os.getcwd()+'VirginiaStar/GymVirginia.jpg', 0, 0, 321, 188)
		c.drawString(100,70,("Nombre: "+ self.nombre))
		c.drawString(100,40,("Apellido: "+ self.apellido))
		#c.drawString(100,660,("Id: "+ self.id))
		c.save()

	def registro_a_recibo(self):
		window = Recibos(self)
		self.close()
		window.show()
	def registro_a_consulta(self):
		window = Consulta(self)
		self.close()
		window.show()
	def registro_a_inventario(self):
		window = Inventario(self)
		self.close()
		window.show()

""" ESTO ES OTRA CLASE; OTRA VENTANA """

class Recibos(QtWidgets.QMainWindow, recibo):
	def __init__(self, parent=None):
		QtWidgets.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.actionRegistrar.triggered.connect(self.recibo_a_registro)
		self.consultar.triggered.connect(self.recibo_a_consulta)
		self.inventario.triggered.connect(self.recibo_a_inventario)
		self.btn_Guardar.clicked.connect(self.btn_Guardar_clicked)
		self.btn_Cargar.clicked.connect(self.btn_Cargar_clicked)
		self.setWindowTitle("VirginiaStarApp")
		
	def recibo_a_registro(self):
		window = MyWindowClass(self)
		self.close()
		window.show()
	def recibo_a_consulta(self):
		window = Consulta(self)
		self.close()
		window.show()
	def recibo_a_inventario(self):
		window = Inventario(self)
		self.close()
		window.show()

	def btn_Guardar_clicked(self):
		self.nombre = self.lineEdit.text()
		self.apellido = self.lineEdit_2.text()
		self.mes = self.lineEdit_3.text()
		self.importe = self.lineEdit_4.text()
		if self.nombre == "" or self.apellido == "" or self.importe == "":
			ret = QtWidgets.QMessageBox.critical(self, "Error",'''Debes rellenar todos los campos.''', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)
		else:

			self.datos = (self.nombre,self.apellido)

			self.con = sqlite3.connect("/Users/evahugarres/VirginiaStar/prueba.bd")
			self.cursor = self.con.cursor()

	# Se cargan los datos indicados de la tabla
			self.cursor.execute("SELECT ID FROM Usuarios WHERE NOMBRE=? AND APELLIDO=?",self.datos)
			try:
				for i in self.cursor:
					self.id = str(i[0])
				self.mes = datetime.datetime.now() 

				self.datos = (self.id,self.mes, self.importe)

				self.cursor.execute("INSERT INTO Facturas (ID, FECHA, PRECIO) VALUES (?,?,?)", self.datos)

				self.con.commit()
				self.con.close()
				self.lineEdit.setText("")
				self.lineEdit_2.setText("")
				self.lineEdit_3.setText("")
				self.lineEdit_4.setText("")
			except:
				ret = QtWidgets.QMessageBox.critical(self, "Error",'''Ese usuario no existe. \n ¿Has introducido bien los datos?''', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)


	# Evento del boton Cargar
	def btn_Cargar_clicked(self):
		self.con = sqlite3.connect("/Users/evahugarres/VirginiaStar/prueba.bd")
		self.cursor = self.con.cursor()

# Se cargan los datos indicados de la tabla
		self.cursor.execute("SELECT NOMBRE, APELLIDO, FECHA FROM Usuarios INNER JOIN Facturas ON Usuarios.id = Facturas.id ORDER BY FECHA DESC")

# Al presionar el boton lo primero es borrar todos los datos
		self.lista.clear()

# Se agregan los elementos al QListWidget
		for i in self.cursor:
			self.mes = i[2]
			self.nombre = i[0]
			self.apellido = i[1]
			self.lista.addItem(self.mes + " - " + self.nombre + " - " + self.apellido)
			self.con.commit()
		self.con.close()

class Consulta(QtWidgets.QMainWindow, consulta):
	def __init__(self, parent=None):
		QtWidgets.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.facturas.triggered.connect(self.consulta_a_recibo)
		self.inventario.triggered.connect(self.consulta_a_inventario)
		self.actionRegistrar.triggered.connect(self.consulta_a_registro)
		self.btn_Buscar.clicked.connect(self.btn_Buscar_clicked)
		self.setWindowTitle("VirginiaStarApp")
		#self.IniciarBase()

	def consulta_a_registro(self):
		window = MyWindowClass(self)
		self.close()
		window.show()
	def consulta_a_recibo(self):
		window = Recibos(self)
		self.close()
		window.show()

	def consulta_a_inventario(self):
		window = Inventario(self)
		self.close()
		window.show()

	def btn_Buscar_clicked(self):

		self.id = ""
		self.direccion = ""
		self.localidad = ""
		self.nif = ""
		self.fecha_nac = ""
		self.fecha_alta = ""
		self.fecha_baja = ""
		self.dias_limite = ""

		self.nombre = self.lineEdit.text()
		self.apellido = self.lineEdit_2.text()
	
		self.datos = (self.nombre,self.apellido)
		if self.nombre == "" or self.apellido == "":
			ret = QtWidgets.QMessageBox.critical(self, "Error",'''Debes rellenar todos los campos.''', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)
		else:
			self.con = sqlite3.connect("/Users/evahugarres/VirginiaStar/prueba.bd")
			self.cursor = self.con.cursor()

			self.lineEdit_3.setText("")
			self.lineEdit_4.setText("")
			self.lineEdit_5.setText("")
			self.lineEdit_6.setText("")
			self.lineEdit_7.setText("")
			self.lineEdit_8.setText("")
			self.lineEdit_9.setText("")
			self.lineEdit_10.setText("")
			self.lineEdit_11.setText("")
			self.lineEdit_12.setText("")

			self.cursor.execute("SELECT ID,DIRECCION,LOCALIDAD,NIF,FECHA_NAC,FECHA_ALTA,FECHA_BAJA,DIAS_LIMITE FROM Usuarios WHERE NOMBRE=? AND APELLIDO=?",self.datos)
			try:
				for i in self.cursor:
					self.id = str(i[0])
					self.direccion = i[1]
					self.localidad = i[2]
					self.nif = i[3]
					self.fecha_nac = i[4]
					self.fecha_alta = i[5]
					self.fecha_baja = i[6]
					self.dias_limite = i[7]
					self.con.commit()
				
				self.lineEdit_3.setText(self.nombre)
				self.lineEdit_4.setText(self.apellido)
				self.lineEdit_5.setText(self.direccion)
				self.lineEdit_6.setText(self.localidad)
				self.lineEdit_7.setText(self.fecha_nac)
				self.lineEdit_8.setText(self.dias_limite)
				self.lineEdit_9.setText(self.fecha_alta)
				self.lineEdit_10.setText(self.fecha_baja)
				self.lineEdit_11.setText(self.id)
				self.lineEdit_12.setText(self.nif)
				self.lista.clear()

				self.cursor.execute("SELECT FECHA, PRECIO FROM Usuarios INNER JOIN Facturas ON Usuarios.id = Facturas.id WHERE Usuarios.ID = ? ORDER BY FECHA DESC",self.id)

				for i in self.cursor:

					self.mes = i[0]
					self.importe = i[1]

					self.lista.addItem(self.mes + " - " + str(self.importe) + " Euros")

				self.con.commit()
					
				self.con.close()
			except:
				self.lineEdit_3.setText("")
				self.lineEdit_4.setText("")
				self.lineEdit_5.setText("")
				self.lineEdit_6.setText("")
				self.lineEdit_7.setText("")
				self.lineEdit_8.setText("")
				self.lineEdit_9.setText("")
				self.lineEdit_10.setText("")
				self.lineEdit_11.setText("")
				self.lineEdit_12.setText("")
				ret = QtWidgets.QMessageBox.critical(self, "Error",'''Ese usuario no existe. \n ¿Has introducido bien los datos?''', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)


class Inventario(QtWidgets.QMainWindow, inventario):
	def __init__(self, parent=None):
		QtWidgets.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.facturas.triggered.connect(self.inventario_a_recibo)
		self.registro.triggered.connect(self.inventario_a_registro)
		self.consultar.triggered.connect(self.inventario_a_consulta)
		self.setWindowTitle("VirginiaStarApp")
		
		self.con = sqlite3.connect("/Users/evahugarres/VirginiaStar/prueba.bd")
		self.cursor = self.con.cursor()

		for n in meses:
			self.comboBox.addItem(n)

		for n in anos:
			self.comboBox_2.addItem(n)

		self.buscar.clicked.connect(self.btn_Buscar_clicked)
		self.todo.clicked.connect(self.btn_Todo_clicked)


	def inventario_a_registro(self):
		window = MyWindowClass(self)
		self.close()
		window.show()
	def inventario_a_recibo(self):
		window = Recibos(self)
		self.close()
		window.show()

	def inventario_a_consulta(self):
		window = Consulta(self)
		self.close()
		window.show()
	def btn_Buscar_clicked(self):
		self.lista.clear()
		self.mes = self.comboBox.currentIndex()
		self.ano = self.comboBox_2.currentText()
		self.mes = int(self.mes)
		if self.mes < 9:
			self.mes = str(self.mes+1)
			self.mes = "0"+ self.mes

		fecha = self.mes+"/"+str(self.ano)
		
		self.cursor.execute("SELECT * FROM Facturas WHERE FECHA = ?",(fecha,))

		total = 0

		for i in self.cursor:
			self.total = str(i[1])
			self.mes = i[2]
			self.lista.addItem(fecha + " - " + str(self.total) + " Euros.")
			self.con.commit()
			total = total + int(self.total)

		self.lista.addItem("Total a fecha de " + fecha + ": " + str(total) + " Euros.")
		

	def btn_Todo_clicked(self):
		self.lista.clear()
		self.cursor.execute("SELECT * FROM Facturas")
		total_final = 0
		for i in self.cursor:
			self.total = str(i[1])
			total_final += int(self.total)
			self.mes = i[2]
			self.lista.addItem(str(self.mes) + " - " + str(self.total) + " Euros.")
			self.con.commit()

		self.lista.addItem("Total:"+ str(total_final) + " Euros.")


app = QtWidgets.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.setWindowTitle("VirginiaStarApp")
MyWindow.show()
app.exec_()