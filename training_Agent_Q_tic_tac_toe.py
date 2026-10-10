import numpy as np
import pickle as pkl


run = True
grid = np.zeros((3, 3))
gamer = [1, 2]
N_EPISODES = 500000
EPISODE = 0
EXPLORATION = 0.2
lr = 0.2
gamma = 0.9


def transform_choice(choice):
    choice = choice.replace(",", " ")
    choice = choice.replace(";", " ")
    choice = choice.split()

    try:
        choice = [int(p) for p in choice]
    except ValueError:
        return None

    return choice


def fill_grid(grid, player, choice):
    correspondant_choice_in_grid = [p - 1 for p in choice]
    x, y = correspondant_choice_in_grid[0], correspondant_choice_in_grid[1]

    if grid[x, y] == 0:
        grid[x, y] = player
        return True, grid
    else:
        return False, grid


def verify_grid(grid, gamer):
    full = bool(np.all(grid != 0))

    diag = np.diag(grid)
    diag2 = np.diag(np.fliplr(grid))

    for player in gamer:
        lines_win = np.any(np.all(grid == player, axis=1))
        columns_win = np.any(np.all(grid == player, axis=0))
        diag_win = np.all(diag == player)
        diag2_win = np.all(diag2 == player)

        if lines_win or columns_win or diag_win or diag2_win:
            return player, full

    return None, full


def verify_choice(choice):
    if choice is None or len(choice) != 2:
        return False

    minimum = min(choice)
    maximum = max(choice)

    if minimum >= 1 and maximum <= 3:
        return True
    else:
        return False

def get_key(grid): 
    
    grid_list = list(grid)
    grid_list = [str(int(i)) for array in grid_list for i in array]
    key = "".join(grid_list) 
    
    return key  

def add_key(Q, key):
    if key in Q.keys():
        return None
    else :
        Q[key] = np.zeros((3,3))
        return None
    
    


counts_wins = {'1': 0,'2' : 0,'eqal' : 0}
counts_block = {'1': 0,'2' : 0,'eqal' : 0}
counter = 0
Q = {}
while EPISODE < N_EPISODES :
    previous_key, previous_action = None, None
    counter +=1
    while run:
        move_accepted = False

        while not move_accepted:
            positions = np.argwhere(grid == 0)
            valid_position = positions[np.random.randint(0,len(positions))]
            choice_gamer1 = list(valid_position)
            choice_gamer1 = [p+1 for p in choice_gamer1]
            bool_choice_1 = verify_choice(choice_gamer1)

            if not bool_choice_1:
                #print("Coordonnées invalides : entrez deux entiers entre 1 et 3.")
                continue

            move_accepted, grid = fill_grid(grid, gamer[0], choice_gamer1)

            if not move_accepted:
                pass
                #print("Case déjà prise. Choisissez une autre case.")

        recompense = 0
        win_player, state_grid = verify_grid(grid, gamer)
        #print(" Naïve Ordinateur 1 a joué ! ")
        #print(grid)

        if win_player is not None:
            #print(f"Le joueur {win_player} a gagné la partie.")
            counts_wins[str(win_player)] += 1
            counts_block[str(win_player)] += 1
            recompense = -1
            run = False
        elif state_grid:
            #print("Match nul.")
            counts_wins['eqal'] += 1
            counts_block['eqal'] += 1
            run = False

        if previous_key is not None : 
           line, column = previous_action
           key = get_key(grid)
           add_key(Q, key)
           if not run : 
               cible = recompense
           else:
               cible = recompense + gamma * np.max(Q[key][grid==0])
           
           Q[previous_key][line,column] +=  lr*(cible - Q[previous_key][line,column])
           
        if run:
            key = get_key(grid)
            add_key(Q, key)
                
            move_accepted = False

            while not move_accepted:
                if np.random.rand() < EXPLORATION : 
                    positions = np.argwhere(grid == 0)
                    valid_position = positions[np.random.randint(0,len(positions))]
                    choice_positions = list(valid_position)
                    choice_gamer2 = [p + 1 for p in choice_positions]
                    bool_choice_2 = verify_choice(choice_gamer2)
                else : 
                    
                    bool_valid_positions = np.where(grid == 0 , True , False)
                    valid_q_values = Q[key][bool_valid_positions]
                    positions_q_values_valid = np.argwhere(bool_valid_positions)
                    
                    max_value = np.max(valid_q_values)
                    max_valid_q_values_index = [pos for pos, value in enumerate(valid_q_values) if value == max_value]
                    index_random = np.random.randint(0, len(max_valid_q_values_index))
                    index_in_max_valid_q_values = max_valid_q_values_index[index_random]
                    choice_positions = positions_q_values_valid[index_in_max_valid_q_values]
                    
                    choice_gamer2 = [p + 1 for p in choice_positions]
                    bool_choice_2 = verify_choice(choice_gamer2)
                    
                if not bool_choice_2:
                    #print("Coordonnées invalides : entrez deux entiers entre 1 et 3.")
                    continue
                
                previous_key, previous_action = key, choice_positions
                move_accepted, grid = fill_grid(grid, gamer[1], choice_gamer2)

                if not move_accepted:
                    pass
                    #print("Case déjà prise. Choisissez une autre case.")
            
            recompense = 0
            win_player, state_grid = verify_grid(grid, gamer)

            if win_player is not None:
                #print(f"Le joueur {win_player} a gagné la partie.")
                counts_wins[str(win_player)] += 1
                counts_block[str(win_player)] += 1
                recompense = 1
                line, column = previous_action
                Q[previous_key][line,column] += lr*(recompense - Q[previous_key][line,column])
                run = False
            elif state_grid:
                #print("Match nul.")
                counts_wins['eqal'] += 1
                counts_block['eqal'] += 1
                line, column = previous_action
                Q[previous_key][line,column] += lr*(recompense - Q[previous_key][line,column])
                run = False
            
    run = True
    grid = np.zeros((3,3))           
    EPISODE += 1
    
    if counter % 1000 == 0 :
        wins_naive_computer = counts_block['1']
        wins_agent_Q= counts_block['2']
        null = counts_block['eqal']
        _TOTAL_GAMES = wins_naive_computer + wins_agent_Q + null
        print(f'Parties {EPISODE-1000+1} à {EPISODE} : victoires de l\'Agent Q : {wins_agent_Q/_TOTAL_GAMES:.1%}, défaites : {wins_naive_computer/_TOTAL_GAMES:.1%}, matchs nuls : {null/_TOTAL_GAMES:.1%}')
        counts_block = {'1': 0,'2' : 0,'eqal' : 0}
        counter = 0
    
with open("Q_table.pkl", "wb") as file : 
    pkl.dump(Q,file)
print("----------------------------------------------ENTRAINEMENT TERMINÉ----------------------------------------------")
print(
    f"Nombre de victoires total joueur 1 : {counts_wins['1']}, "
    f"Nombre de victoires total joueur 2 : {counts_wins['2']}, "
    f"Nombre de matchs total nuls : {counts_wins['eqal']}"
)