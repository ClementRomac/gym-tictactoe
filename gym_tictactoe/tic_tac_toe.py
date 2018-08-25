import gym
from gym import spaces, error
import xml.etree.ElementTree as ET
import os

class TicTacToeEnv(gym.Env):
    def __init__(self):
        super(TicTacToeEnv, self).__init__()
        settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.xml')
        self.load_xml_settings(settings_file)
        
    def load_xml_settings(self, settings_file):
        settings_tree = ET.parse(settings_file)
        settings_root = settings_tree.getroot()
        for child in settings_root:
            if child.tag == 'Rewards':
                self.set_rewards(child)
        
    def set_rewards(self, rewards_section):
        self.rewards = {}
        for reward in rewards_section:
            self.rewards[reward.attrib['description']] = int(reward.attrib['reward'])

    def init(self, symbols):
        self.symbols = {
            symbols[0]: "x",
            symbols[1]: "o"
        }
        self.action_space = spaces.Discrete(9)

    def _reset(self):
        self.state_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        return self.state_vector

    # ------------------------------------------ GAME STATE CHECK ----------------------------------------
    def is_win(self):
        grid = self.state_vector
        if (grid[0] == grid[1]) and (grid[0] == grid[2]) and (grid[0] != 0):
            return True
        elif (grid[3] == grid[4]) and (grid[3] == grid[5]) and (grid[3] != 0):
            return True
        elif (grid[6] == grid[7]) and (grid[6] == grid[8]) and (grid[6] != 0):
            return True
        elif (grid[0] == grid[3]) and (grid[0] == grid[6]) and (grid[0] != 0):
            return True
        elif (grid[1] == grid[4]) and (grid[1] == grid[7]) and (grid[1] != 0):
            return True
        elif (grid[2] == grid[5]) and (grid[2] == grid[8]) and (grid[2] != 0):
            return True
        elif (grid[0] == grid[4]) and (grid[0] == grid[8]) and (grid[0] != 0):
            return True
        elif (grid[2] == grid[4]) and (grid[2] == grid[6]) and (grid[2] != 0):
            return True
        else:
            return False

    def is_draw(self):
        for i in range(9):
            if self.state_vector[i] == 0:
                return False
        return True

    # ------------------------------------------ ACTIONS ----------------------------------------
    def _step(self, action, symbol):
        is_position_already_used = False

        if self.state_vector[action] != 0:
            is_position_already_used = True

        if is_position_already_used:
            self.state_vector[action] = "Bad"
            reward_type = 'bad_position'
            done = True
        else:
            self.state_vector[action] = symbol

            if self.is_win():
                reward_type = 'win'
                done = True
            elif self.is_draw():
                reward_type = 'draw'
                done = True
            else:
                reward_type = 'still_in_game'
                done = False

        return self.state_vector, self.rewards[reward_type], done, {'already_used_position': is_position_already_used}

    # ------------------------------------------ DISPLAY ----------------------------------------
    def get_state_vector_to_display(self):
        new_state_vector = []
        for value in self.state_vector:
            if value == 0:
                new_state_vector.append(value)
            else:
                new_state_vector.append(self.symbols[value])
        return new_state_vector

    def print_grid_line(self, grid, offset=0):
        print(" -------------")
        for i in range(3):
            if grid[i + offset] == 0:
                print(" | " + " ", end='')
            else:
                print(" | " + str(grid[i + offset]), end='')
        print(" |")

    def display_grid(self, grid):
        self.print_grid_line(grid)
        self.print_grid_line(grid, 3)
        self.print_grid_line(grid, 6)
        print(" -------------")

        print()

    def _render(self, mode=None, close=False):
        self.display_grid(self.get_state_vector_to_display())

    def _close(self):
        return None

    def _seed(self, seed=None):
        return [seed]