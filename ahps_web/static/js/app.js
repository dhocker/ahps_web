
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

/*
    App-wide services
*/

/*
    Track page changes
*/
app.factory('Tracker', function() {
    var service = {};
    service.track_change = function() {
        window.onbeforeunload = service.unsaved_changes_warning;
    };

    service.reset_change = function() {
        window.onbeforeunload = null;
    };

    service.unsaved_changes_warning = function(e) {
        e.returnValue = "You have unsaved changes on this page.";
        /*
        Some browsers (e.g. Chrome, Safari will display the returned text.
        Firefox does not display the returned text.
        */
        return e.returnValue;
    };

    return service;
});