from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.minigrid_env import MiniGridEnv
from minigrid.core.world_object import Lava, Door, Key, Goal,Ball, Box,CustomBox
from minigrid.manual_control import ManualControl
import random


class CustomGridEnv(MiniGridEnv):
    def __init__(self, size=8, agent_start_pos=(1, 1), agent_start_dir=0, **kwargs):
        # It's important to initialize these before calling super().__init__
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir
        self.grid_size = size
        mission_space = MissionSpace(mission_func=self._gen_mission)
        self.lava_positions = []
        super().__init__(grid_size=size, mission_space=mission_space ,**kwargs)
        
        self.level_configuration = []
        self.max_steps = 4 * size ** 2
        self.door_pos = None  # Position for the door (will be used in level 3)
        self.key_pos = None  # Postion for key. also level 3

        # Set agent's initial position and direction
        self.reset_agent_start_pos()

        
    @staticmethod
    def _gen_mission():
        return "grand mission" # prolly have to change this based on level

    def reset_agent_start_pos(self):
        #Ensure the initial position is valid
        if not (0 <= self.agent_start_pos[0] < self.grid_size and 0 <= self.agent_start_pos[1] < self.grid_size):
            raise ValueError("Agent's starting position is out of grid bounds.")
        #Ensure the direction is valid
        if not (0 <= self.agent_start_dir < 4):
            raise ValueError("Agent's starting direction is invalid.")
        self.agent_pos = self.agent_start_pos
        self.agent_dir = self.agent_start_dir

    def configure_level(self, level_config): # This is called in main to set the onfig levels. can prolly use this at the end of each level
        self.level_configuration = level_config
        # Reset agent position and direction to start values before resetting the level
        self.reset_agent_start_pos()
        self.reset()

    def _gen_grid(self, width, height): # main function that generates the grid
        # Create an empty grid with walls around the edges
        self.agent_pos = self.agent_start_pos
        self.agent_dir = self.agent_start_dir
        self.grid = Grid(width, height)
        self.grid.wall_rect(0, 0, width, height) # we could take it out. Pure aesthetics 

        # Process the level configuration
        for component in self.level_configuration:
            if component == 0:
                #self.add_random_lava()
                self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2) #Kelsey added so green square was always a part of each level

            # if component == 1:
            #     self.add_random_lava()
            elif component == 1:
                self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2) #Kelsey added
                self.add_random_lava()
            
            elif component == 2:
                self.add_door_and_key_randomly()
            elif component == 3:
                self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2) #Kelsey Added
                n_obstacles = 4  # or some other logic to determine the number
                self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2) #Kelsey added
                self.add_dynamic_obstacles(n_obstacles)
            elif component == 4:
                self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2) #Kelsey added
                self.add_pickup_and_place_object()

            # Additional conditions for more components can be added here

    def add_random_lava(self):
        """Add four lava tiles in random locations within the grid."""
        """Add four lava tiles in random locations within the grid, avoiding the agent's position."""
        possible_positions = [
            (x, y) 
            for x in range(1, self.grid.width - 1) 
            for y in range(1, self.grid.height - 1)
            if (x, y) != self.agent_pos
        ]
       #print(possible_positions)
        critical_path_positions = self.get_critical_path_positions() # Please update this as new levels are added. Cant make the level unsolvable

       #Filter out critical path positions from possible lava positions
        possible_positions = [
            pos for pos in possible_positions if pos not in critical_path_positions
        ]
        
        random.shuffle(possible_positions) # Randomly shuffle the list of possible positions

        
        for i in range(min(4, len(possible_positions))): # Attempt to add up to four lava tiles, stopping if there aren't enough positions
            lava_pos = possible_positions[i]
            
            self.put_obj(Lava(), *lava_pos)
            self.lava_positions.append(lava_pos)

    def add_door_and_key_randomly(self):
       # Create an empty grid with walls around the edges
            # Place a goal in the bottom-right corner if it's not already set by previous configurations
        if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
            self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)

        # Create a vertical splitting wall, avoiding overriding existing objects like lava
        split_idx = random.randint(3, self.grid_size - 4)
        for y in range(1, self.grid_size - 1):
            if not self.grid.get(split_idx, y):
                self.grid.vert_wall(split_idx, 0, length=self.grid_size - 1)

        # Randomly place a door in the vertical wall
        door_idx = random.randint(1, self.grid_size - 3)
        self.put_obj(Door("yellow", is_locked=True), split_idx, door_idx)

        # Randomly place a yellow key on the left side of the wall
        # Make sure it doesn't overlap with lava or the agent's position
        key_placed = False
        while not key_placed:
            key_pos = (random.randint(1, split_idx - 1), random.randint(1, self.grid_size - 2))
            if key_pos != self.agent_pos and not isinstance(self.grid.get(*key_pos), Lava):
                self.put_obj(Key("yellow"), *key_pos)
                key_placed = True
        self.key_pos = key_pos
        self.door_pos = (split_idx, door_idx)
        print( self.key_pos,  self.door_pos)
    def add_dynamic_obstacles(self, n_obstacles):
        """Add dynamic obstacles to the grid."""
        self.obstacles = []
        for i_obst in range(min(n_obstacles, self.grid_size - 2)):
            obstacle = Ball()
            self.obstacles.append(obstacle)
            self.place_obj(obstacle, max_tries=100)

    def get_critical_path_positions(self):
        """Calculate positions on the critical path between agent, key, door, and goal."""
        critical_positions = []

        # Add horizontal path from agent to door assumptions is that door is always to the right of agent
        agent_x, agent_y = self.agent_start_pos
        if(self.door_pos is not None):
            door_x, door_y = self.door_pos  # Assuming self.door_pos has been set in add_door_and_key_randomly
            critical_positions.extend([(x, agent_y) for x in range(agent_x, door_x + 1)])

        # Add vertical path from door to goal (assumes goal is always below door)
        goal_x, goal_y = self.grid_size - 2, self.grid_size - 2
        if(self.door_pos is not None):
            critical_positions.extend([(door_x, y) for y in range(door_y, goal_y + 1)])


        if(self.key_pos is not None):
        # Add positions around the key to ensure it is reachable
            key_x, key_y = self.key_pos  # Assuming self.key_pos has been set in add_door_and_key_randomly
            critical_positions.extend([
                (key_x + dx, key_y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                if 0 <= key_x + dx < self.grid_size and 0 <= key_y + dy < self.grid_size
            ])
        return critical_positions
    def add_pickup_and_place_object(self):
        if 2 in self.level_configuration:
            # If level 2 is in the configuration, place a ball next to the door.
            door_x, door_y = self.door_pos
            # Check the side of the door and place the ball accordingly.
            if door_x > 1:
                ball_pos = (door_x - 1, door_y)
            else:
                ball_pos = (door_x + 1, door_y)
            self.put_obj(CustomBox('red'), *ball_pos)
        else:
            # If level 2 is not in the configuration, create a wall with a gap and place the ball there.
            wall_x = self.grid_size // 2
            gap_y = self.grid_size // 2
            self.grid.vert_wall(wall_x, 0, length=gap_y-1)
            self.grid.vert_wall(wall_x, gap_y+1, length=self.grid_size-gap_y-1)
            
            # Place the ball in the gap.
            ball_pos = (wall_x, gap_y)
            self.put_obj(Ball(), *ball_pos)

            
    def step(self, action):
    # Update the agent's position/direction
        obs, reward, done, truncated, info = super().step(action)  # Removed 'truncated' as it's not a standard Gym return

        # Check if there is an obstacle in front of the agent
        front_cell = self.grid.get(*self.front_pos)
        
        if front_cell and front_cell.type == 'ball':
            reward = -1  # Collided with a dynamic obstacle
            done = True

        # Update dynamic obstacle positions after the agent moves
        if not done and 3 in self.level_configuration :  # Only update obstacles if the game is not done
            self.update_dynamic_obstacles()

        return obs, reward, done, truncated, info

    def update_dynamic_obstacles(self):
        # Move each obstacle to a new random position
        for obstacle in self.obstacles:
            old_pos = obstacle.cur_pos
            # Randomly choose a new direction for the obstacle to move
            dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
            new_pos = (old_pos[0] + dx, old_pos[1] + dy)

            # Check if the new position is within the grid and not occupied
            if self.position_is_inside(new_pos) and not self.grid.get(*new_pos):
                # Move the obstacle to the new position
                self.grid.set(*old_pos, None)  # Remove obstacle from old position
                self.grid.set(*new_pos, obstacle)  # Place obstacle at new position
                obstacle.cur_pos = new_pos
    def position_is_inside(self, pos):
        x, y = pos
        return 0 <= x < self.grid.width and 0 <= y < self.grid.height
       
def main():
    # initializing the environment and configuring a level
    # env = CustomGridEnv(size=8)
    # env.configure_level([1, 2])  # This combines lava and door/key elements in the same level

    # # Example on how to use it with manual control or integrate into a game loop
   
    # print(env.grid)  
    env = CustomGridEnv(size=12,render_mode="human")
    #env.configure_level([1,2,3,4]) #213 works
    env.configure_level([0,1,2,3,4]) 
    manual_control = ManualControl(env, seed = 42)
    manual_control.start()
if __name__ == "__main__":
    main()
