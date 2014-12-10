angular.module('flagular')
  .controller('SensorCtrl', function ($scope, $stateParams, Node, SensorData) {
  $scope.newSensor = false;
  //bla
  $scope.editSensor = function(sensor) {
      if(sensor.edit)
        sensor.edit = false;
      else
        sensor.edit = true;
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

  Node.getSensors({id: $stateParams.id}).$promise.then(
    function success(data) {
      angular.forEach(data.sensors, function(sensor) {
        sensor.edit = false;
        if(sensor.direction === 'R')
        setInterval(function() {
          SensorData.getData(function (data) {
            sensor.in = data.data.value + ' ' + data.data.unit;
            console.log(sensor.name + ' info: ' + data.data.value + ' ' + data.data.unit);
          });
        }, sensor.refresh);
        $scope.sensors = data.sensors;
      });
    });
  });