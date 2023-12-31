import simpy
import numpy as np
import random
import matplotlib.pyplot as plt

env = simpy.Environment()
SIM_TIME = 60*24
lam = 1
k = 0 # Antall aktive sesjoner akkurat nå
n = 5 # Antall servere
m = 10 # Antall sesjoner per server
Q_min = 0.5 # Minimum q-verdi oppgitt i oppgavetekst
price = 0  # Prisen som justeres hele tiden
datacentercost = 0 # Total kostnad for datasenteret i løpet av simuleringen
q = 1 # Bandwidth
i = 0 # Totalt antall brukere
#Lister for å samle avg. q- og mos-verdier for hver bruker
avg_q_scores = []
avg_mos_scores = []
mos_per_hour = []
time_of_violation = 0
user_violated = set()
datacentercostlist = []

def time_between_instances(): #bytte navn?
    return np.random.exponential(lam)

def user3_generator(env):
    global i
    while True:
        i = i + 1
        yield env.timeout(time_between_instances())
        env.process(user3(env,i))


def calculate_Q(m,n,k):
    global q
    #m - antall resource slots, n - antall servere, k - antall brukere
    q = min(1, (m*n)/k)
    return q

def calculate_MOS(q):
    if q >= 0.9:
        return 5
    elif q >= 0.8 and q < 0.9:
        return 4
    
    elif q >= 0.6 and q < 0.8:
        return 3
    
    elif q >= 0.5 and q < 0.6:
        return 2
    
    else: return 1

def calculate_MOS_per_minute():
    global q
    global mos_per_hour
    for i in range(24*60):
        mos_per_hour.append(calculate_MOS(q))
        yield env.timeout(1)

def calculate_avg_MOS(avg_mos_scores):
    return sum(avg_mos_scores)/len(avg_mos_scores)
    

def calculate_datacenter_costs():
    global datacentercost
    global datacentercostlist
    for i in range(60*24):
        datacentercost = datacentercost + calculate_price()
        datacentercostlist.append(calculate_price())
        yield env.timeout(1)

#Hvordan user3-funksjon vil se ut før implementering av simulator (oppgave II.A.4):
# def user3(env, id):
#     k = k + 1
#     calculate_Q(m,n,k)
#     if Q_min < q:
#         print(f'User {id} logged in')
#         user_login = env.now
#         yield env.timeout(1) 
#         time_active = env.now - user_login
#         calculate_Q(m,n,k)
#         print(f'User {id} was active for {time_active} minutes and had a bandwidth of {q} for the price of {userPrice} NOK.')
#         k = k-1
#         calculate_Q(m,n,k)
#     else:
#         k = k-1
#         calculate_Q(m,n,k)


def user3(env, id):
    global k
    global n
    global m
    global time_of_violation
    global q
    global Q_min
    global avg_mos_scores
    global avg_q_scores
    global user_violated
    k = k+1
    q_values = []
    mos_scores = []
    add_server()
    calculate_Q(m,n,k)
    if Q_min < q:
        print(f'User {id} logged in')
        user_login = env.now
        #yield env.timeout(60) #Endrer denne siden det ikke virker å være random timeout på user, ser ut som alle bruker 1 time
        #Går minutt for minutt og regner lokal q og mos
        for minute in range(60):
            verdi = calculate_Q(m,n,k)
            if verdi < 0.5:
                user_violated.add(id)
                if time_of_violation == 0:
                    time_of_violation = env.now
            mos = calculate_MOS(verdi)
            q_values.append(verdi)
            mos_scores.append(mos)
            # while verdi >= 0.5:
            #     timeOfViolation += 1
            yield env.timeout(1)
        avg_q = sum(q_values)/len(q_values)
        avg_q_scores.append(avg_q)
        avg_mos = sum(mos_scores)/len(mos_scores)
        avg_mos_scores.append(avg_mos)
            
        time_active = int(env.now - user_login)
        print(f'User {id} was active for {time_active} minutes and had an average bandwidth of {round(q,2)} and a average MOS score of {round(avg_mos,2)}.')
        k = k-1
        calculate_Q(m,n,k)
    else:
        #Må klokke inn tida dersom første bruker ikke kom inn, men det kommer ikke til å skje
        if time_of_violation == 0:
            time_of_violation = env.now
        user_violated.add(id)
        print(f'User {id} got rejected...')
        k = k-1
        calculate_Q(m,n,k)
    remove_server()


def add_server():
    global n
    if (n<10):
        n = n+1

def remove_server():
    global n
    if (n>2):
        n = n-1

def calculate_price():
    totalPower = (m*n)*200*price
    return totalPower/60

def check_price_level():
    global price
    p_low = 0.1
    p_medium  = 1
    p_high = 5
    Liste = ["low", "high"]
    while True:
        add_server()
        price = p_low
        yield env.timeout(60)
        remove_server()
        while True:
            price = p_medium
            yield env.timeout(60)
            #Bruker bare random.choice her siden sannsynlighetsvariabelen p ikke er definert i oppgavetekstene, blir i praksis 0.5
            if(random.choice(Liste) == "low"): 
                break
            else:
                remove_server()
                price = p_high
                yield env.timeout(120)
                add_server()
       

sim = env.process(user3_generator(env))

sim1 = env.process(check_price_level()) #For å kjøre prisjustering

sim2 = env.process(calculate_datacenter_costs()) #For å kjøre kostnadsstatistikk i datasenter

sim3 = env.process(calculate_MOS_per_minute()) #For å beregne MOS hver time

env.run(until=SIM_TIME)


print(f''' \n
      ----------------------Statistics---------------------- \n
      Average cost in the data center: {round(datacentercost/(60*24),2)}NOK/minute \n
      Time to first GLSA violation: {round(time_of_violation,2)} minutes \n
      Propability for GLSA violation: {round(len(user_violated)/i,2)*100}% \n
      ''')


#Plot quality level over time
# time_x_axis = np.array([i for i in range(24*60)])
# mos_x_axis = np.array([item for item in mos_per_hour])
# cost_y_axis = np.array([item for item in datacentercostlist])
# plt.plot(time_x_axis, cost_y_axis)

# plt.xlabel("minutes")
# plt.ylabel("Price in NOK")

# plt.show()


# fig, ax1 = plt.subplots()

# color = 'tab:red'
# ax1.set_xlabel('time (m)')
# ax1.set_ylabel('Quality', color=color)
# ax1.plot(time_x_axis, mos_x_axis, color=color)
# ax1.tick_params(axis='y', labelcolor=color)

# ax2 = ax1.twinx()

# color = 'tab:blue'
# ax2.set_ylabel('price', color=color)
# ax2.plot(time_x_axis,cost_y_axis, color=color)
# ax2.tick_params(axis='y', labelcolor=color)

# fig.tight_layout()
# plt.show()





