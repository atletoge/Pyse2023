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
failures = 0
SIM_TIME = 24*60
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
            trackDowntimeParalell = None
            trackDowntimeSeriell = None
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

downtimeListeSeriell1 = downtimeListeSeriell
downtimeListeParalell1 = downtimeListeParalell

#Start simulation with repairmen=2
sim_active = True
trackDowntimeSeriell = None
trackDowntimeParalell = None
downtimeListeSeriell = []
downtimeListeParalell = []
failures = 0

env1 = simpy.Environment()

simServer1 = env1.process(server_generator(env1))
simRepairmen1 = env1.process(repairmen_generator(env1))
simRepairmen2 = env1.process(repairmen_generator(env1))

running2 = env1.run(until=SIM_TIME)
downtimeListeSeriell2 = downtimeListeSeriell
downtimeListeParalell2 = downtimeListeParalell

#Start simulation with repairmen=3
sim_active = True
trackDowntimeSeriell = None
trackDowntimeParalell = None
downtimeListeSeriell = []
downtimeListeParalell = []
failures = 0

env2 = simpy.Environment()

simServer2 = env2.process(server_generator(env2))
simRepairmen3 = env2.process(repairmen_generator(env2))
simRepairmen4 = env2.process(repairmen_generator(env2))
simRepairmen5 = env2.process(repairmen_generator(env2))

running3 = env2.run(until=SIM_TIME)
downtimeListeSeriell3 = downtimeListeSeriell
downtimeListeParalell3 = downtimeListeParalell

def calculate_confidence_interval(data):
    # Function to calculate the confidence interval
    mean_value = np.mean(data)
    std_dev = np.std(data)
    confidence_interval = t.interval(0.95, len(data) - 1, loc=mean_value, scale=std_dev/np.sqrt(len(data)))
    return confidence_interval

# Calculate mean and confidence intervals
mean1 = np.mean(downtimeListeSeriell1)
ci1 = calculate_confidence_interval(downtimeListeSeriell1)

mean2 = np.mean(downtimeListeSeriell2)
ci2 = calculate_confidence_interval(downtimeListeSeriell2)

mean3 = np.mean(downtimeListeSeriell3)
ci3 = calculate_confidence_interval(downtimeListeSeriell3)

# Plotting
repairmen_scenarios = [1, 2, 3]
means = [mean1, mean2, mean3]
conf_intervals = [ci1, ci2, ci3]

plt.errorbar(repairmen_scenarios, means, yerr=np.array(conf_intervals).T, fmt='o', capsize=5)
plt.xlabel('Number of Repairmen')
plt.ylabel('Average Downtime (Seriell)')
plt.title('Average DowntimeSeriell with 95% Confidence Intervals')
plt.show()


# # Calculate the confidence interval using numpy
# confidence_level = 0.95
# data_seriell = np.array(downtimeListeSeriell)
# mean_seriell = np.mean(data_seriell)
# confidence_interval_seriell = np.percentile(data_seriell, [100 * (1 - confidence_level / 2), 100 * (confidence_level / 2)])
# std_seriell = np.std(data_seriell)

# # Print the results
# print(f"Mean Downtime (Seriell): {mean_seriell}")
# print(f"Standard Deviation (Seriell): {std_seriell}")
# print(f"Confidence Interval (95%) (Seriell): {confidence_interval_seriell}")

# # Plot the results using errorbar
# plt.errorbar(1, mean_seriell, yerr=std_seriell, fmt='o', label='Mean Downtime (Seriell)')
# plt.title('Mean Downtime with 95% Confidence Interval (Seriell)')
# plt.xlabel('Simulation Results')
# plt.ylabel('Mean Downtime')
# plt.legend()
# plt.show()