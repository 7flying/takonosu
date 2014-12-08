angular.module('flagular')
  .controller('HomeCtrl', function ($scope, Node) {
  
	$scope.editNode = function(node) {
  		if(node.edit)
  			node.edit = false;
  		else
  			node.edit = true;
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

  	Node.query().$promise.then(
    	function success(data) {
    		angular.forEach(data.nodes, function(node) {
          node.edit = false;
          $scope.nodes = data.nodes;
        });
    	});
  	});