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
app.controller('allModulesController', function($scope, $http) {
    // Initialization

    $scope.title = "AHPS Web";
    $scope.error = "";
    $scope.message = "";

    var houseid = $("#houseid").val();
    get_house_modules(houseid);

    function get_house_modules(houseid) {
        $http.get('/modules', {}).
            success(function(data, status, headers, config) {
                $scope.modules = data.modules;
                // Default sorting
                $scope.sort_by_hdc();
                $scope.message = "";
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to get modules for current house";
                }
            });
    };

    $scope.module_on = function(moduleid) {
        $http.put('/modules/' + String(moduleid) + '/state' , {"data": {"state": "on"}}).
            success(function(data, status, headers, config) {
                // Success
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Error turning on module"
                }
            });
    };

    $scope.module_off = function(moduleid) {
        $http.put('/modules/' + String(moduleid) + '/state' , {"data": {"state": "off"}}).
            success(function(data, status, headers, config) {
                // Success
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Error turning off module"
                }
            });
    };

    $scope.save_modules = function() {
        $http.put('/modules/selected', {"data": $scope.modules}).
            success(function(data, status, headers, config) {
                $scope.message = "Saved";
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to save modules for current house";
                }
            });
    };

    $scope.lights_on = function() {
        $http.put('/modules/on', {}).
            success(function(data, status, headers, config) {
                $scope.message = "All lights turned on";
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to turn on modules for current house";
                }
            });
    };

    $scope.lights_off = function() {
        $http.put('/modules/off', {}).
            success(function(data, status, headers, config) {
                $scope.message = "All lights turned off";
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to turn off modules for current house";
                }
            });
    };

    $scope.sort_by_hdc = function() {
        $scope.modules.sort(function(a, b){
            a_hdc = a.house_code + sortable_device_code(a.device_code);
            b_hdc = b.house_code + sortable_device_code(b.device_code);
            if (a_hdc > b_hdc) {
                return 1;
            }
            if (a_hdc < b_hdc) {
                return -1;
            }
            return 0;
        });
    };

    function sortable_device_code(dc) {
        return ("0" + dc).slice(-2);
    };

    $scope.sort_by_room = function() {
        $scope.modules.sort(function(a, b){
            a_lc = a.room_name.toLowerCase();
            b_lc = b.room_name.toLowerCase();
            if (a_lc > b_lc) {
                return 1;
            }
            if (a_lc < b_lc) {
                return -1;
            }
            return 0;
        });
    };
});