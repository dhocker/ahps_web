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
app.controller('modulesController', function($scope, $http, Tracker) {
    // Initialization

    $scope.title = "AHPS Web";
    $scope.error = "";
    $scope.message = "";
    $scope.roomid = $("#roomid").val();
    $scope.room_modules = [];

    $scope.track_change = Tracker.track_change;

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

    $scope.is_module_type_match = function(module_type, mt) {
        return mt.toLowerCase() == module_type.toLowerCase();
    };

    $scope.is_house_code_match = function(module_hc, hc) {
        return hc.toLowerCase() == module_hc.toLowerCase();
    };

    /* When the module type changes, immediately save the module
    so the type change is obvious */
    $scope.module_type_changed = function(module) {
        console.log("Module type was changed");
        $scope.save_module(module);
    }

    $scope.house_code_changed = function(moduleid) {
    };

    $scope.device_code_changed = function(moduleid) {
    };

    /* Save all module properties */
    $scope.save_module = function(module) {
        var moduleid = module.moduleid;
        var rp = {};
        rp["module_type"] = module["module_type"].toLowerCase();
        rp["name"] = module["name"];
        rp["house_code"] = module["house_code"];
        rp["device_code"] = module["device_code"];
        rp["dim_amount"] = module["dim_amount"];

        $http.put('/module/' + String(module.moduleid), {"data": rp}).
            success(function(data, status, headers, config) {
                // Success
                $scope.error = "";
                $scope.message = "Saved";
                window.onbeforeunload = null;
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
        window.location.replace('/module/' + String(moduleid) + '/programs/page');
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
        // Show  dialog for moving a module
        $("#move-module-dialog").data("moduleid", moduleid).dialog("open");
    };

    // Move a module to another room
    $scope.angular_move = function(moduleid) {
        var to_room = $("#new_room").val();
        $http.post('/rooms/' + String(to_room) + "/module/" + String(moduleid), {}).
            success(function(data, status, headers, config) {
                // Success
                $scope.error = "";
                // After move, refresh page
                $scope.get_modules();
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Error moving module"
                }
            });
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

$(document).ready(function() {
    /* Initialize the confirmation dialog */
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

    /* Initialize the module-move dialog box */
    $("#move-module-dialog").dialog(
    {
        autoOpen: false,
        modal: true,
        closeOnEscape: false,
        buttons: {
            "Move": function(event) {
                $("#move-module-dialog").dialog( "close" );
                var el = $("html");
                var scope = angular.element(el).scope();
                scope.angular_move($(this).data("moduleid"));
            },
            "Cancel": function(event) {
                $("#move-module-dialog").dialog( "close" );
            }
        }
    });

});
