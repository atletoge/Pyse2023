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
#lambda_f = 1/20
#lambda_r = 1/2
SIM_TIME = 24*60 #Vet ikke hvor lenge vi skal simulere
servers_up = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
active_servers = 14
sim_active = True


def server_generator(env):
    while sim_active:
        yield env.timeout(np.random.exponential(lambda_srv))
        env.process(server(env))

def server(env):
    global active_servers, failures
    if(active_servers < 15 and active_servers > 0):
        active_servers = active_servers-1
        failures = failures + 1
        if (failures >= 100):
            sim_active = False







#Metode for å sjekke antall aktive servere til enhver tid (sjekker hvert minutt i dette tilfelle)
def checkServerUpCount():
    global servers_up
    global active_servers
    while sim_active:
        servers_up[active_servers] = servers_up[active_servers] # Teller hvor mye av tiden det er x antall aktive servere
        env.timeout(1)


sim = env.process(server_generator(env))
simServerCount = env.process(checkServerUpCount())

running = env.run(until=SIM_TIME)



