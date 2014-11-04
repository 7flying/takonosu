# -*- coding utf-8 -*-
from datetime import datetime
from flask import Flask, abort, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

# Flask general
app = Flask(__name__)

# Restful api
api = Api(app)

""" Example usage """

class SensorAPI(Resource):
	""" Defines the api for a sensor:
		GET /takonosu/api/sensor/<int:id>
	"""
	# Defines how will the json be.
	sensor_field = {
	 'id' : fields.Integer,					# An integer field
	 'name' : fields.String,				# A string
	 'type' : fields.List(fields.String),	# List of strings
	 'lastValue' : fields.Float,			# Float
	 'retrievedAt' : fields.FormattedString("{hour}:{mins}:{secs}")	# Formated time
	}

	def __init_(self):
		super(SensorAPI, self).__init__()

	def get(self, id):
		""" Handles  GET /takonosu/api/sensor/<int:id>"""
		# sensor = some_method_doing_something_useful(id)
		# Imagine that this sensor is real
		time = datetime.now()
		sensor = { 'id' : id, 'name' : 'DHT22',  'type' : ['Temperature', 'Humidity'],
	 			   'lastValue' : 10.275, 'hour': time.strftime('%H'),
	 			    'mins': time.strftime('%M'), 'secs': time.strftime('%S')  
	 	}
	 	return { 'sensor' : marshal(sensor, SensorAPI.sensor_field) }

api.add_resource(SensorAPI, '/takonosu/api/sensor/<int:id>', endpoint='sensor')

""" End example """

if __name__ == '__main__':
	app.run(debug=True)
