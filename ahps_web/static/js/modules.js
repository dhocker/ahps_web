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

    /* Get all modules for the current house */
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

    $scope.is_house_code_match = function(module, hc) {
        return module && (hc.toLowerCase() == module.house_code.toLowerCase());
    };

    $scope.is_device_code_match = function(module, dc) {
        return module && (String(dc) == String(module.device_code));
    };

    /* When the module type changes, immediately save the module
    so the type change is obvious */
    $scope.module_type_changed = function(moduleid) {
        console.log("Module type was changed");
        $scope.save_room(moduleid);
    }

    $scope.house_code_changed = function(moduleid) {
    };

    $scope.device_code_changed = function(moduleid) {
    };

    /* Save all room properties */
    $scope.save_room = function(moduleid) {
        rp = {};
        rp["module_type"] = $("#module-type-" + String(moduleid)).val().toLowerCase();
        rp["name"] = $("#module-name-text-" + String(moduleid)).val();
        rp["house_code"] = $("#house-code-" + String(moduleid)).val();
        rp["device_code"] = $("#device-code-" + String(moduleid)).val();
        rp["dim_amount"] = $("#dim-amount-" + String(moduleid)).val();

        $http.put('/module/' + String(moduleid), {"data": rp}).
            success(function(data, status, headers, config) {
                // Success
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Error saving module"
                }
            });
    };

    $scope.show_programs = function(moduleid) {
        window.location.replace("/module/programs/" + String(moduleid));
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

    $scope.show_remove_dialog = function(moduleid) {
        // Show confirmation dialog for removing a module #}
        $("#dialog").data("moduleid", moduleid).dialog("open");
    };

    $scope.angular_delete = function() {
        // Refresh page
        $scope.get_modules();
    };

    $scope.show_move_dialog = function(moduleid) {
    };

    $scope.add_appliance = function(roomid) {
        window.location.replace("/room/" + String(roomid) + "/new_appliance_module");
    };

    $scope.add_lamp = function(roomid) {
        window.location.replace("/room/" + String(roomid) + "/new_lamp_module");
    };

    /* More initialization */
    $scope.get_modules();

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
                // $("#module-form-" + $(this).data("moduleid")).submit();

                $.ajax({
                    url: '/module/' + $(this).data("moduleid"),
                    type: 'DELETE',
                    success: function() {
                        console.log("Successful module delete");
                        // Get the scope for the html element
                        // and call the delete event.
                        // This is a bit of a hack, but to get rid
                        // of it will require replacing all of the dialogs.
                        var el = $("html");
                        var scope = angular.element(el).scope();
                        scope.angular_delete();
                    }
                });
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
