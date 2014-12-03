'use strict';

angular.module('flagular')
  .factory('Node', function ($resource) {
    return $resource('/takonosu/api/nodes/:id/:sensors', {
      id: '@id',
      sensors: '@sensors'
    },
    {
      get: {
        method: 'GET'
      },
      query: {
        method: 'GET',
        params: { }
      },
      updateNode: {
        method: 'PUT'
      },
      updateSensor: {
        method: 'PUT'
      },
      getSensors: {
        method: 'GET',
        params: {
          sensors: 'sensors'
        }
      }
	  });
  });
