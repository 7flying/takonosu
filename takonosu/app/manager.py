# -*- coding: utf-8 -*-
from __init__ import db


## DB-Keys ##

KEY_NODES 	= "node:"
KEY_LIST_SENSORS_IN_NODE = "list-sensors:"
KEY_SENSORS	= "sensor:"

KEY_AUTO_NODE_ID 	= 'auto:node:id'
KEY_AUTO_SENSOR_ID 	= 'auto:sensor:id'

# Fields #

N_ID 		= 'id'
N_NAME 		= 'name'
N_BOARD 	= 'board_type'
N_NIC 		= 'nic' # Bluetooth, wifi
N_SENSORS 	= 'sensors'

S_ID 		= 'id'
S_NAME		= 'name'
S_SIGNAL	= 'signal'
S_PIN		= 'pin'
S_DIRECTION = 'direction'
S_REFRESH	= 'refresh'

##########

# Nota: A Sesma le molesta que AD se llame AD, depende de como me de el aire
# cambiamos AD a signal o no.

def populate():
	""" Test data """
	db.flush()
	"""
	node['name'] = "Super Node Zero"
		node['board_type'] = "Arduino UNO"
		node['nic'] = 'Bluetooth'
		sensors = []
		sensor = {}
		sensor['id'] = id
		sensor['name'] = 'TMP36'
		sensor['AD'] = 'D'
		sensor['pin'] = 5
		sensor['type'] = 'R'
		sensor['refresh'] = 3000
	"""
	pass

## Keys ##

def increment_key_sensor(pipe):
	pass

def increment_key_node(pipe):
	pass

##  Nodes & Sensors ##

def insert_node(node):
	pass

def delete_node(id):
	pass

def modify_node(new_node):
	pass

def insert_sensor_to_node(node_id, sensor):
	pass

def delete_sensor_from_node(node_id, sensor_id):
	pass

def modify_sensor(new_sensor):
	pass
