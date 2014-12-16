angular.module('flagular')
  .controller('HomeCtrl', function ($scope, Node) {
  
  $scope.nodes = [];
  $scope.newNode = false;
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

    $scope.createNode = function() {
      if($scope.newNode) {
        $scope.newNode = false;
        Node.createNode({
          "name": $scope.newNodeName,
          "board_type": $scope.newNodeBoard_type,
          "nic": $scope.newNodeNic
        }, function (data) {
          console.log(data);
        });
      } else
        $scope.newNode = true;
    }

     $scope.removeNode = function(index) {
    if(confirm("Are you sure you want to remove this node?")) {
      console.log(index);
      console.log($scope.nodes[index].id);
      Node.deleteNode({"id": $scope.nodes[index].id}, function() {
        $scope.nodes.splice(index, 1);
      });
      if($scope.nodes.length == 0) {
        $scope.newNode = true;
      }
    }
  }

  	Node.query().$promise.then(
    	function success(data) {
    		angular.forEach(data.nodes, function(node) {
          node.edit = false;
          $scope.nodes = data.nodes;
        });
    	});
  	});