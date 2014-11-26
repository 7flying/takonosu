# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__, static_url_path='')
app.config.from_object('config')

from app.routes import index

from datetime import datetime
from flask import Flask, abort, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

# Restful api
api = Api(app)


class DataAPI(Resource):
	""" Class to get/send data from/to a sensor. """
	data_field = {
		'value' : fields.Float,
		'unit': fields.String
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('node', type=int, location='form',
			required=True)
		self.reqparse.add_argument('sensor', type=int, location='form',
			required=True)
		self.reqparse.add_argument('data', type=str, location='form')
		super(DataAPI, self).__init__()

	def get(self):
		"""
		Returns data form the specified node-sensor. 
		Needs:	node: the node
				sensor: the sensor to get data from
		"""
		args = self.reqparse.parse_args()
		#ret = manager.get_value(args['node'], args['sensor'])
		ret = {}
		ret['value'] = 3.5
		ret['unit'] = "C"
		return {'data': marshal(ret, DataAPI.data_field)}

	def put(self):
		"""
		Sends data to a sensor identified by its id.
		Needs: 	node: the node where the sensor is
				sensor: the id of the sensor
				data: the data to be sent
		"""
		args = self.reqparse.parse_args()
		response = 'Data sent.'
		# response = someModule.send_data(args['node'], args['sensor'], args['data'])
		return jsonify(message=response)

api.add_resource(DataAPI, '/takonosu/api/data')


class SensorAPI(Resource):
	""" Class for the Sensor resource. """
	sensor_field = {
		'id': fields.Integer,
		'name': fields.String,
		'AD' : fields.String, # Analog or digital
		'pin': fields.Integer, # To witch pin it is connected
		'type': fields.String, # Read or write
		'refresh': fields.Integer # Ignore if unnecessary
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('id', type=str, location='form')
		super(SensorAPI, self).__init__()

	def get(self):
		""" Gets a sensor given its id. """
		args = self.reqparse.parse_args()
		id = args['id']
		# ret = manager.get_sensor(id)
		ret = {}
		ret['id'] = id
		ret['name'] = 'TMP36'
		ret['AD'] = 'D'
		ret['pin'] = 5
		ret['type'] = 'R'
		ret['refresh'] = 3000
		return { 'sensor' : marshal(ret, SensorAPI.sensor_field)}

api.add_resource(SensorAPI, '/takonosu/api/sensor')


class NodeAPI(Resource):
	""" Class for the Node resource. """
	node_field = {
		'id': fields.Integer,
		'name':fields.String,
		'board_type': fields.String,
		'nic': fields.String, # Tipo de comunicación
		'sensors' : fields.List(fields.Nested(SensorAPI.sensor_field)) 
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('id', type=str, location='form')
		self.reqparse.add_argument('name', type=str, location='form')
		self.reqparse.add_argument('board_type', type=str, location='form')
		self.reqparse.add_argument('nic', type=str, location='form')
		super(NodeAPI, self).__init__()

	def get(self):
		""" Returns a node by its id. """
		args = self.reqparse.parse_args()
		id = args['id']
		node = {}
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
		sensors.append(sensor)
		node['sensors'] = sensors
		if id == None:
			nodes = []
			id = 5
			# node = manager.get_node(id) # Returns full node object + its sensors	
			nodes.append(node)
			nodes.append(node)
			return jsonify(nodes= nodes)
		else:
			# node = manager.get_node(id) # Returns full node object + its sensors
			node['id'] = id
			return {'node' : marshal(node, NodeAPI.node_field)}

	def post(self):
		""" Creates a new node."""
		args = self.reqparse.parse_args()
		node = {}
		node['name'] = args['name']
		node['board_type'] = args['board_type']
		node['nic'] = args['nic']
		#result = manager.create_node(args['name'], args['board_type'],
		#	args['nic'])
		result = 1
		if result != -1:
			node['id'] = result
			node['sensors'] = []
			#ret = manager.get_node(result)
			return {'node': marshal(node, NodeAPI.node_field)}
		else:
			return jsonify(message="DB error.", code=501)

	def put(self):
		""" Edit a"""

api.add_resource(NodeAPI, '/takonosu/api/node')
