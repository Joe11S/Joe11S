import random

def remove_items(test_list, item):  
    # using list comprehension to perform the task 
    res = [i for i in test_list if i != item] 
    return res 


def play_game(wins):
    #initialize options
    options = ["rock", "paper", "scissors"]
    choices = ["rock", "paper", "scissors"]

    #initialize players
    computer_wins = 0
    player_wins = 0

    #initalize combo
    player_combo = 0
    highest_player_combo = 0

    while True:
        power = (options.count("rock") + options.count("paper") + options.count("scissors") - 2)

        print("Power:", power)

        user_choice = input("Enter your choice (rock, paper, scissors): ").lower()
        
        if user_choice not in choices:
            print("Invalid choice. Please select rock, paper, or scissors.")
            continue

        computer_choice = random.choice(options)
        print(f"Computer chose: {computer_choice}")
        
        #game starts here

        if user_choice == computer_choice:
            options = remove_items(options, computer_choice)#computer will be less likely to tie: both the user choice and computer choices will be removed, increasing chances of counterattack
            print("It's a tie!")
        elif (user_choice == "rock" and computer_choice == "scissors") or \
            (user_choice == "scissors" and computer_choice == "paper") or \
            (user_choice == "paper" and computer_choice == "rock"): #when player wins
            player_wins = player_wins + 1
            player_combo = player_combo + 1 #increase player combo
            options.append(user_choice) #makes computer more likely to tie the player
            options = remove_items(options, computer_choice) #computer will be less likely to lose
            print(str(player_wins)+"-"+str(computer_wins), "Combo:", player_combo)            
        else: #when computer wins
            computer_wins = computer_wins + 1
            player_combo = 0 #break combo
            options.append(computer_choice) #makes computer more likely to attack with the same item
            print(str(player_wins)+"-"+str(computer_wins), "Combo:", player_combo)               

        if player_combo > highest_player_combo:
            highest_player_combo = highest_player_combo + 1
        
        if player_wins >=wins:
            if player_combo == wins and computer_wins == 0: 
                print("Perfect!! Combo:", highest_player_combo)
            elif player_combo == wins:
                print("Full Combo! Combo:", highest_player_combo)
            else: 
                print("You win! Combo:", highest_player_combo)
            break
        
        if computer_wins >=wins:
            print("You lose. Combo:", highest_player_combo)
            break

        for i in choices: #add choices every turn
            options.append(i)

if __name__ == "__main__":
    play_game(int(input("Enter number of wins: ")))
    input()