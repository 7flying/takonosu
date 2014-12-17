import sys
from app import app
from app import manager
from app.config import BLUE_PORT, BLUE_RATE

def main():
	manager.populate() # Load test data
	app.run(debug = True, port=9000)

if __name__ == '__main__':
	print sys.argv
	if len(sys.argv) > 1:
		BLUE_PORT = sys.argv[1]
		BLUE_RATE = int(sys.argv[2])
	main()

