# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__, static_url_path='')
app.config.from_object('config')

from app.routes import index

from datetime import datetime
from flask import Flask, abort, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import redis
import manager
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
# Restful api
api = Api(app)

# Redis database
db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

class DataAPI(Resource):
	""" Class to get/send data from/to a sensor. """
	data_field = {
		'value' : fields.Float,
		'unit': fields.String
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('node', type=int, location='form')
		self.reqparse.add_argument('sensor', type=int, location='form')
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

api.add_resource(DataAPI, '/takonosu/api/data',endpoint='data')


class SensorAPI(Resource):
	""" Class for the Sensor resource. """
	sensor_field = {
		'id': fields.Integer,
		'name': fields.String,
		'signal' : fields.String, # Analog or digital
		'pin': fields.Integer, # To witch pin it is connected
		'direction': fields.String, # Read or write
		'refresh': fields.Integer # Ignore if unnecessary
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

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('id', type=int)
		self.reqparse.add_argument('name', type=str)
		self.reqparse.add_argument('board_type', type=str)
		self.reqparse.add_argument('nic', type=str)
		super(NodesAPI, self).__init__()

	def get(self):
		""" Returns all the nodes + sensors on the db. """
		args = self.reqparse.parse_args()
		if args['id'] == None: # We want al the nodes
			nodes = manager.get_nodes()
			return jsonify(nodes=nodes)
		elif args['id'] != None:
			node = manager.get_node(args['id'])
			return {'node' : marshal(node, NodesAPI.node_field)}
		else:
			abort(400)	
	def post(self):
		""" Creates a new node."""
		node = {}
		node['name'] = args['name']
		node['board_type'] = args['board_type']
		node['nic'] = args['nic']
		node['sensors'] = []
		result = manager.insert_node(node)
		created = manager.get_node(result)
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
		self.reqparse.add_argument('sensor_id', type=int)
		self.reqparse.add_argument('name', type=str)
		self.reqparse.add_argument('signal', type=str)
		self.reqparse.add_argument('pin', type=int)
		self.reqparse.add_argument('direction', type=str)
		self.reqparse.add_argument('refresh', type=int)
		super(NodeSensorsAPI, self).__init__()

	def get(self, id):
		""" Gets all the sensors of a certain node. """
		sensors = manager.get_sensors(id)
		return jsonify(sensors=sensors)

	def post(self, id):
		""" Inserts a sensor to the node. """
		args = reqparse.parse_args()
		sensor = {}
		sensor['name'] = args['name']
		sensor['signal'] = args['signal']
		sensor['pin'] = args['pin']
		sensor['direction'] = args['direction']
		sensor['refresh'] = args['refresh']
		manager.insert_sensor_to_node(id, sensor)
		return jsonify(message="Sensor inserted to node", code=201)

	def delete(self, id):
		""" Deletes a sensor from a node. """
		args = reqparse.parse_args()
		if args['sensor_id'] != None:
			managet.delete_sensor_from_node(id, args['sensor_id'])
			return jsonify(message="Sensor deleted from node", code=201)

api.add_resource(NodeSensorsAPI, '/takonosu/api/nodes/<int:id>/sensors',
	endpoint='sensors')
