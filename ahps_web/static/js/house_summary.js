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
    Module-programs page controller
*/
app.controller('houseSummaryController', function($scope, $http, $sce) {
    // Initialization

    $scope.title = "AHPS Web";
    $scope.error = "";
    $scope.message = "";

    get_house_summary();

    function get_house_summary() {
        $("#ajax-pending").show();
        $http.get('/house/summary', {}).
            success(function(data, status, headers, config) {
                $scope.programs = data.programs;
                // Make the HTML in the program summary safe
                for (i = 0; i < $scope.programs.length; i++) {
                    var program = $scope.programs[i];
                    program.program_summary = $sce.trustAsHtml(program.program_summary);
                }
                $("#ajax-pending").hide();
            }).
            error(function(data, status, headers, config) {
                if (data && (data.message)) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to get house summary";
                }
                $("#ajax-pending").hide();
            });
    };

});