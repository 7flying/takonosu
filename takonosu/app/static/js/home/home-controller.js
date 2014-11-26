angular.module('flagular')
  .controller('HomeController', function ($scope, Node) {
  
  Node.query().$promise.then(
    	function success(data) {
    		$scope.nodes = data.nodes;		
    	});
  });
