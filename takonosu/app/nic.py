# -*- coding: utf-8 -*-
import socket
from config import S_PORT


# Serial
def serial_read(command, serial_con, queue=""):
	"""Read from serial. """
	serial_con.write(command)
	result = serial_con.read()
	#queue.put(result)
	return result
	
def serial_write(command, serial_con):
	"""Write to serial. """
	serial_con.write(command)

# Sockets
def gpio_read(gpio, ip):
	"""Reads from gpio at the ip."""
	print "on gpio_read"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, S_PORT))
	print "connected to socket"
	s.sendall('R' + ':' + str(gpio) + ':X' )
	print "data sent"
	data = s.recv(256)
	print "data received"
	s.close()
	print "[SOCKET] received: ", data
	return data

def gpio_write(gpio, ip, value):
	"""Writes to gpio at the ip."""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, S_PORT))
	s.sendall('W' + ':' + str(gpio) + ':' + str(value) + ':X')
	data = s.recv(256) # Expected 'ok'
	s.close()

