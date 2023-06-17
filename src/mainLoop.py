import numpy as np
import tqdm
import matplotlib.pyplot as plt
from message import Message
from mempool import Mempool
from miner import Miner
from opcodes import Opcode
import params
from TFM import EIP1559MultiDimensionalMechanism
from block import Block

# Load environment and lane parameters
ENV_PARAMS = params.env_params()
LANE_PARAMS = params.gas_lanes_params()
N_STEPS = 1000#ENV_PARAMS['N_steps']

# Instantiates the code
tfm = EIP1559MultiDimensionalMechanism(LANE_PARAMS)
mempool = Mempool()
miner = Miner(account_balance=0)
opcodes_names = list(params.eth_opcodes().keys())
chain = []


def compute_rate_message(base_fees):
    # TODO: make this a function of base fee
    return 30


def generate_random_messages(base_fees):
    rate_opcodes = 5
    rate_sps = 10
    rate_messages = compute_rate_message(base_fees)

    N_messages = np.random.poisson(rate_messages)
    list_of_messages = []
    for _ in range(N_messages):
        oc_list = []
        K = np.random.poisson(rate_opcodes) + 1
        S = np.random.poisson(rate_sps)
        sampled_opcodes = np.random.choice(opcodes_names, K)

        aux_list = list(sampled_opcodes)
        oc_list = [Opcode(name=a) for a in aux_list]
        for _ in range(S + 1):
            oc_list.append(Opcode(name='SP', gas_used=1e8 * np.random.random()))

        MESSAGE_NAME = 'msg'
        gas_fee_cap = [bf * (1 + 0.2 * np.random.random()) for bf in base_fees]
        gas_premium = [gas_fee_cap[i] - base_fees[i] for i in range(len(base_fees))]

        list_of_messages.append(Message(MESSAGE_NAME, gas_fee_cap, gas_premium, oc_list))
    return list_of_messages


def run_simulation(max_mempool_length=1000):
    for _ in tqdm.tqdm(range(N_STEPS)):
        list_of_messages = generate_random_messages(tfm.get_fees())
        [mempool.add_message(m) for m in list_of_messages]
        
        if tfm.tfms[0].base_fee<5e-9 or tfm.tfms[1].base_fee<5e-9:
            capacity=ENV_PARAMS['lane_widths']
        else:
            capacity=list(np.array(ENV_PARAMS['lane_widths'])/2)
        
        
        # caps the maximum mempool size to solve a faster knapsack problem
        if max_mempool_length<len(mempool.messages):
            
            diff=len(mempool.messages)-max_mempool_length
            diff=list(np.arange(diff))
            to_remove = [mempool.messages[i] for i in diff]
            mempool.remove(to_remove)
            

        try:
            proposed_block = miner.propose_block(mempool,capacity)
        except Exception as e:
            print(f"Error occurred while proposing a block: {str(e)}")
            continue

        to_remove = [mempool.messages[i] for i in proposed_block]
        block = Block(to_remove)
        
        mempool.remove(block.messages)
        chain.append(block)
        tfm.update_fees(block.gas_used)


def plot_base_fee_evolution():
    for i in range(ENV_PARAMS['N_lanes']):
        plt.semilogy(tfm.tfms[i].base_fee_list)
    plt.xlabel("Epochs")
    plt.ylabel("Base Fee")
    plt.title("Evolution of Base Fee")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    
def plot_gas_usage_evolution():
    
    for i in range(ENV_PARAMS['N_lanes']):
        gu=[chain[n].gas_used[i] for n in range(len(chain))]
        plt.plot(gu,label=f'lane={i}')
    plt.xlabel("Epochs")
    plt.ylabel("Gas Usage")
    plt.title("Evolution of Gas Usage")
    plt.legend()
    plt.grid(True)
    plt.show()



if __name__ == '__main__':
    run_simulation()
    plot_base_fee_evolution()
    plot_gas_usage_evolution()

