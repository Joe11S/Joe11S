#this is a ranking system used in osu.

import random

def print_dictionary(dictionary):
    for key, value in dictionary.items():
        print(f"{key}: {value}")

def main(
        base_perfect = 0, base_good = 0, base_bad = 0, base_miss = 0, #note judgements
        EZ = False, NF = False, HT = False, #Difficulty reduction mods
        HR = False, SD = False, PF = False, DT = False, NC = False, HD = False, FL = False, #Difficulty increase mods
        RL = False, AP = False, SO = False, AT = False, CN = False, Sv2 = False #Special mods, only SO is considered ranked.
        ):
     
    def mainloop(perfect = 0, good = 0, bad = 0, miss = 0):
        def multiplier(EZ = False, NF = False, HT = False, HR = False, DT = False, NC = False, HD = False, FL = False, SO = False):
            active_mods = []
            final_multiplier = 1.0

            #Difficulty reduction mods
            if EZ == True:
                active_mods.append(0.5)
            if NF == True:
                active_mods.append(0.5)
            if HT == True:
                active_mods.append(0.3)

            #Difficulty increase mods
            if HR == True:
                active_mods.append(1.06)
            if DT == True:
                active_mods.append(1.12)
            if NC == True:
                active_mods.append(1.12)
            if HD == True:
                active_mods.append(1.06)
            if FL == True:
                active_mods.append(1.12)
            if SO == True:
                active_mods.append(0.90)

            for i in active_mods:
                final_multiplier *= i 
            
            return final_multiplier
                
        def fail_check(NF, SD, PF):
            if NF == True: #NF Flag
                return False
            
            if SD == True: #SD flag
                if miss > 0:
                    return True
            
            if PF == True: #perfect flag
                if accuracy != 100:
                    return True

            if life > 0:
               return False
            else:
               return True

        def accuracy_check(total_notes):
            accuracy = (((300*perfect)+(100*good)+(50*bad))/(300*total_notes))*100
            return round(accuracy, 2)

        def primary_grading_check(accuracy = 0):
            perfect_pct = (perfect/total_notes)*100
            bad_pct = (bad/total_notes)*100

            if accuracy == 100:
                ranking = "SS"
            elif perfect_pct >= 90 and bad_pct <= 1 and miss == 0:
                ranking = "S"
            elif (perfect_pct >= 80 and miss == 0) or perfect_pct >= 90:
                ranking = "A"
            elif (perfect_pct >= 70 and miss == 0) or perfect_pct >= 80:
                ranking = "B"
            elif perfect_pct >= 60:
                ranking = "C"
            else:
                ranking = "D"
            return ranking  

        game = [] #lists all the notes

        #make a list of note judgements
        for i in range(perfect):
            game.append(300)
        for i in range(good):
            game.append(100)
        for i in range(bad):
            game.append(50)
        for i in range(miss):
            game.append(0)
        
        random.shuffle(game)
        
        #combo sequences sector
        possible_combo_sequence = [2, 4, 8, 16] #an arbitrary list that determines a sequence
        combo_sequence = random.choice(possible_combo_sequence) #chooses a random value to form a combo sequence.
        combo_sequence_list = [] #lists notes played in a sequence

        #bonus flags
        is_katsu_sequence = False 
        is_geki_sequence = False

        #elapsed bonuses that update in realtime
        perfect = 0
        good = 0
        bad = 0
        miss= 0
        geki = 0
        katsu = 0

        #realtime updaters
        elapsed_note = 0 #lists the current number of the hit note
        elapsed_score = 0 #lists the current value of the hit note
        life = 1000 #displays life
        combo = 0 #displays combo
        highest_combo = 0 #displays highest combo
        fail = False #failure flag
        score = 0 #cumulative score
        accuracy = 0 #dynamic accuracy
        base_ranking = "" #dynamic rank

        #simulate scenario of a playthrough
        for i in range(len(game)):
            if game[i] == 300:
                elapsed_note += 1
                perfect += 1
                life += 20
                combo += 1
                if combo > highest_combo:
                    highest_combo = combo
                elapsed_score = (game[i]*combo)*multiplier(EZ, NF, HT, HR, DT, NC, HD, FL, SO)
                combo_sequence_list.append(300)
            elif game[i] == 100:
                elapsed_note += 1
                good += 1
                life += 10
                combo += 1
                if combo > highest_combo:
                    highest_combo = combo
                elapsed_score = (game[i]*combo)*multiplier(EZ, NF, HT, HR, DT, NC, HD, FL, SO)
                combo_sequence_list.append(100)
            elif game[i] == 50:
                elapsed_note += 1
                bad += 1
                if EZ == True:
                    life -= 20
                else:
                    life -= 40
                combo += 1
                if combo > highest_combo:
                    highest_combo = combo
                elapsed_score = (game[i]*combo)*multiplier(EZ, NF, HT, HR, DT, NC, HD, FL, SO)
                combo_sequence_list.append(50)
            elif game[i] == 0:
                elapsed_note += 1
                miss += 1
                if EZ == True:
                    life -= 40
                else:
                    life -= 80
                combo = 0
                elapsed_score = 0
                combo_sequence_list.append(0)
            total_notes = perfect+good+bad+miss #count all the notes

            if len(combo_sequence_list) == combo_sequence:
                if 0 not in combo_sequence_list: #Misses prevent a bonus.
                    if 50 not in combo_sequence_list: #50s also prevent a bonus.
                        if 100 not in combo_sequence_list:
                            geki += 1
                            life += 80
                            is_geki_sequence = True
                        else:
                            katsu += 1
                            life += 40
                            is_katsu_sequence = True                 
                combo_sequence_list = [] #resets the list in the sequence
                combo_sequence = random.choice(possible_combo_sequence) #chooses a new random value to form a combo sequence.   
            else:
                is_geki_sequence = False
                is_katsu_sequence = False             
            
            #update values
            score = round(score + elapsed_score) #update score
            accuracy = accuracy_check(total_notes) #update accuracy
            base_ranking = primary_grading_check(accuracy) #update rank
          
            if life>= 1000:
                life = 1000# cap life at 1000
            if life <= 0:
                life = 0 # cap life at 0

            #debugging section:
            if is_geki_sequence:
                print(str(elapsed_note), str(score), str(elapsed_score), str(combo), str(life), str(game[i]), str(accuracy)+"%", base_ranking, "激")
            elif is_katsu_sequence:
                print(str(elapsed_note), str(score), str(elapsed_score), str(combo), str(life), str(game[i]), str(accuracy)+"%", base_ranking,"喝")
            else:
                print(str(elapsed_note), str(score), str(elapsed_score), str(combo), str(life), str(game[i]), str(accuracy)+"%", base_ranking, len(combo_sequence_list))

            if fail_check(NF, SD, PF) == True: #consider unplayed notes as misses
                unplayed_notes = total_notes - miss
                miss = unplayed_notes + miss
                total_notes = perfect+good+bad+miss #count all the notes including updated misses
                accuracy = accuracy_check(total_notes) #update accuracy with updated misses
                fail = True
                break
        
        if combo == total_notes:
            remark = "Full Combo!"
        elif fail == False:
            remark = "Clear"
        else:
            remark = "Failed"
            
        return [score, highest_combo, life, accuracy, base_ranking, remark, fail, perfect, good, bad, miss, geki, katsu]

    active_mods = [] #list all active mods
    if EZ == True:
        active_mods.append("EZ")
    if NF == True:
        active_mods.append("NF")
    if HT == True:
        active_mods.append("HT")
    if HR == True:
        active_mods.append("HR")
    if SD == True:
        active_mods.append("SD")
    if PF == True:
        active_mods.append("Perfect")
    if DT == True:
        active_mods.append("DT")
    if NC == True:
        active_mods.append("NC")
    if HD == True:        
        active_mods.append("HD")
    if FL == True:
        active_mods.append("FL")
    if SO == True:           
        active_mods.append("SO")       
    
    if SD and PF:
        raise Exception("SD and PF cannot be active at the same time.")
    
    if DT and NC:
        raise Exception("DT and NC cannot be active at the same time.")
    
    if AT and CN:
        raise Exception("AT and CN cannot be active at the same time.")

    if (RL or AP or AT or CN or Sv2) == True: #if any of these mods are active, set to unranked:
        return ("Unranked. Ranks are not qualified if one of these mods is active")
    
    game = mainloop(base_perfect, base_good, base_bad, base_miss)

    #gather results from the game
    score = game[0]
    highest_combo = game[1]
    life = game[2]
    accuracy = game[3]
    base_ranking = game[4]
    remark = game[5]
    fail = game[6]
    perfect = game[7]
    good = game[8]
    bad = game[9]
    miss = game[10]
    geki = game[11]
    katsu = game[12]

    if HD or FL: #use this code block if HD or FL is active
        if base_ranking == "SS":
             ranking = "SS+"
        elif base_ranking == "S":
             ranking = "S+"
        else:
             ranking = base_ranking
    else: #if HD/FL is inactive, equate final ranking as base ranking by default
        ranking = base_ranking

    if fail == True: #If you fail, set to F
        ranking = "F"
    
    return {
        "Score": str(int(score)),
        "Life": str(int(life)),
        "Accuracy": str(round(accuracy, 2))+"%",
        "Combo": str(int(highest_combo)),
        "Rank": ranking,
        "Remark": remark,
        "Mods Used": str(active_mods),
        "300's": str(perfect),
        "100's": str(good),
        "50's": str(bad),
        "X's": str(miss),
        "激": str(geki),
        "喝": str(katsu)
    }

player = main(
    #note judgements
    int(input("Enter 300's: ")),
    int(input("Enter 100's: ")),
    int(input("Enter 50's: ")),
    int(input("Enter X's: ")),
    #Difficulty reduction mods
    bool(input("Is EZ on? (Use True or False)")),
    bool(input("Is NF on? (Use True or False)")),
    bool(input("Is HT on? (Use True or False)")),
    #Difficulty increase mods
    bool(input("Is HR on? (Use True or False)")),
    bool(input("Is SD on? (Use True or False)" )),
    bool(input("Is PF on? (Use True or False)")),
    bool(input("Is DT on? (Use True or False)")),
    bool(input("Is NC on? (Use True or False)")),
    bool(input("Is HD on? (Use True or False)")),
    bool(input("Is FL on? (Use True or False)")),
    #Special mods
    bool(input("Is RL on? (Use True or False)")),
    bool(input("Is AP on? (Use True or False)")),
    bool(input("Is SO on? (Use True or False)")),
    bool(input("Is AT on? (Use True or False)")),
    bool(input("Is CN on? (Use True or False)")),
    bool(input("Is Sv2 on? (Use True or False)"))
)
print_dictionary(player)
input()