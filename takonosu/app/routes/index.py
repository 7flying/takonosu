from app import app
from flask import abort, redirect, url_for

"""
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
	def __init__(self, url_map, *items):
		super(RegexConverter, self).__init__(url_map)
		self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter
"""

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def page_not_found(e):
    # return app.send_static_file('index.html')
    return redirect('/')
"""

@app.route('/<regex(".+"):else>/')
def everything_else():
	return app.send_static_file('index.html')

"""
