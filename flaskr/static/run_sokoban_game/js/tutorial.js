// let total_images = 7;
let total_images = 8;
let current_image = 1;
window.onload = function() {
    if(total_images === 1) {
        $("#next_img").attr("disabled", "disabled");
    }

    $("#prev_img").click(function () {
        current_image -= 1;
        $("#tutorial_image").attr("src", "/static/run_sokoban/tutorial_images/tutorial_image_" + current_image + ".png")
        $("#next_img").removeAttr("disabled");
        if(current_image == 1) {
            $("#prev_img").attr("disabled", "disabled");
        }
    });

    $("#next_img").click(function () {
        current_image += 1;
        $("#tutorial_image").attr("src", "/static/run_sokoban/tutorial_images/tutorial_image_" + current_image + ".png")
        $("#prev_img").removeAttr("disabled");
        if(current_image === total_images) {
            $("#next_img").attr("disabled", "disabled");
            $("#play_sokoban").css("visibility", "visible");
        }
    });

    $("#play_sokoban").click(function () {
    //    window.location.replace("/sokoban/run");
       window.location.replace("/sokoban_game/run");
    });

    $(document).keydown(function(e){
        let key = e.which;
        if (key === 37 && current_image !== 1) {
            e.preventDefault();
            $("#prev_img").trigger("click");
        }
        if(key === 39 && current_image !== total_images) {
            e.preventDefault();
            $("#next_img").trigger("click")
        }
    });
};