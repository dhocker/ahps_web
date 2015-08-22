
/*
    AHPS_Web AngularJS app
*/

var app = angular.module('ahps_web', []);

// Change the interpolation marker from {{ }} to {= =} to avoid
// collision with the Jinga2 template system.
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{=');
    $interpolateProvider.endSymbol('=}');
});
