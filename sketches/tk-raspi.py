# -*- coding: utf-8 -*-
import socket
import os
from threading import Thread

HOST = ''
PORT = 5432

def process(conn):
    """ Processes an incoming connection. """
    temp_buffer = ""
    end = False
    while not end:
        data = conn.recv(1)
        if data:
            if data != 'X':
                temp_buffer += data
            else:
                splited = temp_buffer.split(':')
                temp_buffer = ""
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
    """ Starts the server. """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((HOST, PORT))
    my_socket.listen(1)
    print " \n$ Server up and listening"
    while True:
        conn, addr = my_socket.accept()
        print 'Connected by', addr
        thread = Thread(target=process, args=(conn,))
        thread.start()

def _init_gpio(gpio, direction):
    """ Inits the gpio in the specified direction. """
    ret = True
    if not os.path.isdir('/sys/class/gpio/gpio' + str(gpio)):
        try:
            gpio_file = open('/sys/class/gpio/export', 'w')
            gpio_file.write(str(gpio))
            gpio_file.close()
            gpio_file = open('/sys/class/gpio/gpio' + str(gpio) + '/direction', 'w')
            gpio_file.write(str(direction))
            gpio_file.close()
        except IOError, error:
            print IOError, error
            ret = False
    return ret

def read_gpio(gpio):
    """ Reads from the gpio. """
    check = _init_gpio(gpio, 'in')
    if check:
        gpio = open('/sys/class/gpio/gpio' + str(gpio) + '/value', 'r')
        value = gpio.read()
        return value
    else:
        return 'Error reading'
    #return '23'

def write_gpio(gpio, value):
    """ Writes to gpio. """
    check = _init_gpio(gpio, 'out')
    if check:
        gpio = open('/sys/class/gpio/gpio' + str(gpio) + '/value', 'w')
        gpio.write(str(value))
        return 'Ok'
    else:
        return 'Error writing'
    #return 'Ok'

if __name__ == '__main__':
    run_server()
