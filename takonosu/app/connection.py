# -*- coding: utf-8 -*-
import serial

class Connection(object):
	
	def __init__(self, port_name, rate):
		self.serial = serial.Serial(port_name, rate)
		print self.serial.name

	def close(self):
		self.serial.close()

	def read(self):
		end = False
		ret = ''
		while not end:
			temp = self.serial.read(1)
			if temp == 'X':
				end = True
			else:
				ret += temp 
		# result = self.serial.read(10)
		print ret

	def write(self, command):
		print command
		self.serial.write(command)