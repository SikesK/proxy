window.onload = function() {
    $("#accept").click(function () {
       window.location.replace("/sokoban/introduction");
    });
    $("#decline").click(function () {
       window.location.replace("/sokoban/thank_you?done=0");
    });
};