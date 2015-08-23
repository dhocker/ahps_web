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
    Add a new room controller
*/
app.controller('addroomController', function($scope, $http) {
    // Initialization

    $scope.title = "AHPS Web";
    $scope.name = "";
    $scope.description = "";
    $scope.error = "";

    $scope.add_room = function() {
        if ($scope.name == "") {
            $scope.error = "Room name is required";
            return;
        }
        $http.post("/home/room", {"data" :
                    {'name': $scope.name,
                    'description': $scope.description
                    }
                }).
            success(function(data, status, headers, config) {
                // Cancel warnings for unsaved data
                window.onbeforeunload = null;
                // Room was created. Go back to the home page.
                window.location.replace("/home");
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Host communication error";
            });
    };

    $scope.cancel = function() {
        // Cancel warnings for unsaved data
        window.onbeforeunload = null;
        window.location.replace("/home");
    };
});
