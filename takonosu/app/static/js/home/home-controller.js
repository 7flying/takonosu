angular.module('flagular')
  .controller('HomeController', function ($scope, Node) {
  
  Node.get({}).$promise.then(
    	function success(data) {
    		$scope.node = data;		
    	});

  });
