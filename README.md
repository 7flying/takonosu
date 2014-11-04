Takonosu - 蛸の巣
=================

WORK IN PROGRESS

Takonosu - 蛸の巣 - Nest of octopus

###Install

#####Server requirements


- Must have python 2.7 and pip.
- Flask & Flask-RESTful
  Install those two by:

  ```
  pip install -r requirements.txt
  ```

###Play

Start server

```
python server.py
```

Then should be running at localhost:5000.

Go to:

```
http://localhost:5000/takonosu/api/sensor/1
```
To get:
```
{
    "sensor": {
        "id": 1, 
        "lastValue": "10.275", 
        "name": "DHT22", 
        "retrievedAt": "15:25:47", 
        "type": [
            "Temperature", 
            "Humidity"
        ]
    }
}
```

or
```bash
curl -X GET -i http://localhost:5000/takonosu/api/sensor/1
```
To get:
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 217
Server: Werkzeug/0.9.6 Python/2.7.6
Date: Tue, 04 Nov 2014 18:49:55 GMT

{
    "sensor": {
        "id": 1, 
        "lastValue": "10.275", 
        "name": "DHT22", 
        "retrievedAt": "19:49:55", 
        "type": [
            "Temperature", 
            "Humidity"
        ]
    }
}

```


