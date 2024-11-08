import os
from flask import Flask
#from firebase import Firebase
from flask_session import Session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',

    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('mac.cfg', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'
#    firebaseConfig = {
#        "apiKey": "AIzaSyAJKQxorOHo7qX_jXZMcwnpeRDJD4SZw0Q",
#        "authDomain": "black-box-explanation.firebaseapp.com",
#        "databaseURL": "https://black-box-explanation.firebaseio.com",
#        "projectId": "black-box-explanation",
#        "storageBucket": "black-box-explanation.appspot.com",
#        "messagingSenderId": "734956962335",
#        "appId": "1:734956962335:web:e574745cc5674fb8538b2a"
#    }


    firebaseConfig = {
        "apiKey": "AIzaSyDNMJCRAudMEMWxxWbY8yFRcS8H8u9Fv0w",
        "authDomain": "blackbox-1a5e9.firebaseapp.com",
        "databaseURL": "https://blackbox-1a5e9.firebaseio.com",
        "projectId": "blackbox-1a5e9",
        "storageBucket": "blackbox-1a5e9.appspot.com",
        "messagingSenderId": "494009694775",
        "appId": "1:494009694775:web:a7fb6ab633b6a9163bddb2",
        "measurementId": "G-7VNKXE77QD"
    }


    #firebase = Firebase(firebaseConfig)
    #app.config['firebase'] = firebase

    # from . import db
    # db.init_app(app)

    #from . import user_study
    #app.register_blueprint(user_study.study)

    #from . import run_sokoban
    #app.register_blueprint(run_sokoban.sokoban)

    from . import run_sokoban_game
    app.register_blueprint(run_sokoban_game.sokoban_game)



    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = '/tmp/black_box_session'
    Session(app)
    return app
