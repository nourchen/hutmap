'use strict';

(function () {
  angular.module('google-maps').

  /**
   * Modified version of Nicolas Laplante's angular-google-maps directive
   * https://github.com/nlaplante/angular-google-maps
   */
  directive('googleMapMarkers', ['$timeout', '$parse', function($timeout, $parse) {

    function link(scope, element, attrs, controller) {
      // Check what's defined in attrs
      var hasOnMarkerSelected = false;

      if (attrs.hasOwnProperty('onMarkerSelected')) {
        hasOnMarkerSelected = true;
      }

      // Add marker (testing only)
      var marker = new google.maps.Marker({
        position: new google.maps.LatLng(46.87916, -120)
      });
      controller.addMarker(marker);
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(60, -122)
      });
      controller.addMarker(marker);

      // Set up onMarkerSelected callbacks
      if (hasOnMarkerSelected) {
        var onMarkerSelected = $parse(attrs.onMarkerSelected);

        angular.forEach(controller.markers, function(marker, i) {
          google.maps.event.addListener(marker, 'click', function() {
            $timeout(function() {
              var locals = {'$marker': marker};
              onMarkerSelected(scope.$parent, locals);
            });
          });
        });
      }
    }


    return {
      restrict: 'AE',
      priority: 100,
      scope: false,
      require: '^googleMap',
      link: link
    };
  }]);
})();

/**
   
    
    
   
        // Markers
        scope.$watch('markers', function (newValue, oldValue) {
          
          $timeout(function () {
            
            angular.forEach(newValue, function (v, i) {
              if (!_m.hasMarker(v.latitude, v.longitude)) {
                _m.addMarker(v.latitude, v.longitude);
              }
            });
            
            // Clear orphaned markers
            var orphaned = [];
            
            angular.forEach(_m.getMarkerInstances(), function (v, i) {
              // Check our scope if a marker with equal latitude and longitude. 
              // If not found, then that marker has been removed form the scope.
              
              var pos = v.getPosition(),
                lat = pos.lat(),
                lng = pos.lng(),
                found = false;
              
              // Test against each marker in the scope
              for (var si = 0; si < scope.markers.length; si++) {
                
                var sm = scope.markers[si];
                
                if (floatEqual(sm.latitude, lat) && floatEqual(sm.longitude, lng)) {
                  // Map marker is present in scope too, don't remove
                  found = true;
                }
              }
              
              // Marker in map has not been found in scope. Remove.
              if (!found) {
                orphaned.push(v);
              }
            });

            orphaned.length && _m.removeMarkers(orphaned);           
            
            // Fit map when there are more than one marker. 
            // This will change the map center coordinates
            if (attrs.fit == 'true' && newValue.length > 1) {
              _m.fit();
            }
          });
          
        }, true);
        

*/
