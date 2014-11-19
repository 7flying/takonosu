'use strict';

angular.module('flagular')
  .factory('Node', function ($resource) {
    return $resource('/takonosu/api/node', {
      id: '@id'
    },
    {
      update: {
        method: 'GET',
        params: {
          id: 3
        }
      }
	  });
  });
