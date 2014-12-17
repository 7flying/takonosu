angular.module('flagular')
  .controller('HomeCtrl', function ($scope, Node) {
  
  $scope.nodes = [];
  $scope.newNode = false;
  $scope.newNodeBoard_type = 'None';
  $scope.newNodeNic = 'None';

  $scope.boardSelect = function(name) {
    $scope.newNodeBoard_type = name;
    if(name == 'Arduino Uno') {
      $scope.newNodeNic = 'Bluetooth'
    } else {
      $scope.newNodeNic = 'ZigBee'
    }
  }

	$scope.editNode = function(node) {
  		if(node.edit)
  			node.edit = false;
  		else
  			node.edit = true;
  	};

  	$scope.updateNode = function(node) {
      Node.updateNode({
        "id": node.id,
        "board_type": node.board_type,
        "nic": node.nic,
        "name": node.name
        }, function() {
  			node.edit = false;
  		});
  	}
    
     $scope.createNewNode = function() {
      if($scope.newNode) {
        $scope.newNode = false;
      } else {
        $scope.newNode = true;
      }
     }

    $scope.createNode = function() {
      if($scope.newNode) {
        $scope.newNode = false;
        Node.createNode({
          "name": $scope.newNodeName,
          "board_type": $scope.newNodeBoard_type,
          "nic": $scope.newNodeNic
        }, function (data) {
          $scope.nodes.push(data.node);
          $scope.newNodeName = '';
          $scope.newNodeBoard_type = '';
          $scope.newNodeNic = '';
        });
      } else
        $scope.newNode = true;
    }

     $scope.removeNode = function(index) {
    if(confirm("Are you sure you want to remove this node?")) {
      Node.deleteNode({"id": $scope.nodes[index].id}, function() {
        $scope.nodes.splice(index, 1);
        if($scope.nodes.length == 0) {
          $scope.newNode = true;
        }
      });
    }
  }

	Node.query().$promise.then(
  	function success(data) {
  		if(data.nodes.length == 0) {
        $scope.newNode = true;
      } else {
        angular.forEach(data.nodes, function(node) {
          node.edit = false;
          $scope.nodes = data.nodes;
        });
      }
    });
  
});