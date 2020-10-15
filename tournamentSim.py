import math
import numpy as np
import random

def mcmahon0(rounds, ffg_lvl_init, real_lvl, adjustement=True):
    #Simply simulates a mcmahon tournament by estimating we get players half a stone stronger for each win, and half a stone weaker for each loss
    #rounds is the number of rounds
    #ffg_lvl is the public level at the start of tournament
    #real_lvl is the real level of the player
    #adjustement is a bool that controls wether we use the FFG adjustement algorithm
    
    #returns the public level of the player after the tournament
    
    table = [{116,200},{110,195},{105,190},{100,185},{95,180},{90,175},{85,170},{80,165},{75,160},{70,155},{65,150},{60,145},{55,140},{51,135},{47,130},{43,125},{39,120},{35,115},{31,110},{27,105},{24,100},{21,95},{18,90},{15,85},{13,80},{11,75},{10,70}]
    e = 0
    ffg_lvl = ffg_lvl_init
    index_real = math.floor((min(max(-1950,real_lvl),650)  + 1950)/100)
    #We model our opponents as a normal distribution, with a higher avg as we win, and an increased variance later in the tournament
    adv_avg = math.floor(ffg_lvl/100)*100+50 #Due to how pairing works, this is the average strength of our opposition
    adv_var = 25 #The variance will increase throughout the tournament.
    results = []
    advs = []
    for i in range(rounds):
        
        adv_lvl = np.random.normal(adv_avg, adv_var) 
        #adv_lvl = adv_avg
        D_ffg = abs(ffg_lvl - adv_lvl)
        D_real = abs(real_lvl - adv_lvl)
        
        #con & a calculation
        index = math.floor((min(max(-1950,ffg_lvl),650)  + 1950)/100)
        
        (con,a) = table[index]
        (cr,ar) = table[index_real]
        
        S_ffg = 1 / (math.exp(D_ffg/a) + 1)
        S_real = 1 / (math.exp(D_real/ar) + 1)
        
        S_ffg = (1 - S_ffg) if (ffg_lvl > adv_lvl) else S_ffg
        S_real = (1 - S_real) if (real_lvl > adv_lvl) else S_real
        
        A = 1 if (random.random() < S_real) else 0
        
        ffg_lvl += con * (A - S_ffg)
        
        adv_var += 12
        adv_avg += (A*2-1) * 50
        
        results.append(A)
        advs.append(adv_lvl)
        
        #print(f"Round {i+1} result : {A} vs a player rated {round(adv_lvl)}. Win percentage : {round(S_real*100)}%")
        
    if(ffg_lvl - ffg_lvl_init > 60):
        #print(f"Pre-adjustement level : {round(ffg_lvl)}") 
        prev_lvl = ffg_lvl
        cur_lvl = ffg_lvl_init + 60
        while True:
            #print(f"Current adjustment cycle starts at : {cur_lvl}")
            cur_lvl_start= cur_lvl
            for i in range(rounds):
                D_ffg = abs(cur_lvl - advs[i])
                S_ffg = 1 / (math.exp(D_ffg/a) + 1)
                S_ffg = (1 - S_ffg) if (cur_lvl > advs[i]) else S_ffg
                
                cur_lvl += con * (results[i] - S_ffg)
            #print(f"Current adjustment cycle ends at : {cur_lvl}")
            #input()
            if(cur_lvl - cur_lvl_start < 10):
                ffg_lvl = cur_lvl
                break
            prev_lvl = cur_lvl
            cur_lvl = cur_lvl_start + 60
            
    #print(f"End level after tournament : {ffg_lvl}")
    return ffg_lvl
