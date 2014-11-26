'use strict';

angular.module('flagular')
  .factory('Node', function ($resource) {
    return $resource('/takonosu/api/node', null,
    {
      get: {
        method: 'GET',
        params: 3
      },
      query: {
        method: 'GET',
        params: { }
      }
	  });
  });
