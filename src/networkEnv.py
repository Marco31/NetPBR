import gym
from gym import spaces
import numpy as np
import time

print(gym.__version__)

#simulation de l'environnement réseau :
#tate spacee: (a, b, c)
#pertubation toutes les 10-12 secondes

class NetworkEnv(gym.Env):
    def __init__(self, threshold_a, threshold_b, threshold_c, alpha, beta):
        super(NetworkEnv, self).__init__()
        self.threshold_a = threshold_a
        self.threshold_b = threshold_b
        self.threshold_c = threshold_c
        self.alpha = alpha
        self.beta = beta
        self.a_mean = 10
        self.a_std = 1
        self.b_mean = 100
        self.b_std = 10
        self.c_mean = 1000
        self.c_std = 100
        self.perturbation_duration = np.random.randint(2,3)  # durée de la pertubation
        self.last_perturbation_time = time.time()
        self.perturbation_active = False
        self.action_space = spaces.Discrete(2)  # 2 actions
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 0]), high=np.array([np.inf, np.inf, np.inf]), dtype=np.float32
        )
        self.state = None
        self.steps_beyond_threshold = None
        self.LINK_SELECT_ACTION_INTERNET = 0
        self.LINK_SELECT_ACTION_MPLS = 1

    def reset(self,a=None,b=None,c=None):
        # self.state = np.zeros(3)

        a = np.abs(np.random.normal(self.a_mean, self.a_std))
        b = np.abs(np.random.normal(self.b_mean, self.b_std))
        c = np.random.randint(low=0, high=10)
        self.state = np.array([a, b, c])

        self.steps_beyond_threshold = None
        self.last_perturbation_time = time.time()  # reset le dernier temps de pertubation
        self.perturbation_active = False
        return self.state

    # def perturb_values(self):
    #     perturbed_values = np.array([
    #         np.random.normal(self.a_mean * 3, self.a_std*0.5),
    #         np.random.normal(self.b_mean, self.b_std),
    #         np.random.randint(0, 10)
    #     ])
    #     self.state = perturbed_values

    def step(self, action):
        assert self.action_space.contains(action), "Invalid action"
        new_state= self.state # nouvelle etat qui stocke letat initial
        if action ==0 :
            pass
        # a = np.abs(np.random.normal(self.a_mean, self.a_std))
        # b = np.abs(np.random.normal(self.b_mean, self.b_std))
        # c = np.random.randint(low=0, high=10)
        # self.state = np.array([a, b, c])
        done = False
        current_time = time.time()
        tick_perturb = current_time - self.last_perturbation_time
        # print(tick_perturb)s
        if tick_perturb > self.perturbation_duration:
            if not self.perturbation_active:
                self.perturbation_active = True
                self.start_perturbation_time = current_time

            elapsed_perturbation_time = current_time - self.start_perturbation_time

            if elapsed_perturbation_time < self.perturbation_duration:
                perturbation_factor = elapsed_perturbation_time / self.perturbation_duration
                perturbed_values = np.array([
                    np.random.normal(self.a_mean * 5, self.a_std),
                    np.random.normal(self.b_mean, self.b_std),
                    # np.random.normal(0, 0),
                    np.random.randint(0, 10)
                ])
                self.state = perturbation_factor * perturbed_values
            else:
                self.perturbation_active = False
                self.last_perturbation_time = current_time

        elif action==1:
            self.state=new_state

        # reward=0
        # perturbation_active = self.perturbation_active
        # if perturbation_active:
        #     reward -= 20
        # else :
        #     reward+=5
        reward=0
        if action==0 :
            reward = self.alpha * (35-self.state[0]) + self.beta * self.state[1]
            print('reward: ' ,reward)

        terminated= False
        #
        if abs(self.state[0]) >= 50 and action ==0:
                reward-=2000
                terminated = True


        # else:
        #     if action==1:
        #         reward-=4
        # reward = self.calculate_reward(self.state)
        # if self.state[0] < 12 and self.state[1]<120 and action == 1:
        #     reward -= 10
        # elif self.state[0] > 12 and self.state[1]>120 and action == 1:
        #     reward += 20



        return self.state, reward, terminated, {}

    def calculate_reward(self, state):
        reward = -1

        # reward += state[1] * 0.1


        # reward += (1 / state[2]) * 0.2
        reward += (1 / state[0]) * 100

        # if state[2] > 0:
        #     reward -= state[2] * 0.05


        return reward

    def render(self, mode="human"):
        pass


# env = MyEnvironment(threshold_a=9, threshold_b=90, threshold_c=5, alpha=-10, beta=-2)
# observation = env.reset()




