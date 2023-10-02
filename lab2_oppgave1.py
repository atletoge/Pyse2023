import simpy
import numpy as np

env = simpy.Environment()
SIM_TIME = 60*24
lam = 60
k = 0
n = 5
m = 5
def user_time():
    return np.random.exponential(lam)

def time_between_instances(): #bytte navn?
    return np.random.exponential(lam/2)

def user3_generator(env):
    i = 1
    while True:
        yield env.timeout(time_between_instances())
        env.process(user3, i)
        i += 1
        k += 1

def calculate_Q(m,n,k):
    #m - antall resource slots, n - antall servere, k - antall brukere
    return min(1, (m*n)/k)

def calculate_MOS(Q):
    if Q >= 0.9:
        return 5
    elif Q >= 0.8 and Q < 0.9:
        return 4
    
    elif Q >= 0.6 and Q < 0.8:
        return 3
    
    elif Q >= 0.5 and Q < 0.6:
        return 2
    
    else: return 1

def user3(env, id):
    print(f'User {id} logged in')
    user_login = env.now
    yield env.timeout(user_time())
    time_active = env.now - user_login
    print(f'User {id} was active for {time_active} minutes')


def add_server():
    n += 1

def remove_server():
    n -= 1

def check_price_level():
    p_low = 0.1
    p_medium  = 1
    p_high = 5

    







