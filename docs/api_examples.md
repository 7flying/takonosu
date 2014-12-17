
#Sensor resource

```
/takonosu/api/sensor
```

* GET, {id:int}: Gets a sensor by its id
* PUT, {id:int, name:str, signal:str, pin:id, direction:str, refresh:int}


#Node resource

```
/takonosu/api/nodes
```

* GET,    {id:int} : Gets a node by its id 
          {}        : Gets all the nodes
* POST,   {name:str, board_type:str, nic:str}: inserts a node
* PUT,    {id:int, name:str, board_type:str, nic:str}: edits a node
* DELETE, {id:int}  : deletes a node

#Node-sensors resource

```
/takonosu/api/nodes/<int:id>/sensors
```

* GET,    gets all the sensors of a node
* POST,   {name:str, signal:str, pin:int, direction:str, refresh:int}:  Inserts a sensor to a node
* DELETE, {sensor_id:int}: deletes a sensor from a node
