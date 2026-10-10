import numpy as np
import pickle as pkl 
from pathlib import Path

q_path = Path(__file__).resolve().parent / "Q_table.pkl"
with open(q_path, "rb") as file : 
    Q = pkl.load(file)
    
def get_key(grid): 
    grid_list = list(grid)
    grid_list = [str(int(i)) for array in grid_list for i in array]
    key = "".join(grid_list) 
    return key  


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


def play_game(Q):
    run = True
    grid = np.zeros((3, 3))
    gamer = [1, 2]

    while run:
        move_accepted = False

        while not move_accepted:
            choice_gamer1 = input(
                "Joueur 1 : Quelle case souhaitez-vous choisir ? "
                "Entrez une ligne et une colonne entre 1 et 3, "
                "séparées par une virgule, un point-virgule ou un espace : "
            )
            choice_gamer1 = transform_choice(choice_gamer1)
            bool_choice_1 = verify_choice(choice_gamer1)

            if not bool_choice_1:
                print("Coordonnées invalides : entrez deux entiers entre 1 et 3.")
                continue

            move_accepted, grid = fill_grid(grid, gamer[0], choice_gamer1)

            if not move_accepted:
                print("Case déjà prise. Choisissez une autre case.")

        win_player, state_grid = verify_grid(grid, gamer)
        print(grid)

        if win_player is not None:
            print(f"Le joueur {win_player} a gagné la partie.")
            run = False
        elif state_grid:
            print("Match nul.")
            run = False

        if run:
            move_accepted = False

            while not move_accepted:
                key = get_key(grid)
                if key not in Q : 
                    positions = np.argwhere(grid == 0)
                    valid_position = positions[np.random.randint(0,len(positions))]
                    choice_gamer2 = list(valid_position)
                    choice_gamer2 = [p + 1 for p in choice_gamer2]
                else : 
                    valid_q_values = Q[key][grid == 0]
                    positions_valid = np.argwhere(grid == 0)
                    
                    max_q_val = np.max(valid_q_values)
                    index_max_values = [pos for pos, value in enumerate(valid_q_values) if value == max_q_val]

                    ind_rand = np.random.randint(0,len(index_max_values))
                    index = index_max_values[ind_rand]
                    indice = positions_valid[index]
                    choice_gamer2 = list(indice)
                    choice_gamer2 = [p + 1 for p in choice_gamer2]
                    
                bool_choice_2 = verify_choice(choice_gamer2)

                if not bool_choice_2:
                    print("Coordonnées invalides : entrez deux entiers entre 1 et 3.")
                    continue
                
                move_accepted, grid = fill_grid(grid, gamer[1], choice_gamer2)

                if not move_accepted:
                    print("Case déjà prise. Choisissez une autre case.")

            win_player, state_grid = verify_grid(grid, gamer)
            print(" L'Ordinateur a joué ! ")
            print(grid)

            if win_player is not None:
                print(f"Le joueur {win_player} a gagné la partie.")
                run = False
            elif state_grid:
                print("Match nul.")
                run = False


if __name__ == '__main__' : 
    PLAY = True
    while PLAY : 
        play_game(Q)
        CORRECT_ANSWER = False

        while not CORRECT_ANSWER :
            answer = input('Souhaitez-vous jouer à nouveau ? (o/n) :').strip().lower()

            if answer == 'o' or answer == 'n' :
                CORRECT_ANSWER = True
                if answer == 'n' :
                    PLAY = False
            else : 
                print("Répondez par 'o' ou 'n'.")
        