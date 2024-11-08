from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.minigrid_env import MiniGridEnv
#from minigrid.minigrid_env import Grid #Kelsey added
from minigrid.core.world_object import Lava, Door, Key, Goal, Ball, Box, CustomBox, Wall, BigX
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

        #Kelsey Added
        self.obstacles = [] 
        self.obstacles_positions = []

        
        self.level_configuration = []
        self.max_steps = 4 * size ** 2
        self.door_pos = None  # Position for the door (will be used in level 3)
        self.second_door_pos = None  # Kelsey Added
        self.key_pos = None  # Postion for key. also level 3

        # Set agent's initial position and direction
        self.reset_agent_start_pos()

        
    @staticmethod
    def _gen_mission():
        return "grand mission" # prolly have to change this based on level


    def reset_agent_start_pos(self):
        # Ensure the initial position is valid
        if not (0 <= self.agent_start_pos[0] < self.grid_size and 0 <= self.agent_start_pos[1] < self.grid_size):
            raise ValueError("Agent's starting position is out of grid bounds.")
        # Ensure the direction is valid
        if not (0 <= self.agent_start_dir < 4):
            raise ValueError("Agent's starting direction is invalid.")
        self.agent_pos = self.agent_start_pos
        self.agent_dir = self.agent_start_dir

    def configure_level(self, level_config): # This is called in main to set the config levels. can prolly use this at the end of each level
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
            
            if component == 1:
                self.add_agent_empty_grid()
            
            elif component == 2:
                self.add_random_lava()

            elif component == 3:
                self.add_open_door()
            
            elif component == 4:
                self.add_door_and_key_randomly()

            elif component == 5:
                n_obstacles = 4  # or some other logic to determine the number
                self.add_dynamic_obstacles(n_obstacles)

            elif component == 6:
                self.add_pickup_and_place_object()
            # elif component == 6:
            #     #self.add_memory_level()
            #     #self.add_room_with_hallway()
            #     self.add_open_door()


            # Additional conditions for more components can be added here

    def add_agent_empty_grid(self):
        if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
            self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)

    
    def add_random_lava(self):
        if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
            self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)
        goal_position = (self.grid_size - 2, self.grid_size - 2)
        """Add four lava tiles in random locations within the grid."""
        """Add four lava tiles in random locations within the grid, avoiding the agent's position."""
        possible_positions = [
            (x, y) 
            for x in range(1, self.grid.width - 1) 
            for y in range(1, self.grid.height - 1)
            if (x, y) != self.agent_pos and (x, y) != goal_position
        ]
       #print(possible_positions)
        critical_path_positions = self.get_critical_path_positions() # Please update this as new levels are added. Cant make the level unsolvable

       #Filter out critical path positions from possible lava positions -- need to add balls to this?
        possible_positions = [
            pos for pos in possible_positions if pos not in critical_path_positions
        ]
        # Randomly shuffle the list of possible positions
        random.shuffle(possible_positions)

        # Attempt to add up to four lava tiles, stopping if there aren't enough positions
        for i in range(min(4, len(possible_positions))):
            lava_pos = possible_positions[i]
            
            self.put_obj(Lava(), *lava_pos)
            self.lava_positions.append(lava_pos)

    # def add_open_door(self):
    #    # Create an empty grid with walls around the edges
    #         # Place a goal in the bottom-right corner if it's not already set by previous configurations
    #     if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
    #         self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)

    #     # Create a vertical splitting wall, avoiding overriding existing objects like lava
    #     split_idx = random.randint(2, self.grid_size - 4)
    #     for y in range(1, self.grid_size - 1):
    #         if not self.grid.get(split_idx, y):
    #             self.grid.vert_wall(split_idx, 0, length=self.grid_size - 1)

    #     # Randomly place a door in the vertical wall
    #     door_idx = random.randint(1, self.grid_size - 3)
    #     self.put_obj(Door("purple", is_locked=False), split_idx, door_idx)

    #     self.door_pos = (split_idx, door_idx)
    #     print( self.door_pos)

    #CURRENT
    # def add_open_door(self):
    #     if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
    #         self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)

    #     # Create a vertical splitting wall
    #     split_idx = random.randint(2, self.grid_size - 3) #changed 4 to 3
    #     for y in range(1, self.grid_size - 1):
    #         if not self.grid.get(split_idx, y):
    #             self.grid.vert_wall(split_idx, 1, length=self.grid_size - 1) #changed zero to first 1 here

    #     # Attempt to place an open door at a random location on the wall
    #     door_placed = False
    #     possible_door_positions = list(range(1, self.grid_size - 3))
    #     random.shuffle(possible_door_positions)
        
    #     for door_idx in possible_door_positions:
    #         # Check for lava in front and behind the door position
    #         front_pos = (split_idx + 1, door_idx)
    #         back_pos = (split_idx - 1, door_idx)

    #         if not isinstance(self.grid.get(*front_pos), Lava) and not isinstance(self.grid.get(*back_pos), Lava):
    #             self.put_obj(Door("purple", is_locked=False), split_idx, door_idx)
    #             self.door_pos = (split_idx, door_idx)
    #             door_placed = True
    #             break

    #TEST
    # def add_open_door(self):
    #    # Create an empty grid with walls around the edges
    #         # Place a goal in the bottom-right corner if it's not already set by previous configurations
    #     if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
    #         self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)

    #     # Create a vertical splitting wall, avoiding overriding existing objects like lava
    #     split_idx = random.randint(3, self.grid_size - 4)
    #     for y in range(1, self.grid_size - 1):
    #         if not self.grid.get(split_idx, y):
    #             self.grid.vert_wall(split_idx, 0, length=self.grid_size - 1)

    #     # Randomly place a door in the vertical wall
    #     door_idx = random.randint(1, self.grid_size - 3)
    #     self.put_obj(Door("purple", is_locked=False), split_idx, door_idx)
    #     self.door_pos = (split_idx, door_idx)
    #     print(self.door_pos)



    #KEEP
    def add_open_door(self):
        if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
            self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)

        # More conservative positioning of the first door to leave space for the key and second door
        # Limiting the door position to ensure at least 4 spaces to the right (3 for key and second door, 1 as buffer)
        max_door_idx = self.grid_size - 5

        # Create a vertical splitting wall at a random but limited position
        split_idx = random.randint(2, max_door_idx)
        for y in range(1, self.grid_size - 1):
            if not self.grid.get(split_idx, y):
                self.grid.vert_wall(split_idx, 1, length=self.grid_size - 1)

        # Attempt to place an open door at a random location on the wall
        door_placed = False
        possible_door_positions = list(range(1, self.grid_size - 3))
        random.shuffle(possible_door_positions)
        
        for door_idx in possible_door_positions:
            # Check for lava in front and behind the door position
            front_pos = (split_idx + 1, door_idx)
            back_pos = (split_idx - 1, door_idx)

            if not isinstance(self.grid.get(*front_pos), Lava) and not isinstance(self.grid.get(*back_pos), Lava):
                self.put_obj(Door("purple", is_locked=False), split_idx, door_idx)
                self.door_pos = (split_idx, door_idx)
                door_placed = True
                break







    def add_door_and_key_randomly(self):
        if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
            self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)

        if 3 in self.level_configuration:
            if self.door_pos[0] + 2 < self.grid_size - 3:
                second_split_idx = random.randint(self.door_pos[0] + 2, self.grid_size - 3)

                # Place the key between the first and second doors
                key_x_range = range(self.door_pos[0] + 1, second_split_idx)
                key_y_range = range(1, self.grid_size - 1)
                key_positions = [(x, y) for x in key_x_range for y in key_y_range if not isinstance(self.grid.get(x, y), Lava) and not isinstance(self.grid.get(x, y), Wall)]
                if key_positions:
                    key_pos = random.choice(key_positions)
                    self.put_obj(Key("yellow"), *key_pos)
                    self.key_pos = key_pos

                for y in range(1, self.grid_size - 1):
                    if not self.grid.get(second_split_idx, y):
                        self.grid.vert_wall(second_split_idx, 0, length=self.grid_size - 1)
                second_door_idx = random.randint(1, self.grid_size - 3)
                self.put_obj(Door("yellow", is_locked=True), second_split_idx, second_door_idx)
                self.second_door_pos = (second_split_idx, second_door_idx)

        else:
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

   















    # def add_door_and_key_randomly(self):
    #     if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
    #         self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)

    #     # Define the maximum index for placing doors and keys
    #     max_idx = self.grid_size - 5

    #     if 3 not in self.level_configuration:
    #         # Place the first door if component 3 has not been added
    #         #first_split_idx = random.randint(2, max_idx)
    #         #first_door_idx = random.randint(1, self.grid_size - 3)
    #         #self.put_obj(Door("purple", is_locked=False), first_split_idx, first_door_idx)
    #         #self.door_pos = (first_split_idx, first_door_idx)
    #         # Place the key randomly avoiding the path of the first door
    #         possible_key_positions = [
    #             (x, y) for x in range(1, self.grid.width - 1) for y in range(1, self.grid.height - 1)
    #             if (x, y) != (first_split_idx, first_door_idx)
    #         ]
    #         random.shuffle(possible_key_positions)
    #         key_pos = possible_key_positions[0]
    #         self.put_obj(Key("yellow"), *key_pos)
    #         self.key_pos = key_pos
    #     else:
    #         # If the first door is already placed, work with its position
    #         first_door_x, first_door_y = self.door_pos
    #         second_door_x = random.randint(first_door_x + 2, self.grid_size - 3)
    #         second_door_y = random.randint(1, self.grid_size - 3)
    #         self.put_obj(Door("yellow", is_locked=True), second_door_x, second_door_y)
    #         self.second_door_pos = (second_door_x, second_door_y)
            
    #         # Place the key in the area between the two doors
    #         key_x = random.randint(first_door_x + 1, second_door_x - 1)
    #         key_y = random.randint(1, self.grid_size - 3)
    #         self.put_obj(Key("yellow"), key_x, key_y)
    #         self.key_pos = (key_x, key_y)

    #     print(f"Door Position: {self.door_pos}, Key Position: {self.key_pos}, Second Door Position: {self.second_door_pos}")





    #Almost works
    # def add_door_and_key_randomly(self):
    #     # Ensure the grid is prepared with a goal and borders
    #     if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
    #         self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)

    #     # Define the maximum index for the first door to leave space for the key and second door
    #     max_first_door_idx = self.grid_size - 5  # Ensuring at least two units for key and second door

    #     # Place the first door
    #     if not self.door_pos:
    #         first_split_idx = random.randint(2, max_first_door_idx)
    #         for y in range(1, self.grid_size - 1):
    #             if not self.grid.get(first_split_idx, y):
    #                 self.grid.vert_wall(first_split_idx, 0, length=self.grid_size - 1)
    #         first_door_idx = random.randint(1, self.grid_size - 3)
    #         self.put_obj(Door("purple", is_locked=False), first_split_idx, first_door_idx)
    #         self.door_pos = (first_split_idx, first_door_idx)

    #     # Check space availability for the second door and key
    #     if self.door_pos:
    #         if self.door_pos[0] + 2 < self.grid_size - 3:
    #             second_split_idx = random.randint(self.door_pos[0] + 2, self.grid_size - 3)

    #             # Place the key between the first and second doors
    #             key_x_range = range(self.door_pos[0] + 1, second_split_idx)
    #             key_y_range = range(1, self.grid_size - 1)
    #             key_positions = [(x, y) for x in key_x_range for y in key_y_range if not isinstance(self.grid.get(x, y), Lava) and not isinstance(self.grid.get(x, y), Wall)]
    #             if key_positions:
    #                 key_pos = random.choice(key_positions)
    #                 self.put_obj(Key("yellow"), *key_pos)
    #                 self.key_pos = key_pos
    #             else:
    #                 print("No valid positions for key found between the doors. Adjusting positions.")
    #                 # As a fallback, try to find any position to the right of the first door if the preferred range failed
    #                 broader_key_positions = [(x, y) for x in range(self.door_pos[0] + 1, self.grid_size - 1) for y in key_y_range if not isinstance(self.grid.get(x, y), Lava)]
    #                 if broader_key_positions:
    #                     key_pos = random.choice(broader_key_positions)
    #                     self.put_obj(Key("yellow"), *key_pos)
    #                     self.key_pos = key_pos
    #                 else:
    #                     print("Failed to place the key within the constraints.")

    #             # Place the second door
    #             for y in range(1, self.grid_size - 1):
    #                 if not self.grid.get(second_split_idx, y):
    #                     self.grid.vert_wall(second_split_idx, 0, length=self.grid_size - 1)
    #             second_door_idx = random.randint(1, self.grid_size - 3)
    #             self.put_obj(Door("yellow", is_locked=True), second_split_idx, second_door_idx)
    #             self.second_door_pos = (second_split_idx, second_door_idx)
    #         else:
    #             print("Not enough space to place the second door. Adjusting the first door placement.")
    #             # Optionally, you could reposition the first door to make space, or flag an error/logic issue.

    #         print(f"First Door Position: {self.door_pos}, Key Position: {self.key_pos}, Second Door Position: {self.second_door_pos}")






    # def add_dynamic_obstacles(self, n_obstacles):
    #     if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
    #         self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)
    #     """Add dynamic obstacles to the grid."""
    #     self.obstacles = []
    #     for i_obst in range(min(n_obstacles, self.grid_size - 2)):
    #         obstacle = Ball()
    #         self.obstacles.append(obstacle)
    #         self.place_obj(obstacle, max_tries=100)


    def add_dynamic_obstacles(self, n_obstacles):
        if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
            self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)
        goal_position = (self.grid_size - 2, self.grid_size - 2)
        """Add dynamic obstacles to the grid."""

        possible_positions = [
            (x, y) 
            for x in range(1, self.grid.width - 1) 
            for y in range(1, self.grid.height - 1)
            if (x, y) != self.agent_pos and (x, y) != goal_position
        ]

        self.obstacles = []

        critical_path_positions = self.get_critical_path_positions()
        possible_positions = [pos for pos in possible_positions if pos not in critical_path_positions]
        random.shuffle(possible_positions)

        for i_obst in range(min(n_obstacles, len(possible_positions))):
            ball_pos = possible_positions[i_obst]
            self.put_obj(Ball(), *ball_pos)
            self.obstacles_positions.append(ball_pos)



    


    def get_critical_path_positions(self):
        """Calculate positions on the critical path between agent, key, door, and goal."""
        critical_positions = []

        # Add horizontal path from agent to door (assumes door is always to the right of agent)
        agent_x, agent_y = self.agent_start_pos
        if(self.door_pos is not None):
            door_x, door_y = self.door_pos  # Assuming self.door_pos has been set in add_door_and_key_randomly
            critical_positions.extend([(x, agent_y) for x in range(agent_x, door_x + 1)])


        if(self.second_door_pos is not None):
            second_door_x, second_door_y = self.second_door_pos 
            critical_positions.extend([(x, door_y) for x in range(door_x, second_door_x + 1)])


        # Add vertical path from door to goal (assumes goal is always below door) --- this might need to cover more cases?
        goal_x, goal_y = self.grid_size - 2, self.grid_size - 2
        if(self.second_door_pos is not None):
            critical_positions.extend([(second_door_x, y) for y in range(second_door_y, goal_y + 1)])


        if(self.key_pos is not None):
        # Add positions around the key to ensure it is reachable
            key_x, key_y = self.key_pos  # Assuming self.key_pos has been set in add_door_and_key_randomly
            critical_positions.extend([
                (key_x + dx, key_y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                if 0 <= key_x + dx < self.grid_size and 0 <= key_y + dy < self.grid_size
            ])
        return critical_positions





    #ORIGINAL CP
    # def get_critical_path_positions(self):
    #     """Calculate positions on the critical path between agent, key, door, and goal."""
    #     critical_positions = []

    #     # Add horizontal path from agent to door (assumes door is always to the right of agent)
    #     agent_x, agent_y = self.agent_start_pos
    #     if(self.door_pos is not None):
    #         door_x, door_y = self.door_pos  # Assuming self.door_pos has been set in add_door_and_key_randomly
    #         critical_positions.extend([(x, agent_y) for x in range(agent_x, door_x + 1)])

    #     # Add vertical path from door to goal (assumes goal is always below door)
    #     goal_x, goal_y = self.grid_size - 2, self.grid_size - 2
    #     if(self.door_pos is not None):
    #         critical_positions.extend([(door_x, y) for y in range(door_y, goal_y + 1)])


    #     if(self.key_pos is not None):
    #     # Add positions around the key to ensure it is reachable
    #         key_x, key_y = self.key_pos  # Assuming self.key_pos has been set in add_door_and_key_randomly
    #         critical_positions.extend([
    #             (key_x + dx, key_y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]
    #             if 0 <= key_x + dx < self.grid_size and 0 <= key_y + dy < self.grid_size
    #         ])
    #     return critical_positions
    
    def add_pickup_and_place_object(self):
        if not self.grid.get(self.grid_size - 2, self.grid_size - 2):
            self.put_obj(Goal(), self.grid_size - 2, self.grid_size - 2)
        # if 2 in self.level_configuration:
        if 4 in self.level_configuration:
            # If level 2 is in the configuration, place a ball next to the door.
            door_x, door_y = self.door_pos
            # Check the side of the door and place the ball accordingly.
            if door_x > 1:
                ball_pos = (door_x - 1, door_y)
            else:
                ball_pos = (door_x + 1, door_y)
            self.put_obj(CustomBox('red'), *ball_pos)
        else:
            # If level 4 is not in the configuration, create a wall with a gap and place the ball there.
            wall_x = self.grid_size // 2
            gap_y = self.grid_size // 2
            self.grid.vert_wall(wall_x, 0, length=gap_y-1)
            self.grid.vert_wall(wall_x, gap_y+1, length=self.grid_size-gap_y-1)

            red_box_pos = (wall_x, gap_y)
            other_red_box_pos = (red_box_pos[0] - 0, red_box_pos[1] - 1)
            self.put_obj(CustomBox('red'), *red_box_pos)
            self.put_obj(CustomBox('red'), *other_red_box_pos)



          
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
    # Example of initializing the environment and configuring a level
    # env = CustomGridEnv(size=8)
    # env.configure_level([1, 2])  # This combines lava and door/key elements in the same level

    # # Example on how to use it with manual control or integrate into a game loop
    # # For this example, we'll just print out the initial state
    # print(env.grid)  # Depending on your setup, you might visualize it differently
    env = CustomGridEnv(size=12,render_mode="human")
    # env.configure_level([1,2,3]) #213 works 
    env.configure_level([1,2,3,4,5,6]) #213 works 
    manual_control = ManualControl(env, seed = 42)
    manual_control.start()
if __name__ == "__main__":
    main()








# do we care about optimal steps?


# Update numbers above to reflect this
#1 - regular
#2 - lava
#3 - Open Door 
#3 - Door and key
#4 - Dynamic Obstabcles
#5 - Pick up Object and drop 
#6 - Memory






