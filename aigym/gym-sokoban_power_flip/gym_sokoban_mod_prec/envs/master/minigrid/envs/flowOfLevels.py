from __future__ import annotations

from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Door, Goal, Key, Wall
from minigrid.manual_control import ManualControl
from minigrid.minigrid_env import MiniGridEnv
from minigrid.core.world_object import Lava

class EmptyGridEnv(MiniGridEnv):
    """
    An empty MiniGrid environment with only the agent and walls around the grid.
    """
    def __init__(
        self,
        size=8,
        agent_start_pos=(1, 1),
        agent_start_dir=0,
        goal_pos=None,
        max_steps: int | None = None,
        **kwargs,
        ):
        self.goal_pos = goal_pos # position of the goal 
        self.lava_positions = []    # positions of the lava
        self.door_pos = None  # Position for the door (will be used in level 3)
        self.key_pos = None    #position for key
        self.current_level = 1
        mission_space = MissionSpace(mission_func=lambda: "Explore the environment. No specific goals.")
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 4 * size**2
        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            # Set this to True for maximum speed
            see_through_walls=True,
            max_steps=max_steps,
            **kwargs,
        )
    @staticmethod
    def _gen_mission():
        return "grand mission"
    
    
    def _gen_grid(self, width, height):
        # Create an empty grid with walls around the edges
        self.grid = Grid(width, height)
        self.grid.wall_rect(0, 0, width, height)

        # Initialize the agent's position and direction
        self.agent_pos = (1, 1)
        self.agent_dir = 0
        self.mission = "grand mission"
        if self.goal_pos:
            self.put_obj(Goal(), *self.goal_pos)
        # Add lava for level 2
        if self.current_level > 1:
            for pos in self.lava_positions:
                self.put_obj(Lava(), *pos)
        if self.current_level == 3:
            if self.door_pos:
                self.put_obj(Door('yellow', is_locked=True), *self.door_pos)
            if self.key_pos:
                self.put_obj(Key('yellow'), *self.key_pos)
    
    
    
    def step(self, action):
        obs, reward, done, truncated, info = super().step(action)  # Adjusted to capture 'truncated'
        print('current level ', self.current_level)
        # Your existing logic for checking completion and moving to the next level
        if done and reward > 0:  # Assuming reaching the goal gives positive reward
            # Progress to level 2
            self.current_level += 1
            self.reset()  # Reset the environment for the next level
            # Optionally, reposition the agent or make other adjustments for level 2
        # elif self.current_level == 2 and done and reward > 0:
        #     self.current_level += 1
        #     # Setup door and key for Level 3
        #     #self.add_door_and_key(door_pos=(5, 5), key_pos=(2, 2))  # Example positions
        #     self.reset()
        return obs, reward, done, truncated, info
    def reset(self, **kwargs):
        # Before resetting, configure level 2 if needed
        if self.current_level == 2:
            # Define lava positions for level 2
            self.add_lava(2, 2)
            self.add_lava(2, 3)
            self.add_lava(2, 4)
        if self.current_level == 3:
           print('level 3')
           self.add_door_and_key(door_pos=(5, 5), key_pos=(2, 2))  # Example positions
        
        return super().reset(**kwargs)

    def add_goal(self, x, y):
        """
        Adds a goal object to the grid at the specified position.

        :param x: X coordinate of the goal position
        :param y: Y coordinate of the goal position
        """     
        if not (0 < x < self.grid.width - 1 and 0 < y < self.grid.height - 1):
            raise ValueError("Goal position is out of bounds or too close to the walls.")
        self.put_obj(Goal(), x, y)
    def add_lava(self, x, y):
        """
        Adds a lava tile to the grid at the specified position.
        This method stores the lava position in a list; lava tiles are placed when the grid is generated.
        
        :param x: X coordinate of the lava position
        :param y: Y coordinate of the lava position
        """
        if not (0 < x < self.grid.width - 1 and 0 < y < self.grid.height - 1):
            raise ValueError("Lava position is out of bounds or too close to the walls.")
        self.lava_positions.append((x, y))
    def add_door_and_key(self, door_pos, key_pos):
        """
        Adds a door and a key to the environment for Level 3.
        :param door_pos: Tuple specifying the door's position
        :param key_pos: Tuple specifying the key's position
        """
        if not (0 < door_pos[0] < self.width - 1 and 0 < door_pos[1] < self.height - 1):
            raise ValueError("Door position is out of bounds or too close to the walls.")
        if not (0 < key_pos[0] < self.width - 1 and 0 < key_pos[1] < self.height - 1):
            raise ValueError("Key position is out of bounds or too close to the walls.")
        self.door_pos = door_pos
        self.key_pos = key_pos

def main():
    env = EmptyGridEnv(size=8,render_mode="human",goal_pos=(6, 6))
   
    manual_control = ManualControl(env, seed = 42)
    manual_control.start()

if __name__ == "__main__":
    main()
