from app import app
from app import manager

manager.populate() # Load test data
app.run(debug = True, port=9000)
