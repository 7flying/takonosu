angular.module('flagular')
  .controller('SensorCtrl', function ($scope, $stateParams, Node) {
  
  $scope.editNode = function(sensor) {
      if(sensor.edit)
        sensor.edit = false;
      else
        sensor.edit = true;
    };

  $scope.updateNode = function(node) {
    Node.update({
      "id": node.id,
      "board_type": node.board_type,
      "name": node.name,
      "nic": node.nic
    }, function() {
      node.edit = false;
    });
  }

  Node.getSensors({id: $stateParams.id}).$promise.then(
    function success(data) {
      console.log(data);
      $scope.sensors = data.sensors;
    });
  });