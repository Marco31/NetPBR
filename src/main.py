from DQN import Agent
from Utils import plotLearning
from gym_sdwan_stat.envs import sdwan_stat_env
import gym
import numpy as np
from networkEnv import NetworkEnv
import time

# import de la partie script
# on récupère le script




gym.register(
    id='NetworkEnv-v0',
    entry_point='networkEnv:NetworkEnv',
    kwargs={'threshold_a': 5, 'threshold_b': 7, 'threshold_c': 30, 'alpha': 30, 'beta': 0}
)

if __name__ == '__main__':
    # env = gym.make('Sdwan-stat-v0')
    env = gym.make('NetworkEnv-v0')
    # env = gym.make('LunarLander-v2')
    # env = gym.make('Breakout-v0')
    # env = gym.make('SpaceInvaders-v0')
    # env = InventoryEnv()
    agent = Agent(gamma=0.99, epsilon=1.0, batch_size=64, n_actions=2, eps_end=0.01,input_dims=[3], lr=0.001)
    # agent = Agent(gamma=0.99, epsilon=0.99, batch_size=64, n_actions=4, eps_end=0.01,input_dims=[8], lr=0.001)
    # agent = Agent(gamma=0.99, epsilon=1.0, batch_size=64, n_actions=3000, eps_end=0.01,input_dims=[9], lr=0.001)
    scores, eps_history = [], []
    n_games = 5000
    for i in range(n_games):
        score = 0
        done = False
        observation = env.reset()
        i=0
        while not done:
            i+=1
            # env.render()
            #un episode est une solution si on fait un changement quand il ya pertubation
            action = agent.choose_action(observation)
            observation_, reward, terminated,truncated = env.step(action)
            done = terminated or truncated
            score += reward
            agent.store_transition(observation, action, reward,
                                   observation_, done)
            agent.learn()
            observation = observation_
            print("ob : ",observation)
            print("action : " , action)
            # print("reward: " , reward)
            if i>10000:
                time.sleep(0.5)
            # time.sleep(0.6)
            if done:
                break

        scores.append(score)
        eps_history.append(agent.epsilon)
        avg_score = np.mean(scores[-100:])
        print('episode ', i, 'score %.2f' % score,
              'average score %.2f' % avg_score,
              'epsilon %.2f' % agent.epsilon)
    x = [i + 1 for i in range(n_games)]
    filename = '../Sdwan.png'
    plotLearning(x, scores, eps_history, filename)

# total_reward =0
# while True:
#     state = env.reset()
#     done = False
#     while not done:
#         print("State:", state)
#         action = agent.choose_action(state)
#         print("action:", action)
#         state_, reward, terminated, truncated = env.step(action)
#         done = terminated or truncated
#         score += reward
#         print("Reward:", reward,"score : ",score)
#         state = state_
#         if state[0]==1:
#             done=True


