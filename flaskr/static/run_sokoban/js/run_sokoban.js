let total_cost = 0;
let key_to_action_map = {
    87: 'Push up',
    65: 'Push left',
    83: 'Push down',
    68: 'Push right',
    37: 'Move left',
    38: 'Move up',
    39: 'Move right',
    40: 'Move down'
};
let valid_action_keys = [87, 65, 83, 68, 37, 38, 39, 40];
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
            xhttp.open("GET", "/sokoban/step?action=" + action_key, true);
            xhttp.send();
        }
    });

};

function attach_button_functionalities() {
    $("#restart_game").click(function () {
        $("#cancel_add_the_concept").trigger("click");
        $("#cancel_select_the_concept").trigger("click");
        game_ended = false;
        control_pause_game("play");
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                let rgb_data = (xhttp.response);
                initialize_game_image(rgb_data);
            }
        };
        xhttp.open("GET", "/sokoban/step?action=" + -1, true);
        xhttp.send();
    });

    $("#add_new_concept").click(function () {
        control_pause_game("pause");
        $("#concept_name").val("");
        $("#concept_description").val("");
        $("#add_new_concept").hide();
        $("#select_concept_from_list").hide();
        $("#add_new_concept_form").show();
    });

    $("#cancel_add_the_concept").click(function () {
        $("#add_new_concept_form").hide();
        $("#add_new_concept").show();
        $("#select_concept_from_list").show();
        control_pause_game("play");
    });

    $("#select_concept_from_list").click(function () {
        $("#select_concept_from_list").hide();
        $("#add_new_concept").hide();
        $("#select_concept_from_list_form").show();
        control_pause_game("pause");
    });

    $("#cancel_select_the_concept").click(function () {
        $("#select_concept_from_list_form").hide();
        $("#select_concept_from_list").show();
        $("#add_new_concept").show();
        control_pause_game("play");
    });

    $("#add_the_concept").click(add_the_concept);

    $("#select_the_concept").click(select_the_concept);

    $("#move_to_next_action").click(move_to_next_action);
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
        if(total_cost === -11) {
            html_str = '<span>Game finished with perfect score of -11</span><br>';
            html_str += '<span>Restart game to play more.</span><br>';
        } else {
            html_str = '<span>Game finished with score of '+ total_cost +'</span><br>';
            html_str += '<span>Restart game to play more.</span><br>';
            html_str += '<span>Remember to explore the game and find ways to improve your score.' +
                    ' Best possible score is -11.</span>';
        }
        $("#game_paused_message").html(html_str);
        $("#game_paused_container").show();
    }
}

function add_the_concept() {
    let concept_name = $("#concept_name").val();
    let concept_description = $("#concept_description").val();
    $("#concept_list").append('<li class="list-group-item">' + concept_name + '</li>');
    current_action_concepts.push([concept_name, concept_description]);
    all_concepts.push([concept_name, concept_description]);
    let select_concept_list = $("#select_concept_list");
    select_concept_list.removeAttr("disabled");
    if (no_concept_added) {
        select_concept_list.html('<option value="'+ concept_id+'">' + concept_name + '</option>');
        $("#select_the_concept").removeAttr("disabled");
        no_concept_added = false;
    } else {
        select_concept_list.append('<option value="'+ concept_id+'">' + concept_name + '</option>');
    }
    concept_id += 1;
    $("#cancel_add_the_concept").trigger("click");
}

function select_the_concept() {
    let concept_idx = parseInt($("#select_concept_list").val());
    let concept = all_concepts[concept_idx];
    let concept_name = concept[0];
    let concept_description = concept[1];
    current_action_concepts.push([concept_name, concept_description]);
    $("#concept_list").append('<li class="list-group-item">' + concept_name + '</li>');
    $("#cancel_select_the_concept").trigger("click");
}

function move_to_next_action() {
    if(current_action_idx === action_list.length-1){
        let message = "If you are sure you have provided all the concepts for the action -- " + action_list[current_action_idx] +"--, then press Ok to finish the study. Otherwise press Cancel";
        let response = confirm(message);
        if(response) {
            let current_action = action_list[current_action_idx];
            action_to_concepts[current_action] = current_action_concepts;
            finish_run_sokoban();
        }
    } else {
        let message = "If you are sure you have provided all the concepts for the action -- " + action_list[current_action_idx] +"--, then press Ok to move on to the next action. Otherwise press Cancel";
        let response = confirm(message);
        if(response) {
            let current_action = action_list[current_action_idx];
            action_to_concepts[current_action] = current_action_concepts;
            current_action_concepts = [];
            current_action_idx += 1;
            initialize_window_for_action();
            $("#restart_game").trigger("click");
            if(current_action_idx === action_list.length - 1) {
                $("#move_to_next_action").html("Finish study");
            }
        }
    }
}

function initialize_window_for_action() {
    $("#instruction_question").html("Play the game and provide all the relevant concept for the action: " + action_list[current_action_idx]);
    $("#action_name_in_list_of_concepts").html("Concepts added for action: " + action_list[current_action_idx]);
    $("#concept_list").html("");
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
}

function update_sokoban_image(rgb_data, cost_str, done_str) {
    let sokoban_img_container = document.getElementById('sokoban_image_container');
    let html_str = '<div id="game_paused_container" class="instructions"><span id="game_paused_message"></span></div>';
    html_str += '<img id="sokoban_image" src="data:image/png;base64,' + rgb_data + '"/>';
    sokoban_img_container.innerHTML = html_str;
    $("#last_action").html(key_to_action_map[last_action_key]);
    $("#action_cost").html(cost_str);
    let cost = parseFloat(cost_str);
    total_cost += cost;
    $("#total_cost").html(total_cost);
    if (done_str === 'True'){
        game_ended = true;
        control_pause_game();
    }
}

function finish_run_sokoban() {
    //todo handle if JSON.stringify doesn't work for a random text input
    let xhttp = new XMLHttpRequest();   // new HttpRequest instance
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            window.location.replace("/sokoban/thank_you?done=1");
        }
    };
    xhttp.open("POST", "/sokoban/save_concept_data");
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(action_to_concepts));
}