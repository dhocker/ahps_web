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
    Edit house page controller
*/
app.controller('editHouseController', function($scope, $http) {
    // Initialization

    $scope.title = "AHPS Web";
    $scope.error = "";
    $scope.message = "";

    var houseid = $("#houseid").val();
    get_house(houseid);

    function get_house(houseid) {
        $http.get('/house/' + String(houseid), {}).
            success(function(data, status, headers, config) {
                $scope.house = data.house;
                $scope.message = "";
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to get house";
                }
            });
    };

    $scope.save_house = function(houseid) {
        $http.post('/house/' + String(houseid), {"data": $scope.house}).
            success(function(data, status, headers, config) {
                $scope.message = "Saved";
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to save house";
                }
            });
    };
});