#state= vecteur de x elts donc on utilise seulement les couches lineaires et non convolutionnels

# remember :DQN doesnt work for continuous action space

#IMPORTS
import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

# 2 classes
#agent has a deep q network and memory (learn from experience)
#deep q network = nn that takes a set of states as input
#outputs the agents estimate of action values for each given state in the input


#in pytorch every class that extends the functionnality of the base nn layers
#derives from a module for backpropagation

#neural network to approximate the q value
#we approximaate the q values using a function approximator
#(neural network), we parameterize the q function with a parameter
#theta and compute the q value. we just just feed the state
#and the nn will return the q value of all possible actions
#in that state, then select the best one

class DeepQNetwork(nn.Module):
    def __init__(self, lr, input_dims, fc1_dims, fc2_dims,
                 n_actions):
        super(DeepQNetwork, self).__init__()#appele le constructeur pour la classe de base
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions
        self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)#premiere layer
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
        self.fc3 = nn.Linear(self.fc2_dims, self.n_actions)
        #deep q network= estimate of the value of each action given some set of state


        self.optimizer = optim.Adam(self.parameters(), lr=lr)#adam=optimizer
        self.loss = nn.MSELoss()#mean squarred eror loss
        # bc qlearning = linear regression where we minimize the distance
        #= fit a line to the delta between the target value and output of the deep neural network

        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):#forward propagation
        #we want to pass the states into the first fully connected layer then
        #activate it with a value fonction
        #then we pass the output from that layer into the second connected layer and again
        #activate it with a value fonction and finally
        #we pass that output to the 3d connected layer but we dont want to activate it
        #we want to return that value
        #we dont activate the 3rd bc we want to get the agents raw estimate
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        actions = self.fc3(x)

        return actions


class Agent:
    def __init__(self, gamma, epsilon, lr, input_dims, batch_size, n_actions,
                 max_mem_size=100000, eps_end=0.05, eps_dec=5e-4):
        self.gamma = gamma #weighting of future rewards
        self.epsilon = epsilon#solution to explore/exploit dilemma
        #how often does the agent spend exploring its environment versus
        # taking the best known action and that has to be some finite
        self.eps_min = eps_end
        self.eps_dec = eps_dec#by what to decrement epsilon with each time step
        self.lr = lr
        self.action_space = [i for i in range(n_actions)]
        self.mem_size = max_mem_size
        self.batch_size = batch_size#batch size because
        # we're gonna be learning from a batch of memories
        self.mem_cntr = 0#we need a memory counter =  keep track of the
        # position of the first available memory for storing the agent's memory
        self.iter_cntr = 0
        self.replace_target = 100

        self.Q_eval = DeepQNetwork(lr, n_actions=n_actions,
                                   input_dims=input_dims,
                                   fc1_dims=256, fc2_dims=256)
        self.state_memory = np.zeros((self.mem_size, *input_dims),
                                     dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_dims),
                                         dtype=np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool)

    def store_transition(self, state, action, reward, state_, terminal):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = terminal

        self.mem_cntr += 1

    def choose_action(self, observation):
        if np.random.random() > self.epsilon:
            state = T.tensor([observation], dtype=T.float32).to(self.Q_eval.device)
            #state = T.tensor([observation]).to(self.Q_eval.device)
            actions = self.Q_eval.forward(state)
            action = T.argmax(actions).item()
        else:
            action = np.random.choice(self.action_space)

        return action

    def learn(self):
        if self.mem_cntr < self.batch_size:
            return

        self.Q_eval.optimizer.zero_grad()

        max_mem = min(self.mem_cntr, self.mem_size)

        batch = np.random.choice(max_mem, self.batch_size, replace=False)
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        state_batch = T.tensor(self.state_memory[batch]).to(self.Q_eval.device)
        new_state_batch = T.tensor(
                self.new_state_memory[batch]).to(self.Q_eval.device)
        action_batch = self.action_memory[batch]
        reward_batch = T.tensor(
                self.reward_memory[batch]).to(self.Q_eval.device)
        terminal_batch = T.tensor(
                self.terminal_memory[batch]).to(self.Q_eval.device)

        q_eval = self.Q_eval.forward(state_batch)[batch_index, action_batch]
        q_next = self.Q_eval.forward(new_state_batch)
        q_next[terminal_batch] = 0.0

        q_target = reward_batch + self.gamma*T.max(q_next, dim=1)[0]

        loss = self.Q_eval.loss(q_target, q_eval).to(self.Q_eval.device)
        loss.backward()
        self.Q_eval.optimizer.step()

        self.iter_cntr += 1
        self.epsilon = self.epsilon - self.eps_dec \
            if self.epsilon > self.eps_min else self.eps_min