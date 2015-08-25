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
    Home page app controller
*/
app.controller('addApplianceController', function($scope, $http) {
    // Initialization

    $scope.title = "AHPS Web";
    $scope.error = "";
    // Scaffold for house and device code includes
    $scope.module = {};
    // Module id is arbitrary and used only to satisfy includes for house and device codes
    $scope.module["moduleid"] = "0";
    $scope.module["house_code"] = "A";
    $scope.module["device_code"] = "1";

    $scope.save_module = function(roomid) {
        rp = {};
        rp["module_type"] = "appliance";
        rp["name"] = $("#name").val();
        rp["house_code"] = $("#house-code-0").val();
        rp["device_code"] = $("#device-code-0").val();

        $http.post('/room/' + String(roomid), {"data": rp}).
            success(function(data, status, headers, config) {
                // Successfully added
                // will this work???
                // Return to the modules-on-room page
                window.onbeforeunload = null;
                window.location.replace("/modules_page/" + String(roomid));
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Attempt to add appliance module failed"
                }
            });
    };

    $scope.cancel = function(roomid) {
        window.location.replace("/modules_page/" + String(roomid));
    };

    $scope.is_house_code_match = function(module, hc) {
        return module && (hc.toLowerCase() == module.house_code.toLowerCase());
    };

    $scope.house_code_changed = function(moduleid) {
    };

    $scope.device_code_changed = function(moduleid) {
    };
});