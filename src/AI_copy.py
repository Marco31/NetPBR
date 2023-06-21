"""Module AI Manage AI thread and communicate with Controller thread."""

__author__ = 'Marc VEYSSEYRE'

import time
import ast
import logging

DEBUG = True

from DQN import Agent
from Utils import plotLearning
from gym_sdwan_stat.envs import sdwan_stat_env
import gym
import numpy as np
from networkEnv import NetworkEnv
import time

# Enregistrement de l'environnement

gym.register(
    id='NetworkEnv-v0',
    entry_point='networkEnv:NetworkEnv',
    kwargs={'threshold_a': 5, 'threshold_b': 7, 'threshold_c': 30, 'alpha': 30, 'beta': 0}
)

env = gym.make('NetworkEnv-v0')
agent = Agent(gamma=0.99, epsilon=1.0, batch_size=64, n_actions=2, eps_end=0.01,input_dims=[3], lr=0.001)
scores, eps_history = [], []
n_games = 5000

class StageAI:
    """Class representing a AI thread"""
    def __init__(self):
        logging.basicConfig(filename="src/logs/AI.log",
            level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        logging.info("Init AI...")
        print("Init AI...")
        self.loop_nb = 0
        self.set_ACL = False
        self.lst_service_channel = None
        self.throughput_input = None
        self.throughput_output = None
        self.pck_loss = None
        self.latency_avg = None
        self.latency_sigma = None
        self.latency_max = None
        self.bandwidth = None

        self.action = None

    def pased_q_list(self, qlst):
        """Function to parse queue list send from Controler into data useful for AI."""
        # latency_sdw1_2_sdw2 = q_list[2]
        self.lst_service_channel = ast.literal_eval(qlst[0])
         # throughput_input by interface (bit/s) [Gi1/0/1, Gi1/0/2]
        self.throughput_input = ast.literal_eval(qlst[1])
        self.throughput_output = ast.literal_eval(qlst[2])
        self.pck_loss = ast.literal_eval(qlst[3])
        self.latency_avg = float(qlst[4])
        self.latency_sigma = float(qlst[5])
        self.latency_max = float(qlst[6])
        self.bandwidth = float(qlst[7])

    def stage4AI(self, queueS1, queueS2):
        """Function where AI thread is start."""
        print("stage2")
        while True:
            # Check if Request is receive
            pre_queue = "update lists"
            # msg = queueS1.get()    # wait till there is a msg from sController

            msg = "nothing"

            if msg == "ERR_CISCO":
                print("Cisco switch disconnect")
            elif msg == "ERR_DATA":
                print("Data not ready")
            elif msg == 's1 is DONE ':
                break # ends While loop
            elif(self.loop_nb == 0):
                pre_queue = "NOACL"
            else:


                # Perform Action
                # q_list = msg.split('|')
                # self.pased_q_list(q_list)

                #print("- - - sAI RECEIVED from sController:")
                #print(self.lst_service_channel)
                #print(self.throughput_input) # by interface
                #print(self.throughput_output) # by interface
                #print(self.pck_loss) # by interface
                #print(self.latency_avg)
                #print(self.latency_sigma)
                #print(self.latency_max)
                #print(self.bandwidth)

                # if network is not full do
                # pre_queue = "NOACL"
                # otherwise if you want  for example to reroute http (80) and https (443) do
                # pre_queue = "80|443"

                # AI beginning

                score = 0
                done = False

                # observation = np.array([self.latency_avg, self.bandwidth, self.pck_loss])
                observation = env.reset()

                i = 0
                while not done:
                    i += 1
                    action = agent.choose_action(observation)

                    observation_, reward, terminated, truncated = env.step(action)

                    done = terminated or truncated
                    score += reward
                    agent.store_transition(observation, action, reward,
                                           observation_, done)
                    agent.learn()

                    # on passe à l'observation suivante
                    observation = observation_
                    print("ob : ", observation)
                    print("action : ", action)
                    # print("reward: " , reward)

                    # on attribue aux champs l'action retenue
                    self.action = action

                    print('action')

                    # ## Changement de lien
                    #
                    # if self.action == 0:
                    #     print("On envoie sur ethernet")
                    #     pre_queue = "NOACL"
                    #
                    # else:
                    #     print("on envoie sur MPLS")
                    #     pre_queue = "80|443"

                    if i > 10000:
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

                ## Changement de lien

                if self.action == 0:
                    print("On envoie sur ethernet")
                    pre_queue = "NOACL"

                else:
                    print("on envoie sur MPLS")
                    pre_queue = "80|443"


                if DEBUG:
                    print("self.loop_nb :" + str(self.loop_nb))
                    if self.loop_nb == 2:
                        if self.set_ACL:
                            self.set_ACL = False
                            pre_queue = "80|443|1000"
                            print("Set ACL for port 80 and 443 (2)...")
                            # pre_queue = "NOACL"
                            # print("Unset ACL...")
                            # logging.info("Unset ACL...")
                        else:
                            self.set_ACL = True
                            pre_queue = "80|443|1000"
                            print("Set ACL for port 80 and 443...")
                            logging.info("Set ACL for port 80 and 443...")
                    else :
                        pre_queue = "0"
            self.loop_nb +=1
            time.sleep(1) # work
            # Send Request
            queueS2.put(pre_queue)
            print("Applied")
            time.sleep(7) # work

if __name__ == '__main__':
    print("Start AI")


    # TEST lancement du main

    from multiprocessing import Process, Queue
    import Controller
    
    SAI = StageAI()
    #
    queueSCTR = Queue()
    queueSAI = Queue()
    SAI.stage4AI(queueSCTR, queueSAI)
