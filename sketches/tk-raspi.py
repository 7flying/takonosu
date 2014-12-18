# -*- coding: utf-8 -*-
import socket
import os
from threading import Thread

HOST = ''
PORT = 5432

def process(conn):
	buffer = ""
	end = False
	while not end:
		data = conn.recv(1)
		if data:
			if data != 'X':
				buffer += data
			else:
				splited = buffer.split(':')
				buffer = ""
				if len(splited) > 0:
					direction = splited[0]
					if direction == 'R':
						print "Requested READ"
						ret = read_gpio(str(splited[1]))
						print "Sending %s\n" % ret
						conn.sendall(ret)
						print "Sended"
					elif direction == 'W':
						print "Requested WRITE"
						ret = write_gpio(str(splited[1]), str(splited[2]))
						print "Sending %s\n" % ret
						conn.sendall(ret)
						print "Sended"
					end = True
					conn.close()

def run_server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1)
	print " \n$ Server up and listening"
	while True:
		conn, addr = s.accept()
		print 'Connected by', addr
		thread = Thread(target=process, args=(conn,))
		thread.start()
		

def _init_gpio(gpio, direction):
	ret = True
	if not os.path.isdir('/sys/class/gpio/gpio' + str(gpio)):
		try:
			f = open('/sys/class/gpio/export')
			f.write(str(gpio))
			f.close()
			f = open('/sys/class/gpio/gpio' + str(gpio) + '/direction')
			f.write(str(direction))
			f.close()
		except IOError:
			ret = False
	return ret

def read_gpio(gpio):
	"""
	ok = _init_gpio(gpio, 'input')
	if ok:
		gpio = open('/sys/class/gpio/gpio' + str(gpio) + '/value')
		value = gpio.read()
		return value
	else:
		return 'Error reading'
	"""
	return '23'

def write_gpio(gpio, value):
	"""
	ok = _init_gpio(gpio, 'output')
	if ok:
		gpio = open('/sys/class/gpio/gpio' + str(gpio) + '/value')
		gpio.write(str(value))
		return 'Ok'
	else:
		return 'Error writing'
	"""
	return 'Ok'

if __name__ == '__main__':
	run_server()
