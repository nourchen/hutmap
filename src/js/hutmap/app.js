'use strict';

(function() {
  angular.module('hutmap', ['hutmap.services', 'hutmap.directives',
    'hutmap.filters', 'hutmap.controllers', 'AngularGM', 'ngResource',
    'ui.bootstrap']).

  config(
    ['$routeProvider', '$locationProvider', 'PlacesProvider', 
    function($routeProvider, $locationProvider, PlacesProvider) {

    $routeProvider.
      when('/', {
        templateUrl: '/partials/home.html',
        activetab: 'home',
      }).
      when('/map/', {
        templateUrl: '/partials/map.html',
        activetab: 'map',
        reloadOnSearch: false,
      }).
      when('/about/', {
        templateUrl: '/partials/about.html',
        activetab: 'about',
      });

    $locationProvider.html5Mode(true);

    // suggest bounds for our search results
    PlacesProvider.bounds(new google.maps.LatLngBounds(
        new google.maps.LatLng(30, -130),
        new google.maps.LatLng(65, -80)));
  }]).

  constant('hutmapMapId', 'map_canvas').

  value('mapOptions', {
    zoom : 8,
    center : new google.maps.LatLng(46.87916, -120),
    mapTypeId : google.maps.MapTypeId.TERRAIN,
    streetViewControl: false,
    panControlOptions: {
      position: google.maps.ControlPosition.LEFT_CENTER
    },
    zoomControlOptions: {
      position: google.maps.ControlPosition.LEFT_CENTER
    },

  }).

  value('markerOptions', {
    huts: {
      icon: '/static/img/marker_gray_small.png',
      shape: {
        coord: [6, 0, 2, 2, 0, 6, 6, 13, 12, 6, 10, 2, 6, 0],
        type: 'poly'
      },
      zIndex: 0
    },
    filteredHuts: {
      icon: '/static/img/marker_red_small.png',
      shape: {
        coord: [6, 0, 2, 2, 0, 6, 6, 13, 12, 6, 10, 2, 6, 0],
        type: 'poly'
      },
      zIndex: 1
    },
    selected: {
      icon: '/static/img/marker_yellow_small.png',
      zIndex: 2
    }
  });

})();
