// Declare app level module which depends on filters, and services
angular.module('flagular', ['ngResource', 'ui.bootstrap', 'ui.date', 'ui.router'])
    .config(function ($stateProvider, $urlRouterProvider, $locationProvider) {
    $urlRouterProvider
      .otherwise('/');

      $locationProvider.html5Mode(true);
  });