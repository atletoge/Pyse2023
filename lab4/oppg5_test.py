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
SIM_TIME = 24*60 #Vet ikke hvor lenge vi skal simulere
servers_up = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
verdier = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
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


def calculateStandardDeviation():
    global servers_up, verdier
    meanValue = np.dot(servers_up,verdier)/sum(servers_up)
    print(meanValue)
    varians = 0
    for i in range(len(servers_up)):
        varians += (servers_up[i]*(i-meanValue)**2)/len(servers_up)
    return np.sqrt(varians)



simServer = env.process(server_generator(env))
simServerCount = env.process(checkServerUpCount())
simRepairmen = env.process(repairmen_generator(env))

running = env.run(until=SIM_TIME)
print(servers_up)

standardDeviation = calculateStandardDeviation()
meanDowntimeSeriell = (sum(servers_up)-servers_up[-1])/sum(servers_up)
print(meanDowntimeSeriell)

print(standardDeviation)


# Calculate the confidence interval
confidence_level = 0.95
degrees_of_freedom = len(servers_up) - 1
alpha = 1 - confidence_level

# Calculate the standard error of the mean
standard_error = standardDeviation / np.sqrt(len(servers_up))

# Calculate the margin of error
margin_of_error = t.ppf(1 - alpha / 2, degrees_of_freedom) * standard_error

# Calculate the confidence interval
lower_bound = meanDowntimeSeriell - margin_of_error
upper_bound = meanDowntimeSeriell + margin_of_error

# Plot the results
fig, ax = plt.subplots()
ax.bar(verdier, servers_up, alpha=0.7, label='Server Count')
ax.errorbar([np.mean(verdier)], [meanDowntimeSeriell], yerr=[margin_of_error], fmt='ro', label='Mean Downtime (95% CI)')

ax.set_xlabel('Number of Active Servers')
ax.set_ylabel('Count')
ax.legend()
plt.show()
