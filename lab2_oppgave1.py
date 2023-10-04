import simpy
import numpy as np
import random

env = simpy.Environment()
SIM_TIME = 60*24
lam = 60
k = 0
n = 5
m = 5
Q_min = 0.5
price = 0
q = 1
i = 0 #Flytta denne opp hit

# def user_time():
#     return np.random.exponential(1)     Tror ikke vi trenger denne

def time_between_instances(): #bytte navn?
    return np.random.exponential(lam)

def user3_generator(env):
    while True:
        i = i + 1
        yield env.timeout(time_between_instances())
        env.process(user3, i)


def calculate_Q(m,n,k):
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
    k = k+1
    add_server()
    calculate_Q(m,n,k)
    if Q_min < q:
        print(f'User {id} logged in')
        user_login = env.now
        userPrice = calculate_price_for_user()
        yield env.timeout(1) #Endrer denne siden det ikke virker å være random timeout på user, ser ut som alle bruker 1 time
        time_active = env.now - user_login
        calculate_Q(m,n,k)
        print(f'User {id} was active for {time_active} minutes and had a bandwidth of {q} for the price of {userPrice} NOK.')
        k = k-1
        calculate_Q(m,n,k)
    else:
        k = k-1
        calculate_Q(m,n,k)
    remove_server()


def add_server():
    if (n<10):
        n = n+1

def remove_server():
    if (n>2):
        n = n-1

def calculate_price_for_user():
    totalPower = (m*n)*200
    return (totalPower/k)*price

def check_price_level():
    p_low = 0.1
    p_medium  = 1
    p_high = 5
    Liste = ["low", "high"]
    while True:
        add_server()
        price = p_low
        yield env.timeout(1)
        remove_server()
        while True:
            price = p_medium
            yield env.timeout(1)
            #Bruker bare random.choice her siden sannsynlighetsvariabelen p ikke er definert i oppgavetekstene, blir i praksis 0.5
            if(random.choice(Liste) == "low"): 
                break
            else:
                remove_server()
                price = p_high
                yield env.timeout(2)
                add_server()
       

# sim = env.process(user3_generator(env))

# env.run(until=SIM_TIME)



    







