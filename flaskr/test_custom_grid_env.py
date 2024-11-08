import gym
from gym_sokoban_mod_prec.envs import custom_grid_env

# Ensure this path matches your environment registration
env_name = 'CustomGridEnv-v0'  # Use the registered environment ID

try:
    # Create an instance of the environment
    env = gym.make(env_name)

    # Reset the environment to get the initial observation
    obs = env.reset()
    print("Initial observation:", obs)

    done = False
    while not done:
        # Sample a random action from the action space
        action = env.action_space.sample()  # Replace with a valid action if necessary
        obs, reward, done, info = env.step(action)

        # Print the results of the step
        print(f"Action: {action}, Observation: {obs}, Reward: {reward}, Done: {done}, Info: {info}")

    # Close the environment
    env.close()

except Exception as e:
    print("An error occurred:", e)
