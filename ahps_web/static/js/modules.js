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
app.controller('modulesController', function($scope, $http) {
    // Initialization

    $scope.title = "AHPS Web";
    $scope.error = "";
    $scope.roomid = $("#roomid").val();
    $scope.room_modules = [];

    $scope.get_modules = function() {
        $http.get('/modules/' + String($scope.roomid), {}).
            success(function(data, status, headers, config) {
                $scope.room_modules = data.modules;
            }).
            error(function(data, status, headers, config) {
                $scope.status = "";
                $scope.error = data.message;
            });
    };

    $scope.isModuleTypeMatch = function(module, mt) {
        return module && (mt.toLowerCase() == module.module_type.toLowerCase());
    };

    /* When the module type changes, immediately save the module
    so the type change is obvious */
    $scope.module_type_changed = function(moduleid) {
        // TODO Rework
        console.log("Module type was changed");
        // submitForm("save", moduleid);
    }

    $scope.get_modules();

});

/* Initialize the confirmation dialog */
$(document).ready(function() {
    $("#dialog").dialog(
    {
        autoOpen: false,
        modal: true,
        closeOnEscape: false,
        buttons: {
            "Remove": function(event) {
                $("#dialog").dialog( "close" );
                $("#module-form-" + $(this).data("moduleid")).submit();
                },
            "Cancel": function(event) {
                $("#dialog").dialog( "close" );
                }
        }
    });

    $("#move-module-dialog").dialog(
    {
        autoOpen: false,
        modal: true,
        closeOnEscape: false,
        buttons: {
            "Move": function(event) {
                $("#move-module-dialog").dialog( "close" );
                $("#module-to-move").val($(this).data("moduleid"));
                $("#move-module-form").submit();
                },
            "Cancel": function(event) {
                $("#move-module-dialog").dialog( "close" );
                }
        }
    });

});

// Show confirmation dialog for removing a module #}
function showRemoveDialog(moduleid){
    /* Set the value of the hidden button tag to reflect this is a remove */
    $("#submit-button-" + moduleid).val("remove");
    /* Set the dialog text with the room name */
    $("#dialog-text").text("Remove " + $("#module-name-text" + moduleid).val() + "?");
    /* Spring the dialog for the given room */
    $("#dialog")
        .data("moduleid", moduleid)
        .dialog("open");
};

// Show dialog for moving a module to another room #}
function showMoveDialog(moduleid){
    $("#move-module-dialog")
        .data("moduleid", moduleid)
        .dialog("open");
};

/* Submit the form */
function submitForm(form_action, moduleid){
    window.onbeforeunload=null;
    $("#submit-button-" + moduleid).val(form_action);
    $("#module-form-" + moduleid).submit();
};

/* When the module type changes, immediately save the module
so the type change is obvious */
function moduleTypeChanged(moduleid){
    submitForm("save", moduleid);
}
