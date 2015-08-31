/*
#
# AHPS Web - web server for managing an AtHomePowerlineServer instance
# Copyright (C) 2014, 2015  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#
*/

/*
    Houses page controller
*/
app.controller('housesController', function($scope, $http) {
    // Initialization

    $scope.title = "AHPS Web";
    $scope.error = "";
    $scope.message = "";

    get_houses();

    function get_houses() {
        $http.get('/houses', {}).
            success(function(data, status, headers, config) {
                $scope.houses = data.houses;
                $scope.message = "";
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to get houses";
                }
            });
    };

    $scope.add_house = function() {
        $http.post('/houses', {}).
            success(function(data, status, headers, config) {
                $scope.message = "";
                $scope.error = "";
                // Refresh house list to show newly added house
                get_houses();
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to get houses";
                }
            });
    };

    $scope.select_house = function(houseid) {
        $http.put('/houses/selected/' + String(houseid), {}).
            success(function(data, status, headers, config) {
                $scope.message = "";
                $scope.error = "";
                // Refresh house list to show newly selected house
                get_houses();
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to select house";
                }
            });
    };

    $scope.copy_house = function(houseid) {
        $http.post('/houses/duplicate/' + String(houseid), {}).
            success(function(data, status, headers, config) {
                $scope.message = "";
                $scope.error = "";
                // Refresh house list to show newly created house
                get_houses();
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to copy house";
                }
            });
    };

    $scope.edit_house = function(houseid) {
        window.location.replace("/house/" + String(houseid) + "/page");
    };

    $scope.remove_house = function(houseid, house_name) {
        /* Set the dialog text with the house name */
        $("#dialog-text").text("Remove house: " + house_name + "?");
        /* Pop the confirmation dialog */
        $("#dialog")
            .data("houseid", houseid)
            .data("name", name)
            .dialog("open");
    };

    $scope.angular_remove_house = function(houseid) {
        $http.delete('/house/' + String(houseid), {}).
            success(function(data, status, headers, config) {
                $scope.message = "";
                $scope.error = "";
                // Refresh house list to pick up removal
                get_houses();
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to remove house";
                }
            });
    };

});

/* Initialize the confirmation dialog */
$(document).ready(function() {
    $("#dialog").dialog(
    {
        autoOpen: false,
        modal: true,
        closeOnEscape: false,
        width: 500,
        buttons: {
            "Remove": function(event) {
                $("#dialog").dialog( "close" );
                /* Effectively a redirect to the remove page */
                houseid = $(this).data("houseid");
                // Get the scope for the html element
                // and call the delete event.
                // This is a bit of a hack, but to get rid
                // of it will require replacing all of the dialogs.
                var el = $("html");
                var scope = angular.element(el).scope();
                scope.angular_remove_house(houseid);
                },
            "Cancel": function(event) {
                $("#dialog").dialog( "close" );
                }
        }
    });

});

/* Show confirmation dialog for removing a program */
function confirmRemove(houseid, name){
    /* Set the dialog text with the house name */
    $("#dialog-text").text("Remove house " + name + "?");
    /* Pop the confirmation dialog */
    $("#dialog")
        .data("houseid", houseid)
        .data("name", name)
        .dialog("open");
};
