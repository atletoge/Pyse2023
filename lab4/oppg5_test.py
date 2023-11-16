import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
import simpy 

env = simpy.Environment()

# Given values
n_servers = 14 # Setter antall servere
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
sim_active = True # Brukes til å sjekke om vi har nådd 100 failures


def server_generator(env):
    while sim_active:
        yield env.timeout(np.random.exponential(1/lambda_srv))
        server(env)

def server(env):
    global active_servers, failures, sim_active
    if(active_servers < (n_servers+1) and active_servers > 0):
        active_servers = active_servers-1
        failures = failures + 1
        if (failures >= num_failures):
            sim_active = False


def repairmen_generator(env):
    while sim_active:
        yield env.timeout(np.random.exponential(1/mu_srv))
        repairmen(env)
        

def repairmen(env):
    global active_servers
    if (active_servers < n_servers):
        active_servers = active_servers+1



#Metode for å sjekke antall aktive servere til enhver tid (sjekker hvert minutt i dette tilfelle)
def checkServerUpCount():
    global servers_up
    global active_servers, sim_active
    while sim_active:
        servers_up[active_servers] += 1 # Teller hvor mye av tiden det er x antall aktive servere
        yield env.timeout(0.001)
        if failures >= num_failures:
            sim_active = False


simServer = env.process(server_generator(env))
simServerCount = env.process(checkServerUpCount())
simRepairmen = env.process(repairmen_generator(env))

running = env.run(until=SIM_TIME)
print(servers_up)



