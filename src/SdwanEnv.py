import gym
from gym import spaces
import numpy as np
from numpy.random import default_rng

class SDWANEnv(gym.Env):

    def __init__(self):

        self.action_space = spaces.Discrete(2)  # 2 actions : 0 (INTERNET), 1 (MPLS)
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(3,), dtype=np.float32)  # [latence, bande passante, perte de paquets]
        self.latence_min=2
        self.bandwidth_max=20


        # a implementer
        self.packet_loss_max=0.2
        self.nb_flow=None




    def reset(self,latency=15,bandwith=800,nb_flow=1):
        self.latency = latency
        self.bandwidth = bandwith
        self.packet_loss = np.random.uniform(0, 1)
        self.nb_flow=nb_flow
        return self.get_observation()




    def step(self, action):
        # self.latency = np.random.uniform(9, 50)
        # self.bandwidth = np.random.uniform(400, 800)
        # self.packet_loss = np.random.uniform(0, 1)
        if action == 0:  # INTERNET
            self.latency -= 1
            self.bandwidth += 2
            self.packet_loss -= 0.01
            # pass
        elif action == 1:  # MPLS
            # self.latency -= np.random.uniform(3, 4)
            # self.bandwidth -= np.random.uniform(0, 20)
            # self.packet_loss-= np.random.uniform(0, 0.2)
            self.latency -= 2
            self.bandwidth += 3
            self.packet_loss -= 0.02
        # if self.latency<0:
        #     self.latency=0
        if self.packet_loss<0:
            self.packet_loss=0
        # elif self.bandwidth>1000:
        #     self.bandwidth=1000

        if (self.latency < self.latence_min or self.bandwidth > self.bandwidth_max):
            done = True
            self.latency=self.latence_min
            self.bandwidth=self.bandwidth_max
        else:
            done = False

        reward = self.get_reward(action)

        return self.get_observation(), reward, done, {}


    def get_observation(self):
        return np.array([self.latency, self.bandwidth, self.packet_loss])


    def get_reward(self,action):

        reward = -10 * self.latency + 10 * self.bandwidth

        if action==0:
            pass
        elif action ==1: # on pénalise si on passe sur MPLS
            reward= -10 *reward
        return reward
