# Gym TicTacToe
---------
Gym TicTacToe is a light TicTacToe environment for OpenAI Gym.

## Installation
1. Install [OpenAi Gym](https://github.com/openai/gym)
```
pip install gym
```

2. Download and install `gym-tictactoe`
```
git clone https://github.com/ClementRomac/gym-tictactoe
cd gym-tictactoe
python setup.py install
```

## Running
Start by importing the package and initializing the environment
```
import gym
import gym_tictactoe

env = gym.make('TicTacToe-v1')  
env.init()
```

As the TicTacToe is a two players game, you have to create two players (here we use random as action choosing strategy). The environment is not handling the two players part, so you have to do it in your code as shown below.
```
# Define symbols for rendering
ai_symbol = 'x'
random_symbol = 'o'

user = 0
done = False
reward = 0

# Reset the env before playing
state = env.reset()

while not done:
    env.render(mode=None)
    if user == 0:
        state, reward, done, infos = env.step(env.action_space.sample(), ai_symbol)
    elif user == 1:
        state, reward, done, infos = env.step(env.action_space.sample(), random_symbol)
       
    # If the game isn't over, change the current player
    if not done:
        user = 0 if user == 1 else 1
    else :
        print("Infos : " + str(infos))
        if reward == 10:
            print("Draw !")
        elif reward == -20:
            if user == 0:
                print("Random wins ! AI Reward : " + str(r))
            elif user == 1:
                print("AI wins ! AI Reward : " + str(-r))
        elif reward == 20:
            if user == 0:
                print("AI wins ! AI Reward : " + str(r))
            elif user == 1:
                print("Random wins ! AI Reward : " + str(-r))

```

*Warning : If you play on a position where you or your opponent already played, you'll get a 'bad_position' reward and will loose the game*

## Settings
You can change the environment settings by editing the `settings.xml` placed in your `gym-tictactoe` installation folder.

Currently, the settings only allow you to change the rewards values.