import gym
import sys
import time

import gym_sokoban_mod_gravity
import numpy as np
from PIL import Image
import io
import base64





env_name = 'Sokoban-gravity-mod-v0'
env = gym.make(env_name)
ACTION_LOOKUP = env.unwrapped.get_action_lookup()

human_agent_action = 0
restart_game = False

key_to_action_map = {
    ord('w'): 1,
    ord('s'): 2,
    ord('a'): 3,
    ord('d'): 4,
    65362: 5,
    65364: 6,
    65361: 7,
    65363: 8
}

def key_press(key, mod):
    global human_agent_action, restart_game
    if key == ord('r'):
        restart_game = True
        return
    human_agent_action = key_to_action_map[key]


def key_release(key, mod):
    global human_agent_action, restart_game
    human_agent_action = 0
    # print(key)

env.render()
env.unwrapped.viewer.window.on_key_press = key_press
env.unwrapped.viewer.window.on_key_release = key_release

observation = env.reset()
count = 1
while 1:
    rgb_img = env.render("rgb_array")
    img = Image.fromarray(rgb_img, mode="RGB")
    img.save('./temp/%d.png' % count, format='PNG')
    count += 1
    env.render(mode='human')
    action = human_agent_action
    time.sleep(0.08)
    observation, reward, done, info = env.step(action)
    print(action, reward, done, info)

    if restart_game:
        env.reset()
        restart_game = False

    if done:
        rgb_img = env.render("rgb_array")
        img = Image.fromarray(rgb_img, mode="RGB")
        img.save('./temp/%d.png' % count, format='PNG')
        env.render()
        break

env.close()