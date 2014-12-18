# -*- coding: utf-8 -*-
import serial
import time

class Connection(object):
	
	def __init__(self, port_name, rate):
		self.serial = serial.Serial(port_name, rate)
		print self.serial.name

	def close(self):
		self.serial.close()

	def read(self):
		init = int(time.time())
		end = False
		ret = ''
		while not end:
			if int(time.time()) - init > 1000:
				end = True
			else:
				waiting = self.serial.inWaiting()
				if waiting > 0:
					temp = self.serial.read(1)
					if temp == 'X':
						end = True
					else:
						ret += temp
		return ret

	def write(self, command):
		print command
		self.serial.write(command)