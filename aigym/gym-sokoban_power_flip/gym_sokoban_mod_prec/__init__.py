import logging
import pkg_resources
import json
from gym.envs.registration import register #I think there's some problem with this becuase minigrid uses gynasium not gym
#from gymnasium.envs.registration import register


from .envs.custom_grid_env import CustomGridEnv 
#End Kelsey added


logger = logging.getLogger(__name__)

resource_package = __name__
env_json = pkg_resources.resource_filename(resource_package, '/'.join(('envs', 'available_envs.json')))

with open(env_json) as f:

    envs = json.load(f)

    for env in envs:
        register(
            id=env["id"],
            entry_point=env["entry_point"]
        )


