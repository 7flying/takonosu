'use strict';
//blah
angular.module('flagular')
  .factory('SensorData', function ($resource) {
    return $resource('/takonosu/api/data', {
      data: '@datum'
    },
    {
      getData: {
        method: 'GET'
      },
      sendData: {
      	method: 'PUT'
      }
	});
  });
