'use strict';

(function () {
  angular.module('hutmap.directives', [])

  .directive('blur', ['$parse', function ($parse) {
    return function (scope, elem, attrs) {
      var blurFn = $parse(attrs.blur);
      elem.bind('blur', function () {
        blurFn(scope);
      });
    };
  }]);

})();
