angular.module('flagular')
  .config(function ($stateProvider) {
    $stateProvider
      .state('home', {
        url: '/',
        templateUrl: 'views/node/home.html', 
        controller: 'HomeCtrl'
      })
      .state('sensor', {
      	url: '/?id',
      	templateUrl: 'views/sensor/home.html',
      	controller: 'SensorCtrl'
      });
  });