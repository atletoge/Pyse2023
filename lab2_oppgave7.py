import lab2_oppgave1 as lab
import simpy

def reset_global_values():
    global k
    global n
    global m
    global Q_min
    global price
    global datacentercost
    global q
    global i
    global avg_q_scores
    global avg_mos_scores
    global mos_per_hour
    global time_of_violation
    global user_violated
    global datacentercostlist
    global SIM_TIME
    global env

    env = simpy.Environment()
    SIM_TIME = 60*24
    k = 0 # Antall aktive sesjoner akkurat nå
    n = 5 # Antall servere
    m = 5 # Antall sesjoner per server
    Q_min = 0.5 # Minimum q-verdi oppgitt i oppgavetekst
    price = 0  # Prisen som justeres hele tiden
    datacentercost = 0 # Total kostnad for datasenteret i løpet av simuleringen
    q = 1 # Bandwidth
    i = 0 # Totalt antall brukere
    avg_q_scores = [] #Samle opp avg. q-verdier for hver bruker
    avg_mos_scores = [] #Samle opp avg. mos-verdier for hver bruker
    mos_per_hour = [] #Liste for å samle mos-verdier i systemet hver time til plotting
    time_of_violation = 0 #For å måle første GLSA violation i systemet
    user_violated = set() #Samle opp alle som har opplevd GLSA violation
    datacentercostlist = [] #Samle opp kostnadene over tid 

average_time_GSLA = []
probability_GSLA = []
average_bandwidth = []
average_quality = []
average_cost = []
for i in range(10):
    lab.env
    lab.sim
    lab.sim1
    lab.sim2
    lab.sim3
    lab.test
    average_cost.append(round(lab.datacentercost/(60*24),2))
    average_time_GSLA.append(round(lab.time_of_violation,2))
    probability_GSLA.append(round(len(lab.user_violated)/lab.i,2)*100)
    average_bandwidth.append(round(sum(lab.avg_q_scores)/len(lab.avg_q_scores), 2))
    average_quality.append(round(sum(lab.avg_mos_scores)/len(lab.avg_mos_scores), 2))
    reset_global_values()

print(average_cost)