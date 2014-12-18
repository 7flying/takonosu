angular.module('flagular')
  .controller('SensorCtrl', function ($scope, $stateParams, Node, SensorData) {
  
  $scope.newSensor = false;
  $scope.sensors = [];
  $scope.newSensorSignal = 'None';
  $scope.newSensorDirection = 'None';
  $scope.signalList = ['Analog', 'Digital'];
  $scope.directionList = ['Read', 'Write'];
  var signalSelection, directionSelection;

  var tempSensors = [];
  var requests = {};

  $scope.signalSelect = function(name) {
    $scope.newSensorSignal = name;
    if(name == $scope.signalList[0]) {
      signalSelection = 'A';
    } else {
      signalSelection = 'D';
    }
  }

  $scope.directionSelect = function(directionName) {
    $scope.newSensorDirection = directionName;
    if(directionName == $scope.directionList[0]) {
      directionList = 'R';
    } else {
      directionList = 'W';
    }
  }

  $scope.editSensor = function(index) {
    if($scope.sensors[index].edit) {
        $scope.sensors[index].edit = false;
        $scope.sensors[index] = tempSensors[index];
    }
    else
      $scope.sensors[index].edit = true;
  }

  $scope.sendData = function(sensor) {
    SensorData.sendData({
      'node': $stateParams.id,
      'sensor': sensor.id,
      'data': sensor.out
    }, function() {
      sensor.out = '';
    });
  }

  $scope.updateSensor = function(sensor) {
    sensor.edit = false;
  }

  $scope.createNewSensor = function() {
    if($scope.newSensor) {
      $scope.newSensor = false;
    } else {
      $scope.newSensor = true;
    }
  }

  $scope.createSensor = function() {
    if($scope.newSensor) {
      $scope.newSensor = false;
      Node.createSensor({
        "id": $stateParams.id,
        "name": $scope.newSensorName,
        "signal": signalSelection,
        "pin": $scope.newSensorPin,
        "direction": directionList,
        "refresh": $scope.newSensorRefesh
      }, function (data) {
        if($scope.newSensorDirection == directionList[0]) {
          var request = setInterval(function() {
            SensorData.getData({
              "node": $stateParams.id,
              "sensor": data.sensor.id
            },function (datainfo) {
              data.sensor.in = datainfo.data.value + ' ' + datainfo.data.unit;
              //console.log(sensor.name + ' info: ' + datainfo.data.value + ' ' + datainfo.data.unit);
            });
          }, $scope.newSensorRefesh);
          requests[data.sensor.id] = request;
        }
        makeSensorUserfriendly(data.sensor);
        $scope.sensors.push(data.sensor);
        $scope.newSensorName = '';
        $scope.newSensorSignal = 'None';
        $scope.newSensorPin = '';
        $scope.newSensorDirection = 'None';
        $scope.newSensorRefesh = '';
      });
    } else
      $scope.newSensor = true;
  }

  $scope.removeSensor = function(index) {
    if(confirm("Are you sure you want to remove this sensor?")) {
      Node.deleteSensor({
        "sensor_id": $scope.sensors[index].id,
        "id": $stateParams.id
      }, function() {
        clearInterval(requests[$scope.sensors[index].id]);
        delete requests[$scope.sensors[index].id];
        $scope.sensors.splice(index, 1);
        if($scope.sensors.length == 0) {
          $scope.newSensor = true;
        }
      });
    }
  }
  Node.get({"id": $stateParams.id}, function (data) {
    if(data.node.sensors.length == 0) {
        $scope.newSensor = true;
    } else {
      angular.forEach(data.node.sensors, function(sensor) {
        makeSensorUserfriendly(sensor);
        sensor.edit = false;
        $scope.sensors = data.node.sensors;
        if(sensor.direction == $scope.directionList[0])
        var request = setInterval(function() {
          SensorData.getData({
            "node": $stateParams.id,
            "sensor": sensor.id
          },function (input) {
            sensor.in = input.data.value + ' ' + input.data.unit;
            //console.log(sensor.name + ' info: ' + data.data.value + ' ' + data.data.unit);
          });
        }, sensor.refresh);
        if(sensor.direction == $scope.directionList[0])
          requests[sensor.id] = request;
      });
    }
  });

  function makeSensorUserfriendly(sensor) {
    if(sensor.signal == 'A') {
      sensor.signal = $scope.signalList[0]; 
    } else {
      sensor.signal = $scope.signalList[1];
    }
    if(sensor.direction == 'R') {
      sensor.direction = $scope.directionList[0];
    } else {
      sensor.direction = $scope.directionList[1];
    }
  }

  $scope.$on('$destroy', function() {
    angular.forEach(requests, function(value, key) {
      clearInterval(value);
    });
  });

});
