'use strict';
//blah
angular.module('flagular')
  .factory('Node', function ($resource) {
    return $resource('/takonosu/api/nodes/:identifier/:sensors', {
      id: '@identifier',
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
      }, 
      deleteNode: {
        method: 'DELETE'
      },
      createNode: {
        method: 'POST'
      }
	  });
  });
