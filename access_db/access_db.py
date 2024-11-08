from firebase import Firebase
import pandas as pd
import time
import pprint as pp
import datetime
import os

COLUMNS = ["age", "ai_knowledge", "education", "email", "exp_additional_info", "exp_rating", "foil_id",
           "gender", "name", "plan_knowledge", "planning_formalisms", "selected_exp"]


class AccessDatabase:
    def __init__(self, ignore_names=None):
        if ignore_names is None:
            ignore_names = []

        firebaseConfig = {
            "apiKey": "AIzaSyAJKQxorOHo7qX_jXZMcwnpeRDJD4SZw0Q",
            "authDomain": "black-box-explanation.firebaseapp.com",
            "databaseURL": "https://black-box-explanation.firebaseio.com",
            "projectId": "black-box-explanation",
            "storageBucket": "black-box-explanation.appspot.com",
            "messagingSenderId": "734956962335",
            "appId": "1:734956962335:web:e574745cc5674fb8538b2a"
        }
        firebase = Firebase(firebaseConfig)
        self.db = firebase.database()
        self.ignore_names = ignore_names

        # get the latest data from the firebase database
        # self.data = self.get_latest_data()

    def get_latest_data(self):
        users_info = self.db.child("users_info").get().val()
        df = pd.DataFrame(columns=COLUMNS)
        for key in users_info:
            info = users_info[key]
            if info['name'] not in self.ignore_names:
                df = df.append(info, ignore_index=True)
        return df

    def save_data_to_csv(self, file_name):
        self.data.to_csv(file_name)
        print("data added to path %s:" % file_name)

    def start_monitor(self, interval=900):
        current_data_count = len(self.db.child("users_info").get().val())
        original_data_count = current_data_count
        while True:
            print("Total data at time ", datetime.datetime.now(), " is ", current_data_count)
            time.sleep(interval)
            new_data_count = len(self.db.child("users_info").get().val())
            if new_data_count > current_data_count:
                os.system('terminal-notifier -sound default -message \'new {} points received\''.format(
                        new_data_count - current_data_count))
            current_data_count = new_data_count

    def get_tail_data(self, tail=1):
        users_info = self.db.child("users_info").get().val()
        tail_data = list(users_info.values())[-tail:]
        pp.pprint(tail_data)

    def save_tail_data(self, tail=1):
        users_info = self.db.child("users_info").get().val()
        tail_data = list(users_info.values())[-tail:]
        df = pd.DataFrame(columns=COLUMNS)
        for data_point in tail_data:
            df = df.append(data_point, ignore_index=True)
        df.to_csv("./latest_tail_data.csv")

if __name__ == "__main__":
    # csv_path = "./latest_data.csv"
    # ignore_username = ["ssreedh3", "test Mudit"]
    # access_db = AccessDatabase(ignore_names=ignore_username)
    # access_db.save_data_to_csv(csv_path)
    access_db = AccessDatabase()
    # access_db.start_monitor()
    access_db.save_tail_data(40)
