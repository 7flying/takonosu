# -*- coding utf-8 -*-
from datetime import datetime
from flask import Flask, abort, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

# Flask general
app = Flask(__name__)

# Restful api
api = Api(app)


class SensorAPI(Resource):
	""" Class for the Sensor resource. """
	sensor_field = {
		'name': fields.String,
		'AD' : fields.String, # Analog or digital
		'pin': fields.Integer, # To witch pin it is connected
		'type': fields.String, # Read or write
		'refresh': fields.Integer # Ignore if unnecessary
	}

class DataAPI(Resource):
	""" Class to get data from a sensor. """
	data_field = {
		'value' : fields.Float,
		'unit': fields.String
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('node', type=str, location='form',
			required=True)
		self.reqparse.add_argument('sensor', type=str, location='form',
			required=True)
		super(DataAPI, self).__init__()

	def get(self):
		args = self.reqparse.parse_args()
		#ret = manager.get_value(args['node'], args['sensor'])
		ret = {}
		ret['value'] = 3.5
		ret['unit'] = "C"
		return {'data': marshal(ret, DataAPI.data_field)}

api.add_resource(DataAPI, '/takonosu/api/read')


class NodeAPI(Resource):
	""" Class for the Node resource. """
	node_field = {
		'name':fields.String,

	}

if __name__ == '__main__':
	app.run(debug=True)
