# -*- coding: utf-8 -*-
import serial

class Connection(object):
	
	def __init__(self, port_name, rate):
		self.serial = serial.Serial(port_name, rate)
		print self.serial.name

	def close(self):
		self.serial.close()

	def read(self):
		result = self.readLine()
		print result

	def write(self, command):
		self.serial.write(command)