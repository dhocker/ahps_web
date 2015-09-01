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
    Program page controller
*/
app.controller('programController', function($scope, $http, $sce, Tracker) {
    // Initialization

    $scope.title = "AHPS Web";
    $scope.error = "";
    $scope.message = "";

    $scope.track_change = Tracker.track_change;

    /* More initialization*/
    get_program_data(update_program);

    function get_program_data(success_callback) {
        var programid = $("#programid").val();
        $http.get('/module/program/' + String(programid), {}).
            success(function(data, status, headers, config) {
                $scope.program = data.programdata.program;
                $scope.module = data.programdata.module;
                // Post process program data
                success_callback();
            }).
            error(function(data, status, headers, config) {
                if (data && (data.message)) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to get program data";
                }
            });
    };

    // Update page with program data
    function update_program() {
        /*
        Set checkboxes for days of week based on contents of program.days string.
        The string looks like this: "MTWTFSS" (Monday through Sunday). Absent days
        are represented by a period. This is weekdays: "MTWTF.."
        */
        $scope.program.day = [0,0,0,0,0,0,0];
        for (i = 0; i < 7; i++)
        {
            d = $scope.program.days.substr(i, 1);
            if (d != '.')
            {
                //dow = "dow" + String(i);
                //$("#" + dow).attr("checked","checked");
                $scope.program.day[i] = 1;
            }
        }

        /* Initialize start and stop triggers. */
        $scope.startTriggerChanged();
        $scope.stopTriggerChanged();
        window.onbeforeunload = null;

        /* Initialize sunset/sunrise times */
        //show_offset_time("start-trigger-method", "start-offset", "start-offset-time", "start-time");
        //show_offset_time("stop-trigger-method", "stop-offset", "stop-offset-time", "stop-time");
        $scope.update_effective_start_time();
        $scope.update_effective_stop_time();
    };

    $scope.save_program = function() {
        // Translate day array to days string
        var dstr = "";
        weekdays = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
        for (i = 0; i < 7; i++) {
            dstr += $scope.program.day[i] ? weekdays[i] : ".";
        }
        $scope.program.days = dstr;

        // Save the program
        $http.post('/module/program/' + String($scope.program.programid), {"data": $scope.program}).
            success(function(data, status, headers, config) {
                // Success
                $scope.error = "";
                $scope.message = data;
                window.onbeforeunload = null;
            }).
            error(function(data, status, headers, config) {
                if (data && (data.message)) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to get program data";
                }
            });
    };

    $scope.cancel = function() {
        window.onbeforeunload = null;
        // Get return url from #returnto href. Cancel is the same as Back.
        var returnto = $("#returnto").attr('href');
        window.location.replace(returnto);
    };

    $scope.set_weekdays = function() {
        for (i = 0; i < 5; i++) {
            $scope.program.day[i] = $scope.program.day[i] ? 0 : 1;
        }
    }

    $scope.set_weekenddays = function() {
        for (i = 5; i < 7; i++) {
            $scope.program.day[i] = $scope.program.day[i] ? 0 : 1;
        }
    }

    $scope.update_effective_start_time = function() {
        $scope.calc_start_time = calculate_effective_time($scope.program.start_trigger_method, $scope.program.start_offset, $scope.program.start_time);
    };

    $scope.update_effective_stop_time = function() {
        $scope.calc_stop_time = calculate_effective_time($scope.program.stop_trigger_method, $scope.program.stop_offset, $scope.program.stop_time);
    };

    $scope.startTriggerChanged = function() {
        track_change();
        // Cases for each trigger method. Show/hide group boxes.
        triggerMethod = $("#start-trigger-method").val();
        switch (triggerMethod.toLowerCase())
        {
            case "none":
                $("#start-time-group").hide();
                $("#start-offset-group").hide();
                $("#start-randomize-group").hide();
                break;
            case "clock-time":
                $("#start-time-group").show();
                $("#start-offset-group").show();
                $("#start-randomize-group").show();
                break;
            case "sunset":
                $("#start-time-group").hide();
                $("#start-offset-group").show();
                $("#start-randomize-group").show();
                break;
            case "sunrise":
                $("#start-time-group").hide();
                $("#start-offset-group").show();
                $("#start-randomize-group").show();
                break;
        }

        $scope.update_effective_start_time();
    }

    $scope.stopTriggerChanged = function() {
        track_change();
        // Cases for each trigger method. Show/hide group boxes.
        triggerMethod = $("#stop-trigger-method").val();
        switch (triggerMethod.toLowerCase())
        {
            case "none":
                $("#stop-time-group").hide();
                $("#stop-offset-group").hide();
                $("#stop-randomize-group").hide();
                break;
            case "clock-time":
                $("#stop-time-group").show();
                $("#stop-offset-group").show();
                $("#stop-randomize-group").show();
                break;
            case "sunset":
                $("#stop-time-group").hide();
                $("#stop-offset-group").show();
                $("#stop-randomize-group").show();
                break;
            case "sunrise":
                $("#stop-time-group").hide();
                $("#stop-offset-group").show();
                $("#stop-randomize-group").show();
                break;
        }

        $scope.update_effective_stop_time();
    };
    /*
    For sunset and sunrise base triggers, show the effective time.
    the sunset/sunrise times are in hidden elements. The start/stop
    offset is added to the sunrise/sunset time to obtain the
    effective time. Does not apply to clock-time trigger.
    */
    function calculate_effective_time(method, offset, clock_time){
        if (method.toLowerCase() == "sunset"){
            var sunset = get_sunset();
            var sunset_offset = new Date(sunset.getTime() + offset * 60 * 1000);
            return sunset_offset.toLocaleTimeString();
            //$time.text(format_datetime(sunset));
        }
        else if (method.toLowerCase() == "sunrise"){
            var sunrise = get_sunrise();
            var sunrise_offset = new Date(sunrise.getTime() + offset * 60 *1000);
            return sunrise_offset.toLocaleTimeString();
            //$time.text(format_datetime(sunrise));
        }
        else {
            /*
            TODO Solve this problem...
            Unfortunately, the clock-time string is not in a Javascript friendly format.
            As a result, we have to manipulate the string to get it from a format of
            HH:mm AM to yyyy-mm-ddThh:mm (ISO format). The HH:mm AM format uses 12:00 AM
            to represent midnight, another complicating factor.
            */

            // Clock time as a Date
            var ctd = convert_time(clock_time);
            ctd.setMinutes(ctd.getMinutes() + offset);

            return ctd.toLocaleTimeString();
        }
    };

    // Convert a time string hh:mm am/pm to a Date instance
    function convert_time(timetext) {
        var pat = /(\d{1,2}):(\d{1,2}) *(am|pm)/i;
        var m = pat.exec(timetext);
        var hr = parseInt(m[1]);
        var min = parseInt(m[2]);
        var ampm = m[3].toLowerCase();
        if (hr == 12 && ampm == "am") {
            hr = 0;
        }
        if (ampm == "pm" && hr < 12) {
            hr += 12;
        }
        dt = new Date();
        dt.setHours(hr);
        dt.setMinutes(min);
        dt.setSeconds(0);
        return dt;
    };

    /* Retrieve the sunset time as a Date object */
    function get_sunset(){
        var s = $("#sunset").val();
        // Format: 2015-08-30T19:47:41-05:00
        return new Date(Date.parse(s));
    };

    /* Retrieve the sunrise time as a Date object */
    function get_sunrise(){
        var s = $("#sunrise").val();
        // Format: 2015-08-30T06:58:46-05:00
        return new Date(Date.parse(s));
    };

    function unsaved_changes_warning(e){
        e.returnValue = "You have unsaved changes on this page.";
        /*
        Some browsers (e.g. Chrome, Safari will display the returned text.
        Firefox does not display the returned text.
        */
        return e.returnValue;
    };

    function track_change(){
        window.onbeforeunload = unsaved_changes_warning;
    };
});

/*
Code moved from page
*/

/* Page initialization */
$(document).ready(function() {

    /* Initialize time controls */
    /* We have to explicitly supply the spinnerImage because the widget looks for the
       default in a fixed location (starting from the root of the page). */
    $.timeEntry.setDefaults({
        spinnerImage: "static/timeentry/spinnerBlue.png",
        spinnerBigImage: "static/timeentry/spinnerBlueBig.png",
        ampmPrefix: " "
        });
    $("#start-time").timeEntry();
    $("#stop-time").timeEntry();
});

function showHideFieldset(name){
    fs_name = "#" + name;
    $(fs_name).is(":visible") ? $(fs_name).hide() : $(fs_name).show();
}

/* Valid all inputs on submit */
function validate_inputs(){
    if (!validate_numeric_control("start-offset", "Start offset")){
        return false;
    }
    if (!validate_numeric_control("stop-offset", "Stop offset")){
        return false;
    }
    if (!validate_numeric_control("start-randomize-amount", "Start randomize")){
        return false;
    }
    if (!validate_numeric_control("stop-randomize-amount", "Stop randomize")){
        return false;
    }

    return true;
}

/* Validate a numeric control */
function validate_numeric_control(control_id, name){
    target_id = "#" + control_id
    value = $(target_id).val()
    if (!$.isNumeric(value)){
        alert(name + " must be a number. Try again!");
        $(target_id).focus();
        return false;
    }
    return true;
}

/* Format date/time */
function format_datetime(dt){
    if (dt.getHours() >= 12){
        hours = (dt.getHours() - 12).toFixed(0);
    }
    else{
        hours = dt.getHours().toFixed(0);
    }
    if (hours.length < 2){
        hours = "0" + hours;
    }
    minutes = dt.getMinutes().toFixed(0);
    if (minutes.length < 2){
        minutes = "0" + minutes;
    }
    ampm = dt.getHours() >= 12 ? "PM" : "AM";
    return hours + ":" + minutes + " " + ampm;
}

/*
For sunset and sunrise base triggers, show the effective time.
the sunset/sunrise times are in hidden elements. The start/stop
offset is added to the sunrise/sunset time to obtain the
effective time. Does not apply to clock-time trigger.
*/
function show_offset_time(method_id, offset_id, time_id, clock_time_id){
    var $method = $("#" + method_id);
    var $offset = $("#" + offset_id);
    var $time = $("#" + time_id);

    var offset = parseInt($offset.val());

    var method = $method.val().toLowerCase();
    if (method == "sunset"){
        var sunset = get_sunset();
        sunset.setMinutes(sunset.getMinutes() + offset);
        $time.text(sunset.toLocaleTimeString());
        //$time.text(format_datetime(sunset));
    }
    else if (method == "sunrise"){
        var sunrise = get_sunrise();
        sunrise.setMinutes(sunrise.getMinutes() + offset);
        $time.text(sunrise.toLocaleTimeString());
        //$time.text(format_datetime(sunrise));
    }
    else {
        /*
        Unfortunately, the clock-time string is not in a Javascript friendly format.
        As a result, we have to manipulate the string to get it from a format of
        HH:mm AM to yyyy-mm-ddThh:mm (ISO format). The HH:mm AM format uses 12:00 AM
        to represent midnight, another complicating factor.
        */

        /* We'll use this to get the current date (from time zone and DST purposes) */
        var current_date = new Date();

        /* This is the time from the control (as a Date), but the date is not current. */
        var clock_time = $("#" + clock_time_id).timeEntry('getTime');

        /* Put the current date together with the time from the control */
        clock_time.setFullYear(current_date.getFullYear());
        clock_time.setMonth(current_date.getMonth());
        clock_time.setDate(current_date.getDate());

        /* Adjust the time with the offset value */
        clock_time.setMinutes(clock_time.getMinutes() + offset);

        $time.text(clock_time.toLocaleTimeString());
    }

}

