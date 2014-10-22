/*
    Watermark plugin
    By Mitch Satchwell October 29th, 2012
    http://mitchsatchwell.com/jquery-watermark-plugin/

    Modifications by Dave Hocker October 21, 2014
    AtHomeX10@gmail.com
*/

(function($){
$.fn.watermark = function(options) {
    var settings = $.extend({
        'text': 'watermark',
        'color': '#c0c0c0',
        'font_style': 'italic',
        }, options);
    var original_color = $(this).css('color');
    var original_font_style = $(this).css('font-style');
    var class_marker = "watermark";

    $(this).focus(function() {
        if ($(this).hasClass(class_marker)) {
            $(this).removeClass(class_marker);
            $(this).val('');
            $(this).css('color', original_color);
            $(this).css('font-style', original_font_style);
        }
    });

    $(this).blur(function() {
        if($(this).val().length == 0) {
            $(this).addClass(class_marker);
            $(this).val(settings.text);
            $(this).css('color', settings.color);
            $(this).css('font-style', settings.font_style);
        }
    });

    // Initialize the element
    this.blur();

    return this;
};
}(jQuery));