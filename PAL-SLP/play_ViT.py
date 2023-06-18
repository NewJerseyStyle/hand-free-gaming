import time
import torch
import pyautogui
import numpy as np
from sentence_transformers import SentenceTransformer
from PIL import Image

import chromadb
chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="dqn_vmem",
    metadata={"hnsw:space": "cosine"})

model = SentenceTransformer('clip-ViT-B-32')
end_emb = model.encode(Image.open('1.png'))
start_emb = model.encode(Image.open('0.png'))
tran_emb = model.encode(Image.open('3.png'))
fight_emb = model.encode(Image.open('4.png'))
hit_emb = model.encode(Image.open('44.png'))
collection.add(
    embeddings=[end_emb.tolist(), start_emb.tolist(),
                tran_emb.tolist(), fight_emb.tolist(), hit_emb.tolist()],
    ids=['case0', 'case1',
         'case_f0', 'case_f1', 'case_f2']
)

c1, c2 = pyautogui.size()
region=(c1/2-321, c2/2-216, 642, 432)

class Net(torch.nn.Module):
    def __init__(self, n_observations=512, n_actions=13):
        super(Net, self).__init__()
        self.layer1 = torch.nn.Linear(n_observations, 128)
        self.layer2 = torch.nn.Linear(128, 128)
        self.layer3 = torch.nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = torch.nn.functional.relu(self.layer1(x))
        x = torch.nn.functional.relu(self.layer2(x))
        return self.layer3(x)

class DQN(object):
    def __init__(self):
        self.eval_net, self.target_net = Net(), Net()

        self.learn_step_counter = 0                                     # for target updating
        self.memory_counter = 0                                         # for storing memory
        self.memory = np.zeros((100, 512 * 2 + 2))     # initialize memory
        self.optimizer = torch.optim.AdamW(self.eval_net.parameters(),
                                           lr=1e-4,
                                           amsgrad=True)
        # self.loss_func = torch.nn.MSELoss()
        self.loss_func = torch.nn.SmoothL1Loss()

    def choose_action(self, x):
        x = torch.unsqueeze(torch.FloatTensor(x), 0)
        # input only one sample
        if np.random.uniform() < 0.3:   # greedy
            actions_value = self.eval_net.forward(x)
            action = torch.max(actions_value, 1)[1].data.numpy()
            action = action[0]  # return the argmax index
        else:   # random
            print('random act')
            action = np.random.randint(0, 5)
            action = action
        return action

    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, [a, r], s_))
        # replace the old memory with new memory
        index = self.memory_counter % 100
        self.memory[index, :] = transition
        self.memory_counter += 1

    def learn(self):
        # target parameter update
        if self.learn_step_counter % 10 == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_counter += 1

        # sample batch transitions
        sample_index = np.random.choice(100, 32)
        b_memory = self.memory[sample_index, :]
        b_s = torch.FloatTensor(b_memory[:, :512])
        b_a = torch.LongTensor(b_memory[:, 512:512+1].astype(int))
        b_r = torch.FloatTensor(b_memory[:, 512+1:512+2])
        b_s_ = torch.FloatTensor(b_memory[:, -512:])

        # q_eval w.r.t the action in experience
        q_eval = self.eval_net(b_s).gather(1, b_a)  # shape (batch, 1)
        q_next = self.target_net(b_s_).detach()     # detach from graph, don't backpropagate
        q_target = b_r + 0.9 * q_next.max(1)[0].view(32, 1)   # shape (batch, 1)
        loss = self.loss_func(q_eval, q_target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


def sensitivity_adj(x):
    if x < 1:
        return 1
    return x-x/2000

dqn = DQN()

key_dict = ['up_0.5',
            'up_1.0',
            'up_2.0',
            'down_0.5',
            'down_1.0',
            'down_2.0',
            'left_0.5',
            'left_1.0',
            'left_2.0',
            'right_0.5',
            'right_1.0',
            'right_2.0',
            'a_2.0']
speed = 1
im = pyautogui.screenshot(region=region)
s = model.encode(im)
step_num = 0
neg_gain = 10
while True:
    results = collection.query(
        query_embeddings=[s.tolist()],
        n_results=1
    )
    if results['distances'][0][0] != 0:
        insert_db_id = str(step_num)
        if ('case_f' in results['ids'][0][0]
            and abs(results['distances'][0][0]) < 0.1):
            insert_db_id = 'case_f_' + insert_db_id
        collection.add(
            embeddings=[s.tolist()],
            ids=[insert_db_id]
        )
        step_num += 1
    if (results['ids'][0][0] == 'case0'
        and abs(results['distances'][0][0]) < 0.1):
        print('[debug] assume entry')
        with pyautogui.hold('left'):
            time.sleep(2)
            im = pyautogui.screenshot(region=region)
            s = model.encode(im)
        continue
    elif (results['ids'][0][0] == 'case1'
          and abs(results['distances'][0][0]) < 0.1):
        print('[debug] assume exit')
        with pyautogui.hold('right'):
            time.sleep(2)
            im = pyautogui.screenshot(region=region)
            s = model.encode(im)
        continue
    elif ('case_f' in results['ids'][0][0]
          and abs(results['distances'][0][0]) < 0.1):
        print('[debug] assume fight')
        with pyautogui.hold('a'):
            time.sleep(2)
            im = pyautogui.screenshot(region=region)
            s_ = model.encode(im)
            # reward high
            a = 4
            r = 5
            dqn.store_transition(s, a, r, s_)
            s = s_
        continue
    a = dqn.choose_action(s)
    key, t = key_dict[a].split('_')
    with pyautogui.hold(key):
        print('[debug] move', key)
        time.sleep(float(t)/speed)
    im = pyautogui.screenshot(region=region)
    s_ = model.encode(im)
    r = 5
    if collection.count() > 10:
        results = collection.query(
            query_embeddings=[s_.tolist()],
            n_results=10
        )
        dist = np.asarray(results['distances']).flatten()
        # if new image, high reward
        r = np.sum(np.abs(dist)-0.1)
        r *= neg_gain if r < 0.1 else 1
        neg_gain = sensitivity_adj(neg_gain)
    r = max(min(r, 5), -5)
    dqn.store_transition(s, a, r, s_)
    if dqn.memory_counter > 100:
        dqn.learn()
    s = s_
