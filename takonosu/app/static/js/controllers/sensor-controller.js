angular.module('flagular')
  .controller('SensorCtrl', function ($scope, $stateParams, Node, SensorData) {
  $scope.newSensor = false;
  $scope.sensors = [];
  tempSensors = [];
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
        "signal": $scope.newSensorSignal,
        "pin": $scope.newSensorPin,
        "direction": $scope.newSensorDirection,
        "refresh": $scope.newSensorRefesh
      }, function (data) {
        if($scope.newSensorDirection == 'R') {
          setInterval(function() {
            SensorData.getData({
              "node": $stateParams.id,
              "sensor": sensor.id
            },function (datainfo) {
              data.sensor.in = datainfo.data.value + ' ' + datainfo.data.unit;
              console.log(sensor.name + ' info: ' + datainfo.data.value + ' ' + datainfo.data.unit);
            });
          }, $scope.newSensorRefesh);
        }
        $scope.sensors.push(data.sensor);
        $scope.newSensorName = '';
        $scope.newSensorSignal = '';
        $scope.newSensorPin = '';
        $scope.newSensorDirection = '';
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
        $scope.sensors.splice(index, 1);
        if($scope.sensors.length == 0) {
          $scope.newSensor = true;
        }
      });
    }
  }

  Node.getSensors({id: $stateParams.id}).$promise.then(
    function success(data) {
      if(data.sensors.length == 0) {
        $scope.newSensor = true;
      } else {
        angular.forEach(data.sensors, function(sensor) {
          sensor.edit = false;
          $scope.sensors = data.sensors;
          if(sensor.direction === 'R')
          setInterval(function() {
            SensorData.getData({
              "node": $stateParams.id,
              "sensor": sensor.id
            },function (data) {
              sensor.in = data.data.value + ' ' + data.data.unit;
              console.log(sensor.name + ' info: ' + data.data.value + ' ' + data.data.unit);
            });
          }, sensor.refresh);
        });
      }
    });
  });