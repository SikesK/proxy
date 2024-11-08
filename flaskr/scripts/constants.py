import os

# Src location
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

# Keywords for internal dictionary based
# representation of classical planning models
# Expected domain dictionary format
# domain:
#   action_name:
#       params: list
#       pos_prec: set()
#       neg_prec: set()
#       adds: set()
#       dels: set()
#       conditional_adds: list()
#       conditional_dels: list()
# instance:
#   init: set()
#   goal: set()
DOMAIN = "domain"
PARAMETERS = "params"
POS_PREC = "pos_prec"
NEG_PREC = "neg_prec"
ADDS = "adds"
COND_ADDS = "conditional_adds"
COND_DELS = "conditional_adds"
DELS = "dels"
INSTANCE = "instance"
INIT = "init"
GOAL = "goal"

# A hack to get arround multiple goals
GOAL_ACHIEVED = "goal_achieved"
GOAL_ACT = "goal-act"


# CONJUNCT FLUENT
CONJ_PREFIX = "CONJ_"
CONJ_SEPARATOR = '&'
COND_ACT_NAME_SEPARTOR = "#"

MERGE_SEPARATOR = '+'


MAX_RELAXED_PLAN_COST = float('inf')
HEURISTIC_UPPER_BOUND = 10000
RELAXED_ACTION_COST = 1



STAGERRED_PRUNING = True

FLUENT_COST = 1 #000
CONJ_COST = 1


# DEBUG Stuff
DEBUG_LEVEL = 1