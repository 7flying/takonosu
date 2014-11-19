angular.module('flagular')
  .controller('HomeController', ['$scope', function ($scope, Node) {
  
  Node.get().$promise.then(
    	function success(data) {
    		console.log(data);		
    	});

  }]);
