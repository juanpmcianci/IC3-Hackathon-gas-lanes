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
ml=[]
mg=[]
def compute_rate_message(base_fees):
    # TODO: make this a function of base fee
    
    
    N_messages = np.random.poisson(10)

    return N_messages


def generate_random_messages(N_messages,base_fees):
    rate_opcodes = 100
    rate_sps = 2

    list_of_messages = []
    for _ in range(N_messages):
        oc_list = []
        K = np.random.poisson(rate_opcodes) 
        S = np.random.poisson(rate_sps)
        sampled_opcodes = np.random.choice(opcodes_names, K)

        aux_list = list(sampled_opcodes)
        oc_list = [Opcode(name=a) for a in aux_list]
        for _ in range(S ):
            oc_list.append(Opcode(name='SP', gas_used=1e8 * np.random.random()))

        MESSAGE_NAME = 'msg'
        gas_fee_cap = [bf * (1 + 0.2 * np.random.random()) for bf in base_fees]
        gas_premium = [gas_fee_cap[i] - base_fees[i] for i in range(len(base_fees))]

        list_of_messages.append(Message(MESSAGE_NAME, gas_fee_cap, gas_premium, oc_list))
    return list_of_messages


def sample_oom():
    
    r=np.random.randint(7,10)
    return np.random.random()*10**-r



def run_simulation(max_mempool_length=2000):
    for _ in tqdm.tqdm(range(N_STEPS)):
        
        
        N_messages=compute_rate_message(tfm.get_fees())
        
        list_of_messages = generate_random_messages(N_messages,tfm.get_fees())
        [mempool.add_message(m) for m in list_of_messages]
        capacity=ENV_PARAMS['lane_widths']

        if np.random.random()<0.5:
            
            bfs=np.array([tfm.tfms[i].base_fee for i in range(ENV_PARAMS['N_lanes'])])
            
            if all(bfs<sample_oom()):
                capacity=ENV_PARAMS['lane_widths']
            else:
                capacity=list(np.array(ENV_PARAMS['lane_widths'])*0.5*np.random.random())

        
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
            proposed_block=[]
            continue
    
        to_remove = [mempool.messages[i] for i in proposed_block]
        block = Block(to_remove,N_lanes=ENV_PARAMS['N_lanes'])
        
        mempool.remove(block.messages)
        chain.append(block)
        tfm.update_fees(block.gas_used)
        ml.append(len(mempool.messages))
        mg.append(sum([sum(m.gas_used) for m in mempool.messages]))


def plot_base_fee_evolution():
    for i in range(ENV_PARAMS['N_lanes']):
        if ENV_PARAMS['N_lanes']>1:
            if i==0:
                plt.semilogy(tfm.tfms[i].base_fee_list,label='priority lane')

            else:
                plt.semilogy(tfm.tfms[i].base_fee_list,label='other lane ')

        else:
            plt.semilogy(tfm.tfms[i].base_fee_list,label='unique')

        
    plt.xlabel("Epochs")
    plt.ylabel("Base Fee")
    plt.title("Evolution of Base Fee")
    plt.legend()
    plt.grid(True)
    #plt.show()
    
    
def plot_gas_usage_evolution():
    
    for i in range(ENV_PARAMS['N_lanes']):
        gu=[chain[n].gas_used[i] for n in range(len(chain))]
        if ENV_PARAMS['N_lanes']>1:
            if i==0:
                plt.plot(gu,label='priority lane')
            else:
                plt.plot(gu,label='Other lane')
        else:
            plt.plot(gu,label='One dimensional case')


    plt.xlabel("Epochs")
    plt.ylabel("Gas Usage")
    plt.title("Evolution of Gas Usage")
    plt.legend()
    plt.grid(True)
    #plt.show()

def plot_mempool_size_evolution():
    
    plt.plot(ml)
    plt.xlabel("Epochs")
    plt.ylabel("number of messages in mempool")
    plt.title("Evolution of mempool size")
    plt.legend()
    plt.grid(True)
    #plt.show()

def plot_mempool_gas_evolution():
    
    plt.plot(mg)
    plt.xlabel("Epochs")
    plt.ylabel("Total gas in mempool")
    plt.title("Evolution of mempool gas demand")
    plt.legend()
    plt.grid(True)
    #plt.show()

if __name__ == '__main__':
    
    plt.figure(figsize=(16,16))
    plt.rcParams.update({'font.size': 22})

    run_simulation()
    plt.subplot(221)
    plot_base_fee_evolution()
    plt.subplot(222)

    plot_gas_usage_evolution()
    plt.subplot(223)

    plot_mempool_size_evolution()
    plt.subplot(224)

    plot_mempool_gas_evolution()
    plt.tight_layout()

