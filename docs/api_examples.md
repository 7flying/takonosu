
#Node resource

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

* Create a new node:
  curl -X POST http://localhost:5000/takonosu/api/node -d "board_type=Arduino" -d "name=SUPER NODEEEE" -d "nic=Wifi"
  
  Response success:
  {
    "node": {
        "board_type": "Arduino", 
        "id": 1, 
        "name": "SUPER NODEEEE", 
        "nic": "Wifi", 
        "sensors": []
    }
  }

  Response error:
  {
 	 "code": 501, 
 	 "message": "DB error."
  }

* Modify an existing node:
  curl -X POST http://localhost:5000/takonosu/api/node -d "id=1" -d "board_type=Arduino" -d "name=SUPER NODEEEE" -d "nic=Wifi"





