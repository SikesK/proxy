from flask import Blueprint, render_template, request, session, jsonify, send_file, Flask
import gym
#import gym_sokoban_flip_mod


#from gym_sokoban_mod_prec.envs import CustomGridEnv

#from custom_grid_env import CustomGridEnv
#rom custom_grid_env import CustomGridEnv 

import gym_sokoban_mod_prec

#import gymnasium as gym
#import gym_miniworld


from PIL import Image
import io
import base64
#from flaskr.db import get_db
from db import get_db # Kelsey added
import random
import time
#from flaskr.foil_info import foil_info
from foil_info import foil_info # Kelsey added
#from flaskr.scripts.Explainer import Explainer
from scripts.Explainer import Explainer # Kelsey added
from random import shuffle

sokoban_game = Blueprint('sokoban_game', __name__, url_prefix='/sokoban_game')

SCORES = [('Effort vs Performance', 'Effort', 'Performance'),
          ('Temporal Demand vs Frustration', 'Temporal Demand', 'Frustration'),
          ('Temporal Demand vs Effort', 'Temporal Demand', 'Effort'),
          ('Physical Demand vs Frustration', 'Physical Demand', 'Frustration'),
          ('Performance vs Frustration', 'Performance', 'Frustration'),
          ('Physical Demand vs Temporal Demand', 'Physical Demand', 'Temporal Demand'),
          ('Physical Demand vs Performance', 'Physical Demand', 'Performance'),
          ('Temporal Demand vs Mental Demand', 'Temporal Demand', 'Mental Demand'),
          ('Frustration vs Effort', 'Frustration', 'Effort'),
          ('Performance vs Mental Demand', 'Performance', 'Mental Demand'),
          ('Performance vs Temporal Demand', 'Performance', 'Temporal Demand'),
          ('Mental Demand vs Effort', 'Mental Demand', 'Effort'),
          ('Mental Demand vs Physical Demand', 'Mental Demand', 'Physical Demand'),
          ('Effort vs Physical Demand', 'Effort', 'Physical Demand'),
          ('Frustration vs Mental Demand', 'Frustration', 'Mental Demand')]

    #[("Effort vs Mental Demands","Effort", "Mental Demands"), ("Physical Demand vs Mental Demands","Physical Demand", "Mental Demands")]
RATING_DIMENSIONS = ['mental_demand','physical_demand','temporal_demand','performance','effort','frustration']


@sokoban_game.route('/introduction') #this is shown second (see consent.js)
def index():
    return render_template('run_sokoban_game/introduction.html')


@sokoban_game.route('/') #this is the consent page, shown first
def consent():
    explanatory_set = request.args.get("explanatory_set")
    if explanatory_set == '0':
        session["explanation_type"] = 'none'
        session["user_info"] = {
            "explanation_type": 'none'
        }
    elif explanatory_set == '1':
        session["explanation_type"] = 'abstract'
        session["user_info"] = {
            "explanation_type": 'abstract'
        }
        session["predicates_used"] = []
    else:
        session["explanation_type"] = 'none'
        session["user_info"] = {
            "explanation_type": 'none'
        }
    session["user_info"]["steps_taken"] = 0
    return render_template('run_sokoban_game/consent.html')


@sokoban_game.route('/instructions', methods=['POST']) #this is shown third
def instructions():
    user_info = session.get("user_info")
    user_info["name"] = request.form.get('name', "")
    user_info["email"] = request.form.get("email", "")

    # logging data start
    logging_data = {}
    logging_data["name"] = user_info["name"]
    logging_data["email"] = user_info["email"]
    #db = get_db()
    #db.child("users_info_logging").push(logging_data)
    # logging data end

    session["user_info"] = user_info
    return render_template('run_sokoban_game/instructions.html')


@sokoban_game.route('/tutorial')
def tutorial():
    return render_template('run_sokoban_game/tutorial.html')

@sokoban_game.route('/countdown') #this is shown fourth
def countdown():
    return render_template('run_sokoban_game/countdown.html')

@sokoban_game.route('/quiz')
def quiz():    
    return render_template('run_sokoban_game/quiz_succeed.html')

@sokoban_game.route('/quiz_response', methods=['POST'])
def quiz_response():
    test_name = request.form.get("image", "")

    expected_answers = None
    for t_name, t_file, t_conc in foil_info['game_foil']['test_images']:
        if t_name == test_name:
            expected_answers = t_conc.copy()

    final_concepts = foil_info["game_foil"]["all_concepts"]
    for conc, conc_description, image in final_concepts:
        if (conc in expected_answers and request.form.get(conc, "") != conc) or\
                (conc not in expected_answers and request.form.get(conc, "") != ""):
            return render_template('run_sokoban_game/quiz_fail.html')
    return render_template('run_sokoban_game/quiz_succeed.html')




@sokoban_game.route('/run')
def run_custom_grid():
    if 'user_info' not in session:
        return render_template('run_custom_grid_game/error.html')
    if "start_time" not in session:
        session["start_time"] = time.time()
        
    env_name = 'CustomGridEnv-v0'  # Use the custom grid environment name
    env = gym.make(env_name)

    print("env", env)
    session["env"] = env
    session["executed_plan"] = []
    env.seed(0)
    obs = env.reset()
    rgb_img = env.render("rgb_array")
    img = Image.fromarray(rgb_img, mode="RGB")
    file_obj = io.BytesIO()
    img.save(file_obj, format="PNG")
    contents = file_obj.getvalue()
    encoded_contents = base64.b64encode(contents)

    action_list = []  # Define any actions you want to include

    return render_template('run_custom_grid_game/run_custom_grid_game.html',
                           rgb_data=encoded_contents.decode(),
                           action_list=action_list,
                           explanation_type=session.get("explanation_type"))




#Orignal Run you were using yesterday
# @sokoban_game.route('/run') #this is shown fifth
# def run_sokoban():
#     if 'user_info' not in session:
#         render_template('run_sokoban_game/error.html')
#     if "start_time" not in session:
#         session["start_time"] = time.time()
#     env_name = 'Sokoban-mod-prec-v0'
#     env = gym.make(env_name)
#     session["env"] = env
#     session["executed_plan"] = []
#     #session['user_info'] = {}
#     env.seed(0)
#     env.reset()
#     rgb_img = env.render("rgb_array")
#     img = Image.fromarray(rgb_img, mode="RGB")
#     file_obj = io.BytesIO()
#     img.save(file_obj, format="PNG")
#     contents = file_obj.getvalue()
#     encoded_contents = base64.b64encode(contents)
#     # action_list = ["Move up", "Move down", "Move left", "Move right", "Push up", "Push down", "Push left", "Push right"]
#     #action_set_id = session.get("action_set_id")
#     id_to_action_set = {
#         "1": ["Move up", "Move down", "Move left", "Move right"],
#         "2": ["Push up", "Push down", "Push left", "Push right"]
#     }
#     action_list = id_to_action_set['1']#[action_set_id]
#     return render_template('run_sokoban_game/run_sokoban_game.html',
#                            rgb_data=encoded_contents.decode(),
#                            action_list=action_list,
#                            explanation_type=session["explanation_type"])




@sokoban_game.route('/concept')
def concept():
    final_concepts = foil_info["game_foil"]["all_concepts"]
    # final_concepts.extend(current_foil_concepts)
    random.shuffle(final_concepts)
    return render_template('run_sokoban_game/concepts.html', current_foil=final_concepts)


@sokoban_game.route('/step', methods=['GET'])
def step_sokoban():
    key_to_action_map = {
        '13': 0,
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
    session["user_info"]["steps_taken"] += 1
    if action_key == "-1":
        env.seed(0)
        env.reset()
        session["executed_plan"] = []
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
        session["executed_plan"].append(action)
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


# @sokoban.route('/save_concept_data', methods=['POST'])
# def save_concept_data():
#     user_info = session.get("user_info")
#     session["user_info"] = user_info
#     session["time_taken"] = 0
#     db = get_db()
#     db.child("user_trial").push(user_info)
#     return "success"

@sokoban_game.route('/explanation.json', methods=['GET'])
def explanation():
    import json
    print ("explanation type", session["explanation_type"])
    if session["explanation_type"] == "abstract":
        print ("Executed plan",session["executed_plan"])
        exp = Explainer('flaskr/domains/sokoban_switch.pddl', 'flaskr/domains/sokoban_problem.pddl', (3, 7), (3, 6))
        exp_str, domain_str, filtered_preds = exp.find_explanation_text(session["executed_plan"], abstract=True, prev_failure_preds=set(session["predicates_used"]))
        session["predicates_used"] = list(filtered_preds)
        return json.dumps({"failure_text":exp_str, "domain_str": domain_str})
    else:
        exp = Explainer('flaskr/domains/sokoban_switch.pddl', 'flaskr/domains/sokoban_problem.pddl', (3, 8), (3, 7))
        exp_str, domain_str, filtered_preds = exp.find_explanation_text(session["executed_plan"])#, abstract=True)
        return json.dumps({"failure_text": exp_str, "domain_str": domain_str})


@sokoban_game.route('/background', methods=['POST'])
def background():
    user_info = session.get("user_info")
    user_info["exp_rating"] = request.form.get("likert_radio", "")
    user_info["explanation_seen"] = request.form.get("explanation_seen", "")
    user_info["exp_additional_info"] = request.form.get("additional_info", "")
    session["user_info"] = user_info
    return render_template('run_sokoban_game/background.html')


@sokoban_game.route('/thank_you', methods=['POST'])
def thank_you():
    user_info = session.get("user_info")
    print ("user infor", user_info)
    user_info["age"] = request.form.get("age", "")
    user_info["gender"] = request.form.get("gender", "")
    user_info["education"] = request.form.get("education", "")
    user_info["ai_knowledge"] = request.form.get("ai_knowledge", "")
    user_info["plan_knowledge"] = request.form.get("plan_knowledge", "")
    user_info["planning_formalisms"] = request.form.get("planning_formalisms", "")
    session["user_info"] = user_info
    data = session["user_info"]
    data['minutes'] = session['minutes']
    data['seconds'] = session['seconds']
    data['game_status'] = session['game_status']
    data['start_time'] = session['start_time']
    data['end_time'] = session['end_time']
    data['USER_RATINGS'] = session['USER_RATINGS']
    #db = get_db()
    #db.child("users_info").push(data)
    return render_template('run_sokoban_game/thank_you.html')


@sokoban_game.route('/collect_feedback')
def collect_feedback():
    session["end_time"] = time.time()
    done = int(request.args.get("done"))
    minutes = int(request.args.get("minutes"))
    seconds = int(request.args.get("seconds"))
    session['minutes'] = minutes
    session['seconds'] = seconds
    session['game_status'] = done
    message = ""
    if done:
        message = "Thank you for taking the study. You finished the game in "+str(minutes)+" minutes and "+str(seconds)+" seconds. After the end of the study we will notify you if you are eligible for any additional bonuses"
        return render_template("run_sokoban_game/collect_feedback.html", message=message)
    else:
        message = "Thank you for taking the study, but you were not able to finish the game in time."
        return render_template("run_sokoban_game/collect_feedback.html", message=message)


@sokoban_game.route('/tlx_ratings', methods=["POST"])
def tlx_ratings():

    user_info = session.get("user_info")
    user_info["exp_rating"] = request.form.get("likert_radio", "")
    user_info["explanation_seen"] = request.form.get("explanation_seen", "")
    user_info["exp_additional_info"] = request.form.get("additional_info", "")
    session["user_info"] = user_info


    message = ""

    return render_template("run_sokoban_game/tlx_ratings.html", message=message)

  
@sokoban_game.route('/tlx_scoring_instructions')
def tlx_scoring_instructions():

    message = ""

    return render_template("run_sokoban_game/tlx_ratings.html", message=message)

@sokoban_game.route('/tlx_scoring_page_1',methods=["POST"]) #this is shown kind of last
def tlx_scoring_page_1():
    prev_key, _, _ = session['scoring_order'][session['current_scoring_id']]
    session['scoring_info'][prev_key] = request.form.get(prev_key,"")
    session['current_scoring_id'] += 1
    session['per_scale_weight'][session['scoring_info'][prev_key].lower().replace(' ','_')] += 1


    if session['current_scoring_id'] < len(session['scoring_order']):
        key, measure_1, measure_2 = session['scoring_order'][session['current_scoring_id']]
        return render_template("run_sokoban_game/tlx_scoring_page.html", key=key, measure_1=measure_1, measure_2=measure_2)
    else:
        print (session['per_scale_weight'])
        return render_template("run_sokoban_game/thank_you.html")


@sokoban_game.route('/tlx_scoring_page',methods=["POST"])
def tlx_scoring_page():
    # TODO Get the rating
    session["USER_RATINGS"] = {}
    for key in RATING_DIMENSIONS:
        if key not in request.form:
            message = "There was a missing value for rating scale: "+ key.replace("_"," ").title()
            return render_template("run_sokoban_game/tlx_ratings.html", message=message)

        session["USER_RATINGS"][key] = request.form.get(key)


    session['scoring_order'] = SCORES.copy()
    shuffle(session['scoring_order'])
    session['scoring_info'] = {}
    session['per_scale_weight'] = {k:0 for k in RATING_DIMENSIONS}
    session['current_scoring_id'] = 0

    if session['current_scoring_id'] < len(session['scoring_order']):
        key, measure_1, measure_2 = session['scoring_order'][session['current_scoring_id']]
        return render_template("run_sokoban_game/tlx_scoring_page.html", key=key, measure_1=measure_1, measure_2=measure_2)
    else:
        return render_template("run_sokoban_game/thank_you.html")
    


# if __name__ == "__main__":
#     # Your main code here
#     print("Script is running")  