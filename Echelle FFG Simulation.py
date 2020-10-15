######################################################
########             Progression              ########
########        Of a under-evalatued          ########
########                player                ########
######################################################

import numpy as np
import math
import random
import matplotlib.pyplot as py

def sim_player(init_ffg_lvl, init_real_lvl, num_sim = 1000, adv_spread = 25):
    #Adversaries are created using a normal distribution around the current public level
    #TODO : model tournaments in depth
    
    matchs = []
    lvl_history = [[]]
    adv_history = [[]]

    for i in range(0, num_sim):
        ffg_lvl = init_ffg_lvl
        real_lvl = init_real_lvl
        
        matchs.append(0)
        
        lvl_history.append([ffg_lvl])
        adv_history.append([0]) #This is just for ease, so that lvl_history and ffg_history are updated on the same index
        
        while(ffg_lvl < real_lvl):
            matchs[i] += 1;
            adv_lvl = np.random.normal(ffg_lvl, adv_spread) 
            D_ffg = abs(ffg_lvl - adv_lvl)
            D_real = abs(real_lvl - adv_lvl)
            #con & a calculation
            table = [{116,200},{110,195},{105,190},{100,185},{95,180},{90,175},{85,170},{80,165},{75,160},{70,155},{65,150},{60,145},{55,140},{51,135},{47,130},{43,125},{39,120},{35,115},{31,110},{27,105},{24,100},{21,95},{18,90},{15,85},{13,80},{11,75},{10,70}]
            index = math.floor((min(max(-1950,ffg_lvl),650)  + 1950)/100)
            
            (con,a) = table[index]
            e = 0 #We can adjust this later if needed but it shouldn't have too much of an effect
            S_ffg = 1 / (math.exp(D_ffg/a) + 1)
            S_real = 1 / (math.exp(D_real/a) + 1)
            
            S_ffg = (1 - S_ffg) if (ffg_lvl > adv_lvl) else S_ffg
            S_real = (1 - S_real) if (real_lvl > adv_lvl) else S_real
            
            A = 1 if (random.random() < S_real) else 0
            ffg_lvl += con * (A - S_ffg)
            
            lvl_history[i].append(ffg_lvl)
            adv_history[i].append(adv_lvl)
            
    return (matchs,lvl_history,adv_history)

num_sim = 200
elos = []
avg_50 = []
avg_75 = []
avg_90 = []
for elo in range(-1000, 300, 10):
    
    (matchs,lvl_history, adv_history) = sim_player(elo,elo+400,num_sim, 25)
    sort_m = sorted(matchs)
    idx_75 = math.floor(num_sim*75/100)
    idx_90 = math.floor(num_sim*90/100)
    
    elos.append(elo)
    avg_50.append(np.mean(matchs))
    avg_75.append(sort_m[idx_75])
    avg_90.append(sort_m[idx_90])

# print(f"Shortest time : {min(matchs)}")
# print(f"Average games needed : {np.mean(matchs)}")
# print(f"75% time : {sort_m[idx_75]}")
# print(f"90% time : {sort_m[idx_90]}")
# print(f"Longest time : {max(matchs) }")

# for i in range(0,len(lvl_history), math.floor(num_sim/10)): 
    # py.plot(lvl_history[i])

#idx= matchs.index(min(matchs))
#py.plot(lvl_history[idx])
#idx= matchs.index(max(matchs))
#py.plot(lvl_history[idx])
line1, = py.plot(elos, avg_50, 'b-', label = "Moyenne", linewidth = 2)
line2, = py.plot(elos, avg_75, 'g--', label = "Pire 25%")
line3, = py.plot(elos, avg_90, 'r--', label = "Pire 10%")
py.ylabel("Parties")
py.xlabel("Elo de départ")
py.title("Nombre de parties nécessaires pour monter un joueur sous-évalué de 4 pierres")
py.legend(handles=[line1, line2, line3], loc='upper left')
py.show()