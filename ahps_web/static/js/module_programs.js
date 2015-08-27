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
app.controller('moduleProgramsController', function($scope, $http, $sce) {
    // Initialization

    $scope.title = "AHPS Web";
    $scope.error = "";
    // TODO Implement
    $scope.programs = [];

    function get_programs() {
        var moduleid = $("#moduleid").val();
        $http.get('/module/' + String(moduleid) + '/programs', {}).
            success(function(data, status, headers, config) {
                $scope.programs = data.programs;
                // Make the HTML in the program summary safe
                for (i = 0; i < $scope.programs.length; i++) {
                    var program = $scope.programs[i];
                    program["program_summary"] = $sce.trustAsHtml(program["program_summary"]);
                }
            }).
            error(function(data, status, headers, config) {
                if (data && (data.message)) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to get programs";
                }
            });
    };

    $scope.add_program = function() {
        var moduleid = $("#moduleid").val();
        $http.post('/module/' + String(moduleid) + '/program', {}).
            success(function(data, status, headers, config) {
                // Refresh the programs list
                get_programs();
            }).
            error(function(data, status, headers, config) {
                if (data && (data.message)) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to get programs";
                }
            });
    };

    $scope.edit_program = function(programid) {
        var moduleid = $("#moduleid").val();
        window.location.replace("/modules/program/" + String(programid) + "/page");
    };

    $scope.remove_program = function(programid, program_name) {
        /* Set the dialog text with the room name */
        $("#dialog-text").text("Remove program: " + program_name + "?");
        /* Pop the confirmation dialog */
        $("#dialog")
            .data("programid", programid)
            .dialog("open");
    };

    $scope.angular_remove_program = function(programid) {
        $http.delete('/module/program/' + String(programid), {}).
            success(function(data, status, headers, config) {
                // Refresh the programs list
                get_programs();
            }).
            error(function(data, status, headers, config) {
                if (data && (data.message)) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to refresh programs";
                }
            });
    };

    // Continuing with initializatin...
    get_programs();
});

/* Initialize the confirmation dialog */
$(document).ready(function() {
    $("#dialog").dialog(
    {
        autoOpen: false,
        modal: true,
        closeOnEscape: false,
        width: 400,
        buttons: {
            "Remove": function(event) {
                $("#dialog").dialog( "close" );
                /* Effectively a redirect to the remove page */
                var programid = $(this).data("programid");
                // Need access to scope
                var el = $("html");
                var scope = angular.element(el).scope();
                scope.angular_remove_program(programid);
            },
            "Cancel": function(event) {
                $("#dialog").dialog( "close" );
            }
        }
    });

});

/* Show confirmation dialog for removing a program */
function confirmRemove(moduleid, programid, name){
    /* Set the dialog text with the room name */
    $("#dialog-text").text("Remove program " + name + "?");
    /* Pop the confirmation dialog */
    $("#dialog")
        .data("moduleid", moduleid)
        .data("programid", programid)
        .data("name", name)
        .dialog("open");
};
