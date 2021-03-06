# -*- coding: utf-8 -*-
from __init__ import db
import random
from etc import debug

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
N_ADDR		= 'address'

S_ID 		= 'id'
S_NAME		= 'name'
S_SIGNAL	= 'signal'
S_PIN		= 'pin'
S_DIRECTION = 'direction'
S_REFRESH	= 'refresh'

##########

CODE = 'MANAGER'

# Nota: A Sesma le molesta que AD se llame AD, depende de como me de el aire
# cambiamos AD a signal o no.

def populate():
	""" Test data """
	db.flushdb()
	"""
	print "[ MANAGER ]: Inserting test data"
	nic = ['Bluetooth', 'Wifi', 'Xbee']
	boards = ['Arduino UNO', 'Arduino Nano', 'Arduino Micro', 'BeagleBone Black',
		'Raspberry Pi A+', 'Raspberry Pi B+', 'Trinket Pro', 'Waspmote']
	signal = ['A', 'D']
	direction = ['R', 'W']
	for i in range(1, 5):
		node = {}
		node[N_NAME] = "Super Node " + str(i)
		node[N_BOARD] = boards[random.randint(0, len(boards) - 1)]
		node[N_NIC] = nic[random.randint(0, len(nic) - 1)]
		sensors = []
		for j in range(0, 3):
			sensor = {}
			sensor[S_NAME] = 'TMP3' + str(j)
			sensor[S_SIGNAL] = signal[random.randint(0, len(signal) - 1)]
			sensor[S_PIN] = random.randint(0, 10)
			sensor[S_DIRECTION] = direction[random.randint(0, len(direction) - 1)]
			sensor[S_REFRESH] = 1000 * random.randint(1, 10)
			sensors.append(sensor)
		node[N_SENSORS] = sensors
		insert_node(node)
	"""
	"""
	node = {}
	node[N_NAME] = "Testing Node "
	node[N_BOARD] = 'Arduino Uno'
	node[N_NIC] = 'Bluetooth'
	node[N_ADDR] = '/dev/ttyACM0'
	sensors = []
	sensor = {}
	sensor[S_NAME] = 'TESTING SENSOR'
	sensor[S_SIGNAL] = 'D'
	sensor[S_PIN] = '7'
	sensor[S_DIRECTION] = 'W'
	sensor[S_REFRESH] = '1000'
	"""
	"""
	sensor2 = {}
	sensor2[S_NAME] = 'TESTING sensor2'
	sensor2[S_SIGNAL] = 'A'
	sensor2[S_PIN] = '1'
	sensor2[S_DIRECTION] = 'R'
	sensor2[S_REFRESH] = 10000
	sensors.append(sensor2)
	"""
	"""
	sensors.append(sensor)
	node[N_SENSORS] = sensors
	insert_node(node)
	print "[ MANAGER ]: Test data added."
	"""

## Keys ##

def _increment_key_sensor():
	""" Increments the primary key of the sensors. """
	ret = db.incr(KEY_AUTO_SENSOR_ID)
	return str(ret)

def _increment_key_node():
	""" Increments the primary key of the nodes. """
	ret = db.incr(KEY_AUTO_NODE_ID)
	return str(ret)

## Existence check ##

def _does_sensor_exist(sensor_id):
	pass

def _does_node_exist(node_id):
	pass

##  Nodes & Sensors ##

def insert_node(node):
	"""
	Inserts a node into the db.
	If the node has sensors they are also inserted.
	Returns the new node's id
	"""
	debug(CODE, "INSERT NODE: (node): " + str(node))
	id = _increment_key_node()
	debug(CODE, "INSERT NODE: assigned id: " + str(id))
	db.hset(KEY_NODES + id, N_ID, id)
	db.hset(KEY_NODES + id, N_NAME, node[N_NAME])
	db.hset(KEY_NODES + id, N_BOARD, node[N_BOARD])
	db.hset(KEY_NODES + id, N_NIC, node[N_NIC])
	db.hset(KEY_NODES + id, N_SENSORS, id)
	if node.get(N_ADDR, None) != None:
		debug(CODE, "INSERT NODE: The node has an address")
		db.hset(KEY_NODES + id, N_ADDR, node[N_ADDR])
	if node.get(N_SENSORS) != None:
		debug(CODE, "INSERT NODE: The node has sensors")
		for sensor in node[N_SENSORS]:
			insert_sensor_to_node(id, sensor)
	return id

def delete_node(id):
	"""
	Deletes a node from the db as well as all the sensors related to the node.
	"""
	debug(CODE, "DELETE NODE: (id): " + str(id))
	id = str(id)
	sensors = set(db.smembers(KEY_LIST_SENSORS_IN_NODE + id))
	for id_sensor in sensors:
		delete_sensor_from_node(id, id_sensor)
	db.delete(KEY_LIST_SENSORS_IN_NODE + id)
	db.delete(KEY_NODES + id)

def modify_node(new_node):
	""" Modifies simple data (name, board_type, nic) from the node. """
	db.hset(KEY_NODES + str(new_node[N_ID]), N_NAME, new_node[N_NAME])
	db.hset(KEY_NODES + str(new_node[N_ID]), N_BOARD, new_node[N_BOARD])
	db.hset(KEY_NODES + str(new_node[N_ID]), N_NIC, new_node[N_NIC])
	if new_node.get(N_ADDR, None) != None:
		db.hset(KEY_NODES + str(new_node[N_ID]), N_ADDR, new_node[N_ADDR])
	return True

def get_node(node_id):
	""" Returns the node given the id, as well as all its sensors. """
	debug(CODE, "GET NODE: (id): " + str(node_id))
	node = db.hgetall(KEY_NODES + str(node_id))
	sensors = get_sensors(node_id)
	if sensors and len(sensors) > 0:
		debug(CODE, "GET NODE: The node has sensors")
		node[N_SENSORS] = sensors
	elif node:
		node[N_SENSORS] = []
	debug(CODE, "GET NODE: (return): " + str(node))
	return node

def _get_node(node_id):
	node = db.hgetall(KEY_NODES + str(node_id))
	return node

def get_nodes():
	""" Returns every node and sensor in the db. """
	debug(CODE, "GET NODES")
	ret = []
	max_id = 0 if db.get(KEY_AUTO_NODE_ID) == None \
		or len(db.get(KEY_AUTO_NODE_ID)) == 0 else int(db.get(KEY_AUTO_NODE_ID))
	debug(CODE, "GET NODES max_id:" + str(max_id))	
	for i in range(1, max_id + 1):
		node = get_node(i)
		if node:
			ret.append(node)
	return ret

def get_sensors(node_id):
	""" Returns the list of sensors of a node."""
	sensors = []
	for sensor_id in db.smembers(KEY_LIST_SENSORS_IN_NODE + str(node_id)):
		sensor = get_sensor(sensor_id)
		if sensor[S_ID] == 0:
			sensor = None
		if sensor != None:
			sensors.append(sensor)
	return sensors

def get_sensor(sensor_id):
	""" Gets a sensor given its id. """
	debug(CODE, "GET SENSOR: params (id):" + str(sensor_id))
	data = db.hgetall(KEY_SENSORS + str(sensor_id))
	if data.get(S_ID, None) == None:
		debug(CODE, "GET SENSOR: return None")
		return None
	else:
		debug(CODE, "GET SENSOR: return: " + str(data))	
		return data

def _insert_sensor(sensor):
	"""
	Inserts a sensor to the db.
	Returns the new generated id for the sensor.
	"""
	debug(CODE, "INSERT SENSOR: params (sensor):" + str(sensor))
	id = _increment_key_sensor()
	debug(CODE, "INSERT SENSOR: generated id:" + str(id))
	db.hset(KEY_SENSORS + id, S_ID, id)
	db.hset(KEY_SENSORS + id, S_NAME, sensor[S_NAME])
	db.hset(KEY_SENSORS + id, S_SIGNAL, sensor[S_SIGNAL])
	db.hset(KEY_SENSORS + id, S_PIN, str(sensor[S_PIN]))
	db.hset(KEY_SENSORS + id, S_DIRECTION, sensor[S_DIRECTION])
	if sensor.get(S_REFRESH, None) != None and len(str(sensor[S_REFRESH])) > 0:
		db.hset(KEY_SENSORS + id, S_REFRESH, str(sensor[S_REFRESH]))
	return id

def insert_sensor_to_node(node_id, sensor):
	""" Adds a new sensor to the node. """
	debug(CODE, "INSERT SENSOR TO NODE: params (node_id, sensor):" + \
		str(node_id) + " " + str(sensor))
	sensor_id = _insert_sensor(sensor)
	db.sadd(KEY_LIST_SENSORS_IN_NODE + str(node_id), sensor_id)
	return sensor_id

def delete_sensor_from_node(node_id, sensor_id):
	""" Deletes a sensor from the node."""
	db.srem(KEY_LIST_SENSORS_IN_NODE + str(node_id), str(sensor_id))
	db.delete(KEY_SENSORS + str(sensor_id))

def modify_sensor(new_sensor):
	""" Modifies the sensor's data."""
	db.hset(KEY_SENSORS + new_sensor[S_ID], S_NAME, new_sensor[S_NAME])
	db.hset(KEY_SENSORS + new_sensor[S_ID], S_SIGNAL, new_sensor[S_SIGNAL])
	db.hset(KEY_SENSORS + new_sensor[S_ID], S_PIN, str(new_sensor[S_PIN]))
	db.hset(KEY_SENSORS + new_sensor[S_ID], S_DIRECTION, new_sensor[S_DIRECTION])
	db.hset(KEY_SENSORS + new_sensor[S_ID], S_REFRESH, str(new_sensor[S_REFRESH]))
