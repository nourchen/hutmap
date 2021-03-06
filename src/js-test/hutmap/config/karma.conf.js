basePath = '../../../';

files = [
  JASMINE,
  JASMINE_ADAPTER,
  'https://maps.googleapis.com/maps/api/js?sensor=false&libraries=places',
  'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
  'http://ajax.googleapis.com/ajax/libs/angularjs/1.0.5/angular.min.js',
  'http://ajax.googleapis.com/ajax/libs/angularjs/1.0.5/angular-resource.min.js',
  'js-test/lib/angular/angular-mocks.js',
  'js/third-party/**/*.js',
  'js/hutmap/app.js',
  'js/hutmap/**/module.js',
  'js/hutmap/directives.js',
  'js/hutmap/filters.js',
  'js/hutmap/**/*.js',
  'js-test/hutmap/unit/fixtures.js',
  'js-test/hutmap/unit/**/*.js'
];

autoWatch = true;

browsers = ['PhantomJS'];

preprocessors = {
  '**/src/**/*.js': 'coverage'
};

reporters = ['progress', 'coverage'];

coverageReporter = {
  type : 'html',
  dir : 'js-test/hutmap/coverage/'
};

