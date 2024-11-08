//USING THIS ONE
window.onload = function() {
    $("#accept").click(function () {
       window.location.replace("/sokoban_game/introduction");
    });
    $("#decline").click(function () {
       window.location.replace("/sokoban_game/thank_you?done=0");
    });
};