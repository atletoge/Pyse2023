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
SIM_TIME = 24*60
#servers_up = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#verdier = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
active_servers = 14
sim_active = True
trackDowntimeSeriell = None
trackDowntimeParalell = None
downtimeListeSeriell = []
downtimeListeParalell = []


def server_generator(env):
    while sim_active:
        yield env.timeout(np.random.exponential(1/lambda_srv))
        server(env)

def server(env):
    global active_servers, failures, sim_active, trackDowntimeParalell, trackDowntimeSeriell
    if (active_servers < (n_servers + 1) and active_servers > 0):
        active_servers = active_servers - 1
        failures += 1
        if (active_servers < n_servers and trackDowntimeSeriell == None): #Sjekker om det er ny downtime seriell
            trackDowntimeSeriell = env.now
        if (active_servers < 1 and trackDowntimeParalell == None): #Sjekker om det er ny downtime paralell
            trackDowntimeParalell = env.now
        if (failures >= num_failures):
            sim_active = False

def repairmen_generator(env):
    while sim_active:
        yield env.timeout(np.random.exponential(1/mu_srv))
        repairmen(env)

def repairmen(env):
    global active_servers, trackDowntimeSeriell, trackDowntimeParalell
    if (active_servers < n_servers):
        active_servers = active_servers + 1
        if(trackDowntimeSeriell != None and active_servers == n_servers): #Sjekker om downtime er over seriell
            downtimeListeSeriell.append(env.now-trackDowntimeSeriell)
            trackDowntimeSeriell = None
        if(trackDowntimeParalell != None and active_servers > 0): #Sjekker om downtime er over paralell
            downtimeListeParalell.append(env.now-trackDowntimeParalell)
            trackDowntimeParalell = None


simServer = env.process(server_generator(env))
simRepairmen = env.process(repairmen_generator(env))

running = env.run(until=SIM_TIME)

meanSeriell1 = np.mean(downtimeListeSeriell)
stdSeriell1 = np.std(downtimeListeSeriell)


# Calculate the confidence interval using numpy
confidence_level = 0.95
data_seriell = np.array(downtimeListeSeriell)
mean_seriell = np.mean(data_seriell)
confidence_interval_seriell = np.percentile(data_seriell, [100 * (1 - confidence_level / 2), 100 * (confidence_level / 2)])
std_seriell = np.std(data_seriell)

# Print the results
print(f"Mean Downtime (Seriell): {mean_seriell}")
print(f"Standard Deviation (Seriell): {std_seriell}")
print(f"Confidence Interval (95%) (Seriell): {confidence_interval_seriell}")

# Plot the results using errorbar
plt.errorbar(1, mean_seriell, yerr=std_seriell, fmt='o', label='Mean Downtime (Seriell)')
plt.title('Mean Downtime with 95% Confidence Interval (Seriell)')
plt.xlabel('Simulation Results')
plt.ylabel('Mean Downtime')
plt.legend()
plt.show()