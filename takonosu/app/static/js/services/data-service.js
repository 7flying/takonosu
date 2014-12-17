'use strict';
//blah
angular.module('flagular')
  .factory('SensorData', function ($resource) {
    return $resource('/takonosu/api/data', null,
    {
      getData: {
        method: 'GET'
      },
      sendData: {
      	method: 'PUT'
      }
	});
  });
