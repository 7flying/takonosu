from app import app
from app import manager

def main():
	manager.populate() # Load test data
	app.run(debug = True, port=9000)

if __name__ == '__main__':
	main()

