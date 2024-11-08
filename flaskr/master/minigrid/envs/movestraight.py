from __future__ import annotations

from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Door, Goal, Key, Wall, Ball
from minigrid.manual_control import ManualControl
from minigrid.minigrid_env import MiniGridEnv
#kelsey added 
import random 
from minigrid.core.world_object import Ball, Point, WorldObj 
from minigrid.minigrid_env import MiniGridEnv 
from doorkey import DoorKeyEnv 
from gotodoor import GoToDoorEnv
from blockedunlockpickup import BlockedUnlockPickupEnv


class SimpleEnv(MiniGridEnv):
    def __init__(
        self,
        size=7,
        obstacle_type=Wall, 
        agent_start_pos=(3, 5),
        agent_start_dir=3,
        max_steps: int | None = None,
        **kwargs,
    ):
        
        self.obstacle_type = obstacle_type #kelsey added

        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 4 

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
        return "Move to green block in fewest steps" #add function below this?
    
    def place_walls(self): #kelsey added 
        pass

    def place_goal(self, num1, num2):
        pass

    def place_key(self, num1=4, num2=5):
        pass

    def state_mission(self):
        return "Here I ammmmm"
       
    def _gen_grid(self, width, height):
        self.grid = Grid(width, height)
        self.grid.wall_rect(0, 0, width, height)
        self.place_goal()
        self.place_walls() #kelsey added
        self.place_key()
        if self.agent_start_pos is not None: # Place the agen
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = self.state_mission()


#We can play with stuff using this ;)
class Level1_GoStraight(SimpleEnv):
    def __init__(self, agent_start_dir):
        super().__init__(agent_start_dir=agent_start_dir) #need to pass specific num to agent_star_dir

    def place_walls(self):
        i = 0
        while i < 5:
            self.put_obj(self.obstacle_type(), 1, 1 + i) 
            self.put_obj(self.obstacle_type(), 2, 1 + i)
            self.put_obj(self.obstacle_type(), 4, 1 + i)
            self.put_obj(self.obstacle_type(), 5, 1 + i) 
            i += 1

    def place_goal(self, num1=3, num2=1):
        self.put_obj(Goal(), num1, num2)


class Level2_Turn(Level1_GoStraight): #specific num steps to win level?
    def __init__(self):
        super().__init__(agent_start_dir=random.randrange(4))


class Level3_TurnRight(SimpleEnv):
    def __init__(self):
        super().__init__(max_steps=12, agent_start_dir=random.randrange(4)) #need to pass specific num to agent_star_dir

    def place_walls(self):
        i = 0
        while i < 5:
            self.put_obj(self.obstacle_type(), 1, 1 + i) #column, block in that column
            self.put_obj(self.obstacle_type(), 2, 1 + i)
            self.put_obj(self.obstacle_type(), 4, 2 + i) 
            self.put_obj(self.obstacle_type(), 5, 2 + i)
            i += 1

    def place_goal(self, num1=5, num2=1):
        self.put_obj(Goal(), num1, num2)


class Level4_MoveDown(SimpleEnv):
    def __init__(self):
        super().__init__(max_steps=12, agent_start_dir=random.randrange(4)) #need to pass specific num to agent_star_dir

    def place_walls(self):
        i = 0
        x = 0
        while i < 5:
            self.put_obj(self.obstacle_type(), 1, 1 + i) #column, block in that column
            self.put_obj(self.obstacle_type(), 2, 1 + i)
            self.put_obj(self.obstacle_type(), 4, 2 + i) 
            i += 1
        while x < 2:
            self.put_obj(self.obstacle_type(), 5, 4 + x)
            x += 1

    def place_goal(self, num1=5, num2=3):
        self.put_obj(Goal(), num1, num2)


class Level5_GoLeft(SimpleEnv):
    def __init__(self):
        super().__init__(agent_start_pos=(2, 5), max_steps=15, agent_start_dir=random.randrange(4)) #need to pass specific num to agent_star_dir

    def place_walls(self):
        i = 0
        while i < 5:
            self.put_obj(self.obstacle_type(), 1, 1 + i) #column, block in that column
            self.put_obj(self.obstacle_type(), 3, 2 + i) 
            i += 1

        self.put_obj(self.obstacle_type(), 5, 4)
        self.put_obj(self.obstacle_type(), 5, 5)
        self.put_obj(self.obstacle_type(), 4, 2)
        self.put_obj(self.obstacle_type(), 4, 4)
        self.put_obj(self.obstacle_type(), 4, 5)

    def place_goal(self, num1=4, num2=3):
        self.put_obj(Goal(), num1, num2)


class Level6_LeastSteps(SimpleEnv):
    def __init__(self):
        super().__init__(agent_start_pos=(2, 5), max_steps=15, agent_start_dir=random.randrange(4)) 

    def place_walls(self):
        i = 0
        while i < 3:
            self.put_obj(self.obstacle_type(), 2, 2 + i)
            self.put_obj(self.obstacle_type(), 4, 2 + i)
            i += 1
        self.put_obj(self.obstacle_type(), 3, 4)

    def place_goal(self, num1=3, num2=3):
        self.put_obj(Goal(), num1, num2)
    

class Level7_PickUpKey(SimpleEnv): 

    def __init__(self):
        super().__init__(size=8, agent_start_pos=(1, 6), max_steps=15, agent_start_dir=random.randrange(4))
        #super().place_key(num1=4, num2=5)

    # def place_walls(self):
    #     i = 0
    #     while i < 3:
    #         self.put_obj(self.obstacle_type(), 2, 2 + i)
    #         self.put_obj(self.obstacle_type(), 4, 2 + i) 
    #         i += 1
    #     self.put_obj(self.obstacle_type(), 3, 4)

    def place_goal(self, num1=6, num2=6):
        self.put_obj(Goal(), num1, num2)

    def place_key(self, num1=1, num2=1):
        self.put_obj(Key("yellow"), num1, num2)

    def state_mission(self):
        return "Pickup key & navigate to green block" 
    
class Level8_OpenDoor(GoToDoorEnv): 
    pass

class Level9_PickUpKeyOpenDoor(DoorKeyEnv):
    pass

#shift is used to drop an object
class Level10_UnblockDoor(DoorKeyEnv): #works but env yoru're inheriting must hold that object type/function

    def place_ball(self, num1=1, num2=3):
        self.put_obj(Ball("red"), num1, num2)



   

def main():
    #env = SimpleEnv(render_mode="human")

    #env = Level1_GoStraight(agent_start_dir=3) 
    #env = Level2_Turn() 
    #env = Level3_TurnRight() 
    #env = Level4_MoveDown()
    #env = Level5_GoLeft()
    #env = Level6_LeastSteps()
    #env = Level7_PickUpKey()
    #env = Level8_OpenDoor()
    #env = Level9_PickUpKeyOpenDoor()
    env = Level10_UnblockDoor()
    env.render_mode = "human"


    # enable manual control for testing
    manual_control = ManualControl(env, seed=42)
    manual_control.start()


    
if __name__ == "__main__":
    main()