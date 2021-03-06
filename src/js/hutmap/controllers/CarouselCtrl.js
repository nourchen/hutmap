'use strict';

(function () {
  angular.module('hutmap.controllers').

  controller('CarouselCtrl', ['$scope', '$route', '$http', '$q', function($scope, $route, $http, $q) {
    $scope.slides = [
      {
        title: 'Plummer Hut', 
        location: 'Waddington Range, British Columbia, Canada',
        hutLink: '/map/?m_selected=51.37361,-125.16458&m_center=51.388403,-125.062053&m_zoom=9',
        agency: {
          name: 'BC Mountaineering Club',
          url:  ''
        },
        thumbnail: '/static/img/no-image-available.gif',
        image: '/static/img/carousel/Plummer Hut.JPG'
      },
      {
        title: 'Joe River Chickee', 
        location: 'lorem ipsum dolor',
        hutLink: '',
        agency: {
          name: 'lorem ipsum dolor',
          url:  ''
        },
        thumbnail: '/static/img/no-image-available.gif',
        image: '/static/img/carousel/Joe River Chickee.JPG'
      },
      {
        title: 'John Muir Shelter', 
        location: 'lorem ipsum dolor',
        hutLink: '',
        agency: {
          name: 'lorem ipsum dolor',
          url:  ''
        },
        thumbnail: '/static/img/no-image-available.gif',
        image: '/static/img/carousel/John Muir Shelter.JPG'
      }
    ];
    $scope.imgStyle = function(imgUrl) {
      return {
        'background-image': 'url(\'' + imgUrl + '\')'
      }
    };

    // pre-load images
    $scope.carouselInterval = -1;
    var imgsLoaded = [];
    angular.forEach($scope.slides, function(slide, index) {
      imgsLoaded.push($http.get(slide.image));
    });
    $q.all(imgsLoaded).then(function() { $scope.carouselInterval = 8000; });
  }]);

})();
