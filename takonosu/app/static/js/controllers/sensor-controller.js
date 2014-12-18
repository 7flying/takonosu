angular.module('flagular')
  .controller('SensorCtrl', function ($scope, $stateParams, Node, SensorData) {
  
  var signalSelection, directionSelection;
  var board;
  var tempSensors = [];
  var requests = {};

  $scope.newSensor = false;
  $scope.sensors = [];
  $scope.newSensorSignal = 'None';
  $scope.newSensorDirection = 'None';
  $scope.signalList = ['Analog', 'Digital'];
  $scope.directionList = ['Read', 'Write'];
  $scope.pinList = [];


  $scope.signalSelect = function(name) {
    $scope.newSensorSignal = name;
    if(name == $scope.signalList[0]) {
      signalSelection = 'A';
      if(board == 'Arduino Uno')
        loadPinListForArduinoSignal();
    } else {
      signalSelection = 'D';
      if(board == 'Arduino Uno')
        loadPinListForArduinoSignal();
    }
  }

  $scope.directionSelect = function(directionName) {
    $scope.newSensorDirection = directionName;
    if(directionName == $scope.directionList[0]) {
      directionSelection = 'R';
      loadPinListForArduinoDirection();
    } else {
      directionSelection = 'W';
      loadPinListForArduinoDirection();
    }
  }

  $scope.pinSelect = function(pin) {
    $scope.newSensorPin = pin;
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
        "direction": directionSelection,
        "refresh": $scope.newSensorRefesh
      }, function (data) {
        makeSensorUserfriendly(data.sensor);
        if($scope.newSensorDirection == $scope.directionList[0]) {
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
  Node.get({"id": $stateParams.id}).$promise.then(
    function success(data) {
    board = data.node.board_type;
    if(board != 'Arduino Uno') { 
      $scope.showPinList = false;
    } else { 
      $scope.showPinList = true;
    }
    loadPinListForArduinoSignal('');
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

  function loadPinList(limit) {
    $scope.pinList = [];
    for(var i = 0; i < limit; i++) {
      $scope.pinList.push(i+1);
    }
  }

  function loadPinListArray(list) {
    $scope.pinList = [];
    for(var i in list){
      $scope.pinList.push(list[i]);
    }
  }

  function loadPinListForArduinoSignal() {
    if($scope.newSensorSignal == $scope.signalList[0]) {
      if($scope.newSensorDirection == 'None') {
          loadPinListArray(['1', '2', '3', '4', '5', '6', '9', '10', '11']);
      } else if($scope.newSensorDirection == $scope.directionList[0]) {
        loadPinListArray(['1', '2', '3', '4', '5']);
      } else {
        loadPinListArray(['3', '5', '6', '9', '10', '11']);
      }
      if(typeof $scope.newSensorPin === 'undefined' || $scope.newSensorPin == '') {
        $scope.newSensorPin = 'None';
      } else if(!isPinInList($scope.newSensorSignal, $scope.pinList)) {
        $scope.newSensorPin = $scope.pinList[0];
      }
    } else {
      loadPinList(13);
      if((typeof $scope.newSensorPin === 'undefined' || $scope.newSensorPin == '')) {
        $scope.newSensorPin = 'None';
      }
    }
  }

  function loadPinListForArduinoDirection() {
    if($scope.newSensorDirection == $scope.directionList[0]) {
      if($scope.newSensorSignal == $scope.signalList[0]) {
        loadPinListArray(['1', '2', '3', '4', '5']);
      } else {
        loadPinList(13);
      }
      if((typeof $scope.newSensorPin === 'undefined' || $scope.newSensorPin == '')) {
        $scope.newSensorPin = 'None';
      }
    } else {
      if($scope.newSensorSignal == $scope.signalList[0]) {
        loadPinListArray(['3', '5', '6', '9', '10', '11']);
      } else {
        loadPinList(13);
      }
      if((typeof $scope.newSensorPin === 'undefined' || $scope.newSensorPin == '')) {
        $scope.newSensorPin = 'None';
      }
    }
  }

  function isPinInList(pin, list) {
    for (var i = 0; i < list.length; i++) {
        if (list[i] == pin) {
            return true;
        }
    }
    return false;
  }

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
