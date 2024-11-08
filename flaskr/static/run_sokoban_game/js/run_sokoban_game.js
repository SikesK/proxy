
let total_cost = 0;
let key_to_action_map = {
    87: 'Push up',
    65: 'Push left',
    83: 'Push down',
    68: 'Push right',
    37: 'Move left',
    38: 'Move up',
    39: 'Move right',
    40: 'Move down',
    13: 'Activate'
};
let valid_action_keys = [87, 65, 83, 68, 37, 38, 39, 40, 13];
let last_action_key;
let play_game = true;
let action_to_concepts = {};
let current_action_idx = 0;
let concept_id = 0;
let current_action_concepts = [];
let all_concepts = [];
let no_concept_added = true;
let current_rgb_str;
let game_pause_message;
let game_ended = false;
window.onload = function() {
    initialize_game_image(init_rgb_data);
    attach_button_functionalities();
    initialize_window_for_action();
    $(document).keydown(function(e) {
        let action_key = e.which;
        if(play_game && valid_action_keys.includes(action_key)) {
            e.preventDefault();
            last_action_key = action_key;
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState === 4 && this.status === 200) {
                    let response = (xhttp.response);
                    let cost_idx = response.search("cost:");
                    let rgb_idx = response.search("rgb_str:");
                    let cost_str = response.slice(cost_idx+5, rgb_idx);
                    let done_str = response.slice(5, cost_idx);
                    let updated_rgb_data = response.slice(rgb_idx+8);
                    update_sokoban_image(updated_rgb_data, cost_str, done_str);
                }
            };
            xhttp.open("GET", "/sokoban_game/step?action=" + action_key, true);
            xhttp.send();
        }
    });

};

function attach_button_functionalities() {
    $("#restart_game").click(function () {
        $("#cancel_add_the_concept").trigger("click");
        $("#cancel_select_the_concept").trigger("click");
        game_ended = false;

        explanation_html_str = "";

        $('#explanatory_content').html(explanation_html_str);
        $('#explanatory_content').show();


        control_pause_game("play");
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                let rgb_data = (xhttp.response);
                initialize_game_image(rgb_data);
            }
        };
        xhttp.open("GET", "/sokoban_game/step?action=" + -1, true);
        xhttp.send();
    });

}

function control_pause_game(status){
    if (!game_ended) {
        if (status === "pause") {
            play_game = false;
            $("#game_paused_message").html("Game paused. Finish adding concept or cancel to unpause game.");
            $("#game_paused_container").show();
        } else if (status === "play") {
            play_game = true;
            $("#game_paused_container").hide();
        }
    } else {
        play_game = false;
        let html_str;
        if(current_cost >= 100) {

            html_str = '<span>Goal Achieved</span><br>';
            var now = new Date().getTime();
            var saved_start_time = parseInt(window.localStorage.getItem("start_time"));
            var distance = now - saved_start_time;

            // Time calculations for days, hours, minutes and seconds
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);
            finish_run_sokoban(1,minutes,seconds)
            html_str += '<span>Total time taken '+minutes+'m '+seconds+'s</span><br>';
        } else {
//        '87': 1,
//        '65': 3,
//        '83': 2,
//        '68': 4,
            html_str = '<span>Invalid move!! Game failed</span><br>';
            html_str += '<span>Restart game to play more.</span><br>';
            $("#game_paused_message").html(html_str);
            $("#game_paused_container").show();
            // There should be a check here on what kind of failure state it is and what are the action
                //var explanation_text = "None";
                explanation_html_str = "<button class='accordion'>Failure State and Cause</button>\n <div id='exp_panel' class='panel'> </div> <br><button class='accordion'>Actions the Player can perform</button>\n <div id='domain_panel' class='panel'> </div>";

                $('#explanatory_content').html(explanation_html_str);
                $('#explanatory_content').show();
                var explanation_text;
                $.getJSON('/sokoban_game/explanation.json', function(data) {
                explanation_text=data.failure_text;
                explanation_panel_txt = " <p>"+explanation_text+"</p>"
                $('#exp_panel').html(explanation_panel_txt);
                $('#domain_panel').html(data.domain_str);

                });

                //alert(data.text);
                //explanation_html_str = "<button class='accordion'>Section 1</button>\n <div class='panel'> \n <p>"+data.text+".</p>\n</div>";

                //});



var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}

        }

    }
}



function initialize_window_for_action() {
    $("#instruction_question").html("Play the game and try to finish it as soon as possible");
}

function initialize_game_image(rgb_data) {
    let sokoban_img_container = document.getElementById('sokoban_image_container');
    let html_str = '<div id="game_paused_container" class="instructions"><span id="game_paused_message"></span></div>';
    html_str += '<img id="sokoban_image" src="data:image/png;base64,' + rgb_data + '"/>';
    sokoban_img_container.innerHTML = html_str;
    $("#final_score_text").hide();
    $("#last_action").html("&#x2015;");
    $("#action_cost").html("&#x2015;");
    $("#total_cost").html("&#x2015;");
    total_cost = 0;
    current_cost = 0;
}

function update_sokoban_image(rgb_data, cost_str, done_str) {
    let sokoban_img_container = document.getElementById('sokoban_image_container');
    let html_str = '<div id="game_paused_container" class="instructions"><span id="game_paused_message"></span></div>';
    html_str += '<img id="sokoban_image" src="data:image/png;base64,' + rgb_data + '"/>';
    sokoban_img_container.innerHTML = html_str;
    $("#last_action").html(key_to_action_map[last_action_key]);
    $("#action_cost").html(cost_str);
    let cost = parseFloat(cost_str);
    current_cost = cost
    total_cost += cost;
    $("#total_cost").html(total_cost);
    if (done_str === 'True'){
        game_ended = true;
        control_pause_game();
    }
}

function finish_run_sokoban(done=0,minutes=-1, seconds=-1) {
    //todo handle if JSON.stringify doesn't work for a random text input
    //let xhttp = new XMLHttpRequest();   // new HttpRequest instance
    //xhttp.onreadystatechange = function() {
        //if (this.readyState === 4 && this.status === 200) {
    window.location.replace("/sokoban_game/collect_feedback?done="+done+"&minutes="+minutes+"&seconds="+seconds);
        //}
    //};
//    let user_blob = new Map();
//    user_blob['done'] = done;
//    user_blob['minutes'] = minutes;
//    user_blob['seconds'] = seconds;
//   xhttp.open("POST", "/sokoban/save_concept_data");
//    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//    xhttp.send(JSON.stringify(action_to_concepts));
}
