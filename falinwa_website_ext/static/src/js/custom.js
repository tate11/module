$(function() {
    var header = $(".custom-fixed-00");
    $(window).scroll(function() {
        var scroll = $(window).scrollTop();
        if (scroll >= 650) {
            header.removeClass('custom-fixed-00').addClass("custom-fixed-01");
        } else {
            header.removeClass("custom-fixed-01").addClass('custom-fixed-00');
        }
    });
    new WOW().init();
});