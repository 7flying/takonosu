
* Obtain a node by its id:
  curl -X GET http://localhost:5000/takonosu/api/node -d "id=3"
  Response:
  	{
    	"node": {
        	"board_type": "Arduino UNO", 
        	"id": 3, 
        	"name": "Super Node Zero", 
        	"nic": "Bluetooth", 
        	"sensors": [
        	    {
            	    "AD": "D", 
            	    "id": 3, 
            	    "name": "TMP36", 
            	    "pin": 5, 
            	    "refresh": 3000, 
            	    "type": "R"
            	}
        	]
    	}
	}

