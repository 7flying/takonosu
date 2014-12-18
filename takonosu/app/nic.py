# -*- coding: utf-8 -*-

def serial_read(command, serial_con, queue=""):
	print "Serial read"
	serial_con.write(command)
	print "resultado imprimido"
	result = serial_con.read()
	#queue.put(result)
	return result
	
def serial_write(command, serial_con):
	print "Serial write"
	serial_con.write(command)

def gpio_read(gpio):
	pass

def gpio_write(gpio, value):
	pass
