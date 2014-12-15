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
    };

  $scope.updateSensor = function(sensor) {
    sensor.edit = false;
  }

  $scope.createSensor = function() {
    console.log("on sensor create, value: " + $scope.newSensor);
    if($scope.newSensor)
      $scope.newSensor = false;
    else
      $scope.newSensor = true;
  }

  $scope.removeSensor = function(index) {
    if(confirm("Are you sure you want to remove this sensor?")) {
      console.log('removed');
      $scope.sensors.splice(index, 1);
      //Call server to upload removal.
      if($scope.sensors.length == 0) {
        $scope.newSensor = true;
      }
    }
  }

  Node.getSensors({id: $stateParams.id}).$promise.then(
    function success(data) {
      angular.forEach(data.sensors, function(sensor) {
        sensor.edit = false;
        $scope.sensors = data.sensors;
        tempSensors = JSON.parse(JSON.stringify($scope.sensors));
        if(sensor.direction === 'R')
        setInterval(function() {
          SensorData.getData(function (data) {
            sensor.in = data.data.value + ' ' + data.data.unit;
            console.log(sensor.name + ' info: ' + data.data.value + ' ' + data.data.unit);
          });
        }, sensor.refresh);
      });
    });
  });