from app import app
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
	def __init__(self, url_map, *items):
		super(RegexConverter, self).__init__(url_map)
		self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/')
def root():
    return app.send_static_file('index.html')
