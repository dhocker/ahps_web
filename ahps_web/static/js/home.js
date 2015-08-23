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
app.controller('homeController', function($scope, $http) {
    // Initialization

    $scope.title = "AHPS Web";
    $scope.error = "";
    get_rooms();

    // Save room data (name and description)
    $scope.save_room = function(room_id) {
        var name_id = "#room-name-text-" + String(room_id);
        var room_name = $(name_id).val();
        var desc_id = "#room-desc-" + String(room_id);
        var room_desc = $(desc_id).val();

        $http.put("/home/room/" + String(room_id), {"data" :
                    {'room-name': room_name,
                    'room-desc': room_desc
                    }
                }).
            success(function(data, status, headers, config) {
                // Room was saved
                window.onbeforeunload=null;
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Host communication error";
            });
    };

    $scope.show_modules = function(room_id) {
        window.location.replace("/modules/" + String(room_id));
    };

    /* Show confirmation dialog for removing a room */
    $scope.show_dialog = function(roomid){
        /* Set the value of the hidden button tag to reflect this is a remove */
        $("#submit-button-" + roomid).val("remove");
        /* Set the dialog text with the room name */
        $("#dialog-text").text("Remove room: " + $("#room-name-text-" + roomid).val() + "?");
        /* Spring the dialog for the given room */
        $("#dialog")
            .data("roomid", roomid)
            .dialog("open");
    };

    $scope.add_room = function() {
        window.location.replace("/home/room");
    };

    $scope.download_programs = function() {
        $("#download-progress-dialog").dialog("open");
        $http.put('/home/download_programs', {}).
            success(function(data, status, headers, config) {
                $("#download-progress-dialog").dialog("close");
                $("#download-results").html(result);
                $("#download-results-dialog").dialog("open");
            }).
            error(function(data, status, headers, config) {
                $("#download-progress-dialog").dialog("close");
                $("#download-results").html("Download failed");
                $("#download-results-dialog").dialog("open");
            });
    };

    $scope.angular_delete = function() {
        console.log("Angualar_Delete was called");
        // TODO Reload the rooms list
        get_rooms();
    };

    function get_rooms() {
        $http.get('/home/rooms', {}).
            success(function(data, status, headers, config) {
                $scope.rooms = data.rooms;
            }).
            error(function(data, status, headers, config) {
                $scope.status = "";
                $scope.error = data.message;
            });
    };

});

/*
Script originally embedded in the home.html file
*/

$(document).ready(function() {

    /* Initialize the confirmation dialog */
    $("#dialog").dialog(
    {
        autoOpen: false,
        modal: true,
        closeOnEscape: false,
        buttons: {
            "Remove": function(event) {
                $("#dialog").dialog( "close" );
                // $("#room-form-" + $(this).data("roomid")).submit();

                $.ajax({
                    url: '/home/room/' + $(this).data("roomid"),
                    type: 'DELETE',
                    success: function() {
                        console.log("Successful delete");
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

    // Initialize the download dialog boxes
    $("#download-progress-dialog").dialog(
    {
        autoOpen: false,
        modal: true,
        closeOnEscape: false
    });
    $("#download-results-dialog").dialog(
    {
        autoOpen: false,
        modal: true,
        closeOnEscape: true,
        buttons: {
            "Close": function(event) {
                $("#download-results-dialog").dialog( "close" );
                },
        }
    });

    // Reset change tracking to avoid false positives #}
    window.onbeforeunload=null;

});

/* Show confirmation dialog for removing a room */
function showDialog(roomid){
    /* Set the value of the hidden button tag to reflect this is a remove */
    $("#submit-button-" + roomid).val("remove");
    /* Set the dialog text with the room name */
    $("#dialog-text").text("Remove room: " + $("#room-name-text-" + roomid).val() + "?");
    /* Spring the dialog for the given room */
    $("#dialog")
        .data("roomid", roomid)
        .dialog("open");
};
