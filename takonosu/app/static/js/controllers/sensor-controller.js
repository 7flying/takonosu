angular.module('flagular')
  .controller('SensorCtrl', function ($scope, $stateParams, Node) {
  
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

  Node.getSensors({id: $stateParams.id}).$promise.then(
    function success(data) {
      angular.forEach(data.sensors, function(sensor) {
        sensor.edit = false;
        $scope.sensors = data.sensors;
      });
    });
  });