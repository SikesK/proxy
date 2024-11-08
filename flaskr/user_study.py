from flask import Blueprint, render_template, request, session, jsonify, send_file
from flaskr.foil_info import foil_info
import json
import random
from flaskr.db import get_db
import gym
import numpy as np
from PIL import Image
import io
import base64

study = Blueprint('study', __name__, url_prefix='/study')


@study.route('/')
def consent():
    foil_id = request.args.get("foil_id")
    session["foil_id"] = foil_id
    session["user_info"] = {
        "foil_id": foil_id
    }
    return render_template('consent.html')


@study.route('/introduction')
def index():
    return render_template('introduction.html')


@study.route('/instructions', methods=['POST'])
def instructions():
    user_info = session.get("user_info")
    user_info["name"] = request.form.get('name', "")
    user_info["email"] = request.form.get("email", "")
    session["user_info"] = user_info
    return render_template('instructions.html')


@study.route('/concept')
def concept():
    current_foil_concepts = foil_info["foil" + session.get("foil_id")]["concepts"]
    important_concept = foil_info["foil" + session.get("foil_id")]["important_concept"]
    final_concepts = [important_concept]
    # print(current_foil_concepts)
    final_concepts.extend(random.sample(current_foil_concepts, 4))
    # final_concepts.extend(current_foil_concepts)
    random.shuffle(final_concepts)
    return render_template('concepts.html', current_foil=final_concepts)


@study.route('/plan_and_foil')
def plan_and_foil():
    current_foil_info = foil_info["foil" + session.get("foil_id")]
    plan_video_loc = current_foil_info["plan_video_loc"]
    plan_goal = current_foil_info["plan_goal"]
    foil_image_loc = current_foil_info["foil_image_loc"]
    foil_text = current_foil_info["foil_text"]
    return render_template('plan_and_foil.html',
                           plan_video_loc=plan_video_loc,
                           plan_goal=plan_goal,
                           foil_image_loc=foil_image_loc,
                           foil_text=foil_text)


@study.route('/explanation')
def explanation():
    current_foil_info = foil_info["foil" + session.get("foil_id")]
    explanations = current_foil_info["foil_explanation"]
    foil_text = current_foil_info["foil_text"]
    random.shuffle(explanations)
    return render_template('explanation.html', explanations=explanations, foil_text=foil_text)


@study.route('/rate_exp', methods=['POST'])
def rate_exp():
    user_info = session.get("user_info")
    selected_exp = request.form.get("likert_radio", "")
    user_info["selected_exp"] = selected_exp
    session["user_info"] = user_info
    current_foil_info = foil_info["foil" + session.get("foil_id")]
    concept_rating_ques = current_foil_info["concept_rating_ques"][selected_exp]
    return render_template('rate_exp.html', concept_rating_ques=concept_rating_ques)


@study.route('/background', methods=['POST'])
def background():
    user_info = session.get("user_info")
    user_info["exp_rating"] = request.form.get("likert_radio", "")
    user_info["exp_additional_info"] = request.form.get("additional_info", "")
    session["user_info"] = user_info
    return render_template('background.html')


@study.route('/thank_you', methods=['POST'])
def thank_you():
    user_info = session.get("user_info")
    user_info["age"] = request.form.get("age", "")
    user_info["gender"] = request.form.get("gender", "")
    user_info["education"] = request.form.get("education", "")
    user_info["ai_knowledge"] = request.form.get("ai_knowledge", "")
    user_info["plan_knowledge"] = request.form.get("plan_knowledge", "")
    user_info["planning_formalisms"] = request.form.get("planning_formalisms", "")
    session["user_info"] = user_info
    data = session["user_info"]
    db = get_db()
    db.child("users_info").push(data)
    return render_template('thank_you.html', store=list(session["user_info"].items()))


@study.route('/declined')
def declined():
    return render_template('declined.html')

# @bp.before_app_request
# def save_logged_in_user():
#     user_name = session.get('user_name')
#     if user_name is None:
#         g.user = None
#     else:
#         g.user = user_name
