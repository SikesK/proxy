from flask import Blueprint, render_template, request, session, jsonify, send_file
import gym
# import gym_sokoban_flip_mod
import gym_sokoban_mod
from PIL import Image
import io
import base64
from flaskr.db import get_db

sokoban = Blueprint('sokoban', __name__, url_prefix='/sokoban')


@sokoban.route('/introduction')
def index():
    return render_template('run_sokoban/introduction.html')


@sokoban.route('/')
def consent():
    action_set_id = request.args.get("action_set_id")
    session["action_set_id"] = action_set_id
    session["user_info"] = {
        "action_set_id": action_set_id
    }
    return render_template('run_sokoban/consent.html')


@sokoban.route('/instructions', methods=['POST'])
def instructions():
    user_info = session.get("user_info")
    user_info["name"] = request.form.get('name', "")
    user_info["email"] = request.form.get("email", "")
    session["user_info"] = user_info
    return render_template('run_sokoban/instructions.html')


@sokoban.route('/tutorial')
def tutorial():
    return render_template('run_sokoban/tutorial.html')


@sokoban.route('/run')
def run_sokoban():
    env_name = 'Sokoban-mod-v0'
    env = gym.make(env_name)
    session["env"] = env
    env.seed(0)
    env.reset()
    rgb_img = env.render("rgb_array")
    img = Image.fromarray(rgb_img, mode="RGB")
    file_obj = io.BytesIO()
    img.save(file_obj, format="PNG")
    contents = file_obj.getvalue()
    encoded_contents = base64.b64encode(contents)
    # action_list = ["Move up", "Move down", "Move left", "Move right", "Push up", "Push down", "Push left", "Push right"]
    action_set_id = session.get("action_set_id")
    id_to_action_set = {
        "1": ["Move up", "Move down", "Move left", "Move right"],
        "2": ["Push up", "Push down", "Push left", "Push right"]
    }
    action_list = id_to_action_set[action_set_id]
    return render_template('run_sokoban/run_sokoban.html',
                           rgb_data=encoded_contents.decode(),
                           action_list=action_list)


@sokoban.route('/step', methods=['GET'])
def step_sokoban():
    key_to_action_map = {
        '87': 1,
        '65': 3,
        '83': 2,
        '68': 4,
        '37': 7,
        '38': 5,
        '39': 8,
        '40': 6
    }
    action_key = request.args.get("action")
    env = session.get("env")
    if action_key == "-1":
        env.seed(0)
        env.reset()
        rgb_img = env.render("rgb_array")
        img = Image.fromarray(rgb_img, mode="RGB")
        file_obj = io.BytesIO()
        img.save(file_obj, format="PNG")
        contents = file_obj.getvalue()
        encoded = base64.b64encode(contents)
        rgb_str = encoded.decode()
        return rgb_str
    else:
        action = key_to_action_map[action_key]
        observation, reward, done, info = env.step(action)
        # cost = -1 * reward
        rgb_img = env.render("rgb_array")
        img = Image.fromarray(rgb_img, mode="RGB")
        file_obj = io.BytesIO()
        img.save(file_obj, format="PNG")
        contents = file_obj.getvalue()
        encoded = base64.b64encode(contents)
        rgb_str = encoded.decode()
        final_response = "done:" + str(done) + "cost:" + str(reward) + "rgb_str:" + rgb_str
        return final_response


@sokoban.route('/save_concept_data', methods=['POST'])
def save_concept_data():
    user_info = session.get("user_info")
    user_info["action_to_concepts"] = request.json
    session["user_info"] = user_info
    db = get_db()
    db.child("users_info_concept").push(user_info)
    return "success"


@sokoban.route('/thank_you')
def thank_you():
    done = int(request.args.get("done"))
    message = None
    if done:
        message = "Thank you for taking the study. You may close the window now."
        return render_template("run_sokoban/thank_you.html", message=message)
    else:
        message = "Thank you for your interest, but you are not eligible for the study. You may close the window now."
        return render_template("run_sokoban/thank_you.html", message=message)
