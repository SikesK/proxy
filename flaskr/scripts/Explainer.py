#No Operation	0
# Push Up	1
# Push Down	2
# Push Left	3
# Push Right	4
# Move Up	5
# Move Down	6
# Move Left	7
# Move Right	8
#from flaskr.scripts.model_parser import Parser
#from flaskr.scripts.constants import *

from .model_parser import Parser #Kelsey added
from .constants import * #Kelsey added


VAR_SYMBOL = "?"

class Explainer():
    def __init__(self, domain_file, problem_file, player_pos, box_pos):
        self.init_player_pos = player_pos
        self.box_pos = box_pos
        self.parser = Parser()
        self.model = self.parser.parse_model(domain_file, problem_file)

    def find_next_state(self, state, act):
        # Assume all actions are executable
        grounded_act = self.parser.get_grounded_action_definition(act, self.model)
        return (state - grounded_act[DELS])| grounded_act[ADDS]

    def find_failure(self, state, act):
        # Assuming only positive preconditions
        print ("action", act)
        grounded_act = self.parser.get_grounded_action_definition(act, self.model)
        return list(grounded_act[POS_PREC] - state)[0]

    def get_proposition_text(self, prop):
        prop_parts = prop.split(' ')
        if prop_parts[0] == 'increasing_x':
            return "The column "+ prop_parts[1] + " is on the right of " + prop_parts[2]
        elif prop_parts[0] == 'increasing_y':
            return "The row "+ prop_parts[1] + " is above " + prop_parts[2]
        elif prop_parts[0] == 'player_at':
            return "The player is at the cell ("+prop_parts[1]+","+prop_parts[2]+")"
        elif prop_parts[0] == 'box_at':
            return "The box "+prop_parts[1]+" is at the cell ("+prop_parts[2]+","+prop_parts[3]+")"
        elif prop_parts[0] == 'switch_at':
            return "Switch is at the cell ("+prop_parts[1]+","+prop_parts[2]+")"
        elif prop_parts[0] == 'switch_activated':
            return "Switch is on"
        elif prop_parts[0] == 'free_cell':
            return "The cell ("+prop_parts[1]+","+prop_parts[2]+") is free to move to"


    def get_action_name_text(self, act_name, grounded=False, act_defn = {}):
        if grounded == True:
            act_parts = act_name.split(' ')
            act_name = act_parts[0]
            act_defn = {PARAMETERS: act_parts[1:]}
        if act_name == "move_right":
            #(:action move_right
		    #:parameters (?x1 - cell_x ?y1 - cell_y ?x2 - cell_x )
            act_name_string = f"Move right from cell ({act_defn[PARAMETERS][0].replace('?',VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][1].replace('?',VAR_SYMBOL)}) to ({act_defn[PARAMETERS][2].replace('?',VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][1].replace('?',VAR_SYMBOL)})"
        elif act_name == "move_left":
            # (:action move_left
            #:parameters (?x1 - cell_x ?y1 - cell_y ?x2 - cell_x )
            act_name_string = f"Move left from cell ({act_defn[PARAMETERS][0].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][1].replace('?', VAR_SYMBOL)}) to ({act_defn[PARAMETERS][2].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][1].replace('?', VAR_SYMBOL)})"

        elif act_name == "move_up":
            # (:action move_up
            # 		:parameters (?x1 - cell_x ?y1 - cell_y ?y2 - cell_y )
            act_name_string = f"Move up from cell ({act_defn[PARAMETERS][0].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][1].replace('?', VAR_SYMBOL)}) to ({act_defn[PARAMETERS][0].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][2].replace('?', VAR_SYMBOL)})"

        elif act_name == "move_down":
            # (:action move_up
            # 		:parameters (?x1 - cell_x ?y1 - cell_y ?y2 - cell_y )
            act_name_string = f"Move down from cell ({act_defn[PARAMETERS][0].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][1].replace('?', VAR_SYMBOL)}) to ({act_defn[PARAMETERS][0].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][2].replace('?', VAR_SYMBOL)})"

        elif act_name == "push_box_right":
            # 	(:action push_box_right
            # 		:parameters (?b - box ?x1 - cell_x ?y1 - cell_y ?x2 - cell_x ?x3 - cell_x)
            act_name_string = f"Push box {act_defn[PARAMETERS][0].replace('?', VAR_SYMBOL)} right from cell ({act_defn[PARAMETERS][3].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][2].replace('?', VAR_SYMBOL)}) to ({act_defn[PARAMETERS][4].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][2].replace('?', VAR_SYMBOL)})"

        elif act_name == "push_box_left":
            # 	(:action push_box_right
            # 		:parameters (?b - box ?x1 - cell_x ?y1 - cell_y ?x2 - cell_x ?x3 - cell_x)
            act_name_string = f"Push box {act_defn[PARAMETERS][0].replace('?', VAR_SYMBOL)} left from cell ({act_defn[PARAMETERS][2].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][1].replace('?', VAR_SYMBOL)}) to ({act_defn[PARAMETERS][3].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][1].replace('?', VAR_SYMBOL)})"

        elif act_name == "push_box_up":
            # 	(:action push_box_up
            # 		:parameters (?b - box ?x1 - cell_x ?y1 - cell_y ?y2 - cell_y ?y3 - cell_y)
            act_name_string = f"Push box {act_defn[PARAMETERS][0].replace('?', VAR_SYMBOL)} up from cell ({act_defn[PARAMETERS][1].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][3].replace('?', VAR_SYMBOL)}) to ({act_defn[PARAMETERS][1].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][4].replace('?', VAR_SYMBOL)})"

        elif act_name == "push_box_down":
            # 	(:action push_box_up
            # 		:parameters (?b - box ?x1 - cell_x ?y1 - cell_y ?y2 - cell_y ?y3 - cell_y)
            act_name_string = f"Push box {act_defn[PARAMETERS][0].replace('?', VAR_SYMBOL)} down from cell ({act_defn[PARAMETERS][1].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][3].replace('?', VAR_SYMBOL)}) to ({act_defn[PARAMETERS][1].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][4].replace('?', VAR_SYMBOL)})"

        elif act_name == "activate_switch":
            # 		(:action activate_switch
            # 		:parameters (?x1 - cell_x ?y1 - cell_y)
            act_name_string = f"Activate switch at cell ({act_defn[PARAMETERS][0].replace('?', VAR_SYMBOL)}," \
                              f"{act_defn[PARAMETERS][1].replace('?', VAR_SYMBOL)})"

        else:
            raise Exception("Unexpected action name")

        return act_name_string


    def get_action_definition_string(self, act_name, act_defn):
        act_string = "Action Definition: <br> Name: "+self.get_action_name_text(act_name,act_defn=act_defn)#+"<br>"
        if len(act_defn[POS_PREC]) > 0:
            act_string += "<br>Action requires the following facts to be true:"+"<br>"+ \
                          '<br>'.join(["&nbsp;&nbsp;&nbsp;&nbsp;" +self.get_proposition_text(prop.replace('?',VAR_SYMBOL)) for prop in sorted(list(act_defn[POS_PREC]))]) #+"<br>"
        if len(act_defn[ADDS]) > 0:
            act_string += "<br>Action causes the following facts to be true:" + "<br>" + \
                      '<br>'.join(["&nbsp;&nbsp;&nbsp;&nbsp;" +self.get_proposition_text(prop.replace('?',VAR_SYMBOL)) for prop in sorted(list(act_defn[ADDS]))]) #+ "<br>"
        if len(act_defn[DELS]) > 0:
            act_string += "<br>Action causes the following facts to be False:" + "<br>" + \
                          '<br>'.join(["&nbsp;&nbsp;&nbsp;&nbsp;" +self.get_proposition_text(prop.replace('?',VAR_SYMBOL)) for prop in sorted(list(act_defn[DELS]))]) #+ "<br>"
        return act_string

    def get_domain_text(self, model):
        domain_string = "<br><br>".join(self.get_action_definition_string(act, model[DOMAIN][act]) for act in model[DOMAIN])
        return domain_string

    def get_state_str(self, state, failure_pred):
        print (state)
        if failure_pred is None:
            return "<h4>Current state contains:</h4> "+"<br>"+"<br>".join([self.get_proposition_text(prop) for prop in sorted(list(state))])
        else:
            return "<h4>Current state contains:</h4> " + "<br>" + "<br>".join(
                [self.get_proposition_text(prop) for prop in sorted(list(state)) if self.parser.fluent_to_be_kept(prop, failure_pred)])

    def progress_player_pos_and_box_pos(self, act, player_pos, box_pos):
        if act == 0:
            return (player_pos, box_pos)
        elif act == 1:
            return ((player_pos[0],player_pos[1] - 1),(box_pos[0], box_pos[1]-1))

        elif act == 2:
            return ((player_pos[0],player_pos[1] + 1),(box_pos[0], box_pos[1]+1))

        elif act == 3:
            return ((player_pos[0]-1,player_pos[1]),(box_pos[0]-1, box_pos[1]))

        elif act == 4:
            return ((player_pos[0]+1,player_pos[1]),(box_pos[0]+1, box_pos[1]))

        elif act == 5:
            return ((player_pos[0],player_pos[1]-1),(box_pos[0], box_pos[1]))

        elif act == 6:
            return ((player_pos[0],player_pos[1]+1),(box_pos[0], box_pos[1]))
        elif act == 7:
            return ((player_pos[0] - 1,player_pos[1]),(box_pos[0], box_pos[1]))

        elif act == 8:
            return ((player_pos[0] + 1,player_pos[1]),(box_pos[0], box_pos[1]))



    def convert_atomic_act_to_grounded_act(self, act, player_pos, box_pos):
        # TODO: Need a way to skip impossible actions, but for now the walls take care of it
        # Push Up	1
        # Push Down	2
        # Push Left	3
        # Push Right	4
        # Move Up	5
        # Move Down	6
        # Move Left	7
        # Move Right	8
        if act ==0:
            return "activate_switch x" + str(player_pos[0]) + " y" + str(player_pos[1])

        elif act == 1:
            #		:parameters (?b - box ?C1 - cell_x ?R1 - cell_y ?R2 - cell_y ?R3 - cell_y)
            return "push_box_up b1 x"+str(player_pos[0]) +" y"+str(player_pos[1]) \
                   +" y"+str(player_pos[1]-1) + " y"+str(player_pos[1] - 2)

        elif act == 2:
            return "push_box_down b1 x"+str(player_pos[0]) +" y"+str(player_pos[1]) \
                   +" y"+str(player_pos[1]+1) + " y"+str(player_pos[1] + 2)

        elif act == 3:
            return "push_box_left b1 x"+str(player_pos[0]) +" y"+str(player_pos[1]) \
                   +" x"+str(player_pos[0]-1) +" x"+str(player_pos[0] - 2)

        elif act == 4:
            return "push_box_right b1 x"+str(player_pos[0]) +" y"+str(player_pos[1]) \
                   +" x"+str(player_pos[0]+1) +" x"+str(player_pos[0] + 2)

        elif act == 5:
            return "move_up x"+str(player_pos[0]) +" y"+str(player_pos[1]) +" y"+str(player_pos[1] - 1)

        elif act == 6:
            return "move_down x"+str(player_pos[0]) +" y"+str(player_pos[1]) +" y"+str(player_pos[1] + 1)

        elif act == 7:
            return "move_left x"+str(player_pos[0]) +" y"+str(player_pos[1]) +" x"+str(player_pos[0] - 1)

        elif act == 8:
            return "move_left x"+str(player_pos[0]) +" y"+str(player_pos[1]) +" x"+str(player_pos[0] + 1)


    def find_explanation_text(self, plan=[1], abstract=False, prev_failure_preds = set()):
        # Execute actions till failure
        curr_state = self.model[INSTANCE][INIT].copy()
        player_pos = self.init_player_pos
        box_pos = self.box_pos
        for act in plan[:-1]:
            act_name = self.convert_atomic_act_to_grounded_act(act, player_pos,box_pos)
            curr_state = self.find_next_state(curr_state, act_name)
            player_pos, box_pos = self.progress_player_pos_and_box_pos(act, player_pos, box_pos)
        failure_act = self.convert_atomic_act_to_grounded_act(plan[-1], player_pos, box_pos)
        failure_prec = self.find_failure(curr_state, failure_act)
        print ("Failed prec", failure_prec)
        if abstract:
            filter_pred = prev_failure_preds| set([failure_prec])
            filtered_model = self.parser.get_abstract_model(self.model, filter_pred)
        else:
            filter_pred = None
            filtered_model = self.model
        print ("Filter preds", filter_pred)
        state_string = self.get_state_str(curr_state, filter_pred)
        failed_action = self.get_action_name_text(failure_act, grounded=True)
        grounded_act = self.parser.get_grounded_action_definition(failure_act, filtered_model)
        preconditions = "The action requires: "+"<br>".join([self.get_proposition_text(prop) for prop in grounded_act[POS_PREC] if self.parser.fluent_to_be_kept(prop, filter_pred)])
        unmet_precondition = "But couldn't meet the requirement: "+ self.get_proposition_text(failure_prec)

        domain_string = self.get_domain_text(filtered_model)

        return (state_string+"<br><br><h4> Failed Action </h4>"+failed_action+"<br>"+preconditions+"<br>"+unmet_precondition,domain_string, filter_pred)


if __name__ == "__main__":
    import sys

    # Current state
    # action
    # missing precondition

    domain_file = sys.argv[1]
    problem_file = sys.argv[2]
    exp = Explainer(domain_file, problem_file, (1,1), (2,2))
    print (exp.find_explanation_text([1]))