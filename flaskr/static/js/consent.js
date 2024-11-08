window.onload = function() {
    $("#accept").click(function () {
       //window.location.replace("/study/introduction");
       window.location.replace("/introduction");
    });
    $("#decline").click(function () {
       window.location.replace("/study/declined");
    });
};