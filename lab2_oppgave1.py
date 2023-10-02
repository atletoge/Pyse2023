import simpy
import numpy as np

env = simpy.Environment()
SIM_TIME = 60*24
lam = 60

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

# def user3(env, id):
#     print(f"User {id} created")
#     time_created = env.now
#     yield env

