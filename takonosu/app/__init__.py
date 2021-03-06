# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__, static_url_path='')
app.config.from_object('config')

from app.routes import index

from datetime import datetime
from multiprocessing.pool import ThreadPool
from threading import Thread
import time
from flask import Flask, abort, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import redis
import manager
import nic
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, BLUE_RATE
from connection import Connection
from etc import debug

# Restful api
api = Api(app)

# Redis database
db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Connections
pool = ThreadPool(processes=3)

# Serial port management
serial_connection = None

# Constants
BLUETOOTH = 'Bluetooth'
WIFI = 'Wifi'


class DataAPI(Resource):
	""" Class to get/send data from/to a sensor. """
	data_field = {
		'value' : fields.String,
		'unit': fields.String
	}
	
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('node', type=int)
		self.reqparse.add_argument('sensor', type=int)
		self.reqparse.add_argument('data', type=str)
		super(DataAPI, self).__init__()

	def get(self):
		"""
		Returns data form the specified node-sensor. 
		Needs:	node: the node
				sensor: the sensor to get data from
		"""
		args = self.reqparse.parse_args()
		print args
		if args['node'] != None and args['sensor'] != None:
			# From node select nic
			node = manager._get_node(args['node'])
			print node
			if node == None:
				abort(404)
			else:
				# From sensor get pin and signal
				sensor = manager.get_sensor(args['sensor'])
				print sensor
				if sensor == None:
					abort(404)
				else:
					if node['nic'] == BLUETOOTH:
						temp = serial_connection
						if temp == None:
							global serial_connection
							serial_connection = Connection(node['address'],
								BLUE_RATE)
						pin = sensor['pin'] if len(sensor['pin']) > 1 else '0' + sensor['pin']
						command = 'R' + sensor['signal'] + pin + 'X'
						ret = {}
						ret['unit'] = " "
						# Option 1
						global serial_connection
						async_result = pool.apply_async(
							nic.serial_read,
							(command, serial_connection))
						ret['value'] = async_result.get(timeout=1)
						# Option 2
						"""
						# remember to import Queue
						queue = Queue.Queue()
						t = Thread(target=serial_read,
							args=(command,
								serial_connection, queue))
						t.start()
						result = queue.get()
						ret['value'] = result
						"""
						return {'data': marshal(ret, DataAPI.data_field)}	
					elif node['nic'] == WIFI:
						print "GET DATA pin: ", node['address']
						print "GET DATA pin: ", sensor['pin']
						ip = node['address']
						data = {}
						data['value'] = nic.gpio_read(sensor['pin'], ip)
						data['unit'] = " "
						return {'data': marshal(data, DataAPI.data_field)}

	def put(self):
		"""
		Sends data to a sensor identified by its id.
		Needs: 	node: the node where the sensor is
				sensor: the id of the sensor
				data: the data to be sent
		"""
		args = self.reqparse.parse_args()
		print args
		if args['node'] != None and args['sensor'] != None and args['data']:
			# From node select nic
			node = manager._get_node(args['node'])
			if node == None:
				abort(404)
			else:
				# From sensor get pin and signal
				sensor = manager.get_sensor(args['sensor'])
				if sensor == None:
					abort(404)
				else:
					if node['nic'] == BLUETOOTH:
						global serial_connection
						temp = serial_connection
						if temp == None:
							global serial_connection
							serial_connection = Connection(
								node['address'], BLUE_RATE)
						pin = sensor['pin'] if len(sensor['pin']) > 1 else '0' + sensor['pin']
						command = 'W' + sensor['signal'] + pin + args['data'] + 'X'
						global serial_connection
						thread = Thread(target=nic.serial_write,
							args=(command, serial_connection))
						thread.start()
					elif node['nic'] == WIFI:
						ip = node['address']
						pin = sensor['pin']
						data = args['data']
						thread = Thread(target=nic.gpio_write,
							args=(pin, ip, data))
						thread.start()

api.add_resource(DataAPI, '/takonosu/api/data', endpoint='data')


class SensorAPI(Resource):
	""" Class for the Sensor resource. """
	sensor_field = {
		'id': fields.Integer,
		'name': fields.String,
		'signal' : fields.String, # Analog or digital
		'pin': fields.Integer, # To witch pin it is connected
		'direction': fields.String, # Read or write
		'refresh': fields.String # Ignore if unnecessary
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('id', type=int, required=True)
		self.reqparse.add_argument('name', type=str)
		self.reqparse.add_argument('signal', type=str)
		self.reqparse.add_argument('pin', type=int)
		self.reqparse.add_argument('direction', type=str)
		self.reqparse.add_argument('refresh', type=int)
		super(SensorAPI, self).__init__()

	def get(self):
		""" Gets a sensor given its id. """
		args = self.reqparse.parse_args()
		id = str(args['id'])
		ret = manager.get_sensor(id)
		return { 'sensor' : marshal(ret, SensorAPI.sensor_field)}

	def put(self):
		""" Updates a sensor. """
		sensor = {}
		args = self.reqparse.parse_args()
		sensor['id'] = args['id']
		sensor['name'] = args['name']
		sensor['signal'] = args['signal']
		sensor['pin'] = args['pin']
		sensor['direction'] = args['direction']
		sensor['refresh'] = args['refresh']
		manager.modify_sensor(sensor) # Boolean on the future
		return jsonify(message="Sensor modified", code=201)

api.add_resource(SensorAPI, '/takonosu/api/sensor', endpoint='sensor')


class NodesAPI(Resource):
	""" Class for the Node resource. """
	node_field = {
		'id': fields.Integer,
		'name':fields.String,
		'board_type': fields.String,
		'nic': fields.String,
		'sensors' : fields.List(fields.Nested(SensorAPI.sensor_field)) 
	}

	node_field_address = {
		'id': fields.Integer,
		'name':fields.String,
		'board_type': fields.String,
		'nic': fields.String,
		'address': fields.String,
		'sensors' : fields.List(fields.Nested(SensorAPI.sensor_field)) 
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('id', type=int)
		self.reqparse.add_argument('name', type=str)
		self.reqparse.add_argument('board_type', type=str)
		self.reqparse.add_argument('nic', type=str)
		self.reqparse.add_argument('address', type=str)
		
		super(NodesAPI, self).__init__()

	def get(self):
		""" Returns all the nodes + sensors on the db. """
		args = self.reqparse.parse_args()
		if args['id'] == None: # We want al the nodes
			nodes = manager.get_nodes()
			return jsonify(nodes=nodes)
		elif args['id'] != None: 
			# We usually want to pair with this node if it has bluetooth
			node = manager.get_node(args['id'])
			if node['nic'] == BLUETOOTH:
				# Unpair the last one
				global serial_connection
				temp = serial_connection
				if temp != None:
					global serial_connection
					serial_connection.close()
				global serial_connection
				serial_connection = None
				global serial_connection
				serial_connection = Connection(node['address'], BLUE_RATE)
			if node.get('address', None) != None:
				return {'node' : marshal(node, NodesAPI.node_field_address)} 
			else:
				return {'node' : marshal(node, NodesAPI.node_field)}
		else:
			abort(400)

	def post(self):
		""" Creates a new node."""
		args = self.reqparse.parse_args()
		node = {}
		node['name'] = args['name']
		node['board_type'] = args['board_type']
		node['nic'] = args['nic']
		if args.get('address', None) != None:
			node['address'] = args['address']
		node['sensors'] = []
		result = manager.insert_node(node)
		created = manager.get_node(result)
		if created.get('address', None) != None:
			return {'node' : marshal(created, NodesAPI.node_field_address)}	
		else:
			return {'node' : marshal(created, NodesAPI.node_field)}

	def put(self):
		""" Edit a Node."""
		args = self.reqparse.parse_args()
		if args['id'] != None:
			node = {}
			node['id'] = args['id']
			node['name'] = args['name']
			node['board_type'] = args['board_type']
			node['nic'] = args['nic']
			if args.get('address', None) != None:
				node['address'] = args['address']
			result = manager.modify_node(node)
			if result:
				return jsonify(message="Node modified", code=201)
			else:
				return jsonify(message="DB error on node modification", code=501)
		else:
			abort(400)

	def delete(self):
		""" Deletes a node and all its sensors. """
		args = self.reqparse.parse_args()
		if args['id'] != None:
			manager.delete_node(args['id'])
			return jsonify(message="Node deleted", code=201)
		else:
			abort(400)

api.add_resource(NodesAPI, '/takonosu/api/nodes', endpoint='nodes')


class NodeSensorsAPI(Resource):
	""" Class to interact with the sensors of a node. """

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('identifier', type=int)
		self.reqparse.add_argument('id', type=int) # NODE id
		self.reqparse.add_argument('sensor_id', type=int)
		self.reqparse.add_argument('name', type=str)
		self.reqparse.add_argument('signal', type=str)
		self.reqparse.add_argument('pin', type=int)
		self.reqparse.add_argument('direction', type=str)
		self.reqparse.add_argument('refresh', type=int)
		super(NodeSensorsAPI, self).__init__()

	def get(self):
		""" Gets all the sensors of a certain node. """
		args =  self.reqparse.parse_args()
		if args['id'] != None:
			sensors = manager.get_sensors(args['id'])
			return jsonify(sensors=sensors)

	def post(self):
		""" Inserts a sensor to the node. """
		args =  self.reqparse.parse_args()
		if args['id'] == None:
			print "abortando"
			abort(400)
		else:
			sensor = {}
			sensor['name'] = args['name']
			sensor['signal'] = args['signal']
			sensor['pin'] = args['pin']
			sensor['direction'] = args['direction']
			sensor['refresh'] = args['refresh']
			print "insert sensor: " + str(sensor)
			new_sensor_id = manager.insert_sensor_to_node(args['id'], sensor)
			return jsonify(sensor=manager.get_sensor(new_sensor_id))

	def delete(self):
		""" Deletes a sensor from a node. """
		args = self.reqparse.parse_args()
		if args['id'] != None and args['sensor_id'] != None:
			manager.delete_sensor_from_node(args['id'], args['sensor_id'])
			return jsonify(message="Sensor deleted from node", code=201)

api.add_resource(NodeSensorsAPI, '/takonosu/api/nodes/sensors',
	endpoint='sensors')
