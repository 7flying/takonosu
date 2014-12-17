'use strict';
//blah
angular.module('flagular')
  .factory('Node', function ($resource) {
    return $resource('/takonosu/api/nodes/:sensors/:identifier', {
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
      deleteSensor: {
        method: 'DELETE',
        params: {
          sensors: 'sensors'
        }
      },
      createNode: {
        method: 'POST'
      },
      createSensor: {
        method: 'POST',
        params: {
          sensors: 'sensors'
        }
      }
	  });
  });
