from flaskr.scripts.model_parser import Parser
import sys
# Current state
# action
# missing precondition

domain_file = sys.argv[1]
problem_file = sys.argv[2]
#state_file = sys.argv[3]
#action = sys.argv[4]

parser_obj = Parser()

model_map = parser_obj.parse_model(domain_file, problem_file)

print (parser_obj.get_grounded_action_definition('move_left x2 y2 x1',model_map))