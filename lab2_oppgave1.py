import simpy
import numpy as np
import random

env = simpy.Environment()
SIM_TIME = 60*24
lam = 1
k = 0
n = 5
m = 5
Q_min = 0.5
price = 0
datacentercost = 0
q = 1
i = 0 #Flytta denne opp hit
#Lister for å samle avg. q- og mos-verdier for hver bruker
avg_q_scores = []
avg_mos_scores = []
time_of_violations = []
# def user_time():
#     return np.random.exponential(1)     Tror ikke vi trenger denne

def time_between_instances(): #bytte navn?
    return np.random.exponential(lam)

def user3_generator(env):
    global i
    while True:
        i = i + 1
        yield env.timeout(time_between_instances())
        env.process(user3, i)


def calculate_Q(m,n,k):
    global q
    #m - antall resource slots, n - antall servere, k - antall brukere
    q = min(1, (m*n)/k)

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

def calculate_avg_MOS(avg_mos_scores):
    return sum(avg_mos_scores)/len(avg_mos_scores)
    

def calculate_datacenter_costs():
    global datacentercost
    for i in range(60*24):
        datacentercost = datacentercost + calculate_price()

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
    global timeOfViolation
    global q
    global Q_min
    global avg_mos_scores
    global avg_q_scores
    k = k+1
    timeOfViolation = 0
    q_values = []
    mos_scores = []
    add_server()
    calculate_Q(m,n,k)
    if Q_min < q:
        print(f'User {id} logged in')
        user_login = env.now
        #yield env.timeout(60) #Endrer denne siden det ikke virker å være random timeout på user, ser ut som alle bruker 1 time
        #Går minutt for minutt og regner lokal q og mos
        for minute in range(61):
            verdi = calculate_Q(m,n,k)
            mos = calculate_MOS(verdi)
            q_values.append(verdi)
            mos_scores.append(mos)
            while verdi >= 0.5:
                timeOfViolation += 1
            yield env.timeout(1)
        avg_q = sum(q_values)/len(q_values)
        avg_q_scores.append(avg_q)
        avg_mos = sum(mos_scores)/len(mos_scores)
        avg_mos_scores.append(avg_mos)
        time_of_violations.append(timeOfViolation)

        time_active = env.now - user_login
        print(f'User {id} was active for {time_active} minutes and had a bandwidth of {q}.')
        k = k-1
        calculate_Q(m,n,k)
    else:
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
    return totalPower

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
       

# sim = env.process(user3_generator(env))

# sim1 = env.process(user3_generator(env)) For å kjøre prisjustering

# sim2 = env.process(user3_generator(env)) For å kjøre kostnadsstatistikk i datasenter

# env.run(until=SIM_TIME)



#print(f"Gjennomsnittlig kost på datasenteret i simuleringen har vært {datacentercost/(60*24)}")    







