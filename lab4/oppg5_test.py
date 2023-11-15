import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
import simpy 

env = simpy.Environment()

# Given values
n_servers = 14
lambda_srv = 0.1386
mu_srv = 13.86
num_failures = 100
repairmen_values = [1, 2, 3]
mdt_serial = []
mdt_parallell = []
failures = 0
lambda_f = 1/20
lambda_r = 1/2
SIM_TIME = 24*60 #Vet ikke hvor lenge vi skal simulere

def calculateMDT(liste):
    return round(sum(liste)/len(liste),3)

def time_between_failure():
    return np.random.exponential(lambda_f)

def time_between_repair():
    return np.random.exponential(lambda_r)

def server_generator(env):
    global n_servers
    i = 0
    while i <= n_servers:
        env.process(server(env, i))

def server(env, id):
    global num_failures
    count_failure = 0
    while count_failure < num_failures:
    #     if server fail:
    #         start = env.now
    #     if server repaired:
    #         slutt = env.now
    #         mdt.append(slutt-start)
        None
    #stopp simulering når vi har 100 failures.

sim = env.process(server_generator(env))

running = env.run(until=SIM_TIME)



