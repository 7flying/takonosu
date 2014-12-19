angular.module('flagular')
  .controller('HomeCtrl', function ($scope, Node) {
  
  $scope.nodes = [];
  $scope.newNode = false;
  $scope.newNodeBoard_type = 'None';
  $scope.newNodeNic = 'None';
  $scope.showError = false;

  $scope.boardSelect = function(name) {
    $scope.newNodeBoard_type = name;
    if(name == 'Arduino Uno') {
      $scope.newNodeNic = 'Bluetooth'
    } else if(name == 'Other') {
      $scope.newNodeNic = 'Wifi'
    } else {
      $scope.newNodeNic = 'XBee'
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
        if(typeof $scope.newNodeName !== 'undefined' && $scope.newNodeName.length
          && typeof $scope.newNodeAddress !== 'undefined' && $scope.newNodeAddress.length
          && $scope.newNodeBoard_type != 'None')
        {
          Node.createNode({
            "name": $scope.newNodeName,
            "board_type": $scope.newNodeBoard_type,
            "nic": $scope.newNodeNic,
            "address": $scope.newNodeAddress
          }, function (data) {
            $scope.nodes.push(data.node);
            $scope.newNodeName = '';
            $scope.newNodeBoard_type = 'None';
            $scope.newNodeNic = '';
            $scope.newNodeAddress = '';
            $scope.newNode = false;
            $scope.showError = false;
          });
        } else {
          $scope.showError = true;
        }
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