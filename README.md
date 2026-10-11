# Tic-tac-toe — Q-learning en Python

Ce projet propose un jeu de tic-tac-toe dans le terminal, avec un adversaire aléatoire et un agent entraîné par Q-learning tabulaire.

L'exercice laissait le choix de l'approche pour développer le jeu. J'ai commencé par les règles du jeu, puis ajouté un adversaire aléatoire, avant de développer un agent qui apprend en jouant. Le projet utilise une table Q, sans réseau de neurones.

## Fonctionnalités

- Grille de 3 × 3 cases.
- Vérification des coordonnées saisies et refus des cases occupées.
- Détection des victoires par ligne, colonne ou diagonale et des matchs nuls.
- Jeu contre un agent entraîné, avec possibilité de rejouer.
- Entraînement contre un adversaire aléatoire.
- Sauvegarde et chargement de la table Q.
- Évaluation automatique avec une barre de progression.

## Fichiers

Les commandes ci-dessous utilisent les noms actuels des scripts, avec l'extension `.py`.

| Fichier | Description |
|---|---|
| `tic-tac-toe.py` | Version initiale du jeu 2 joueurs. |
| `naive_tic_tac_toe.py` | Version utilisant un ordinateur aléatoire. |
| `training_Agent_Q_tic_tac_toe.py` | Entraînement de l'agent Q-learning. |
| `naive_vs_Agent_Q.py` | Évaluation de l'agent contre un joueur aléatoire. |
| `tic_tac_toe_play_against_Agent_Q.py` | Jeu humain contre l'agent entraîné. |
| `Q_table.pkl` | Table Q sauvegardée après l'entraînement. |

## Installation

Python 3 et les bibliothèques NumPy et tqdm sont nécessaires.

```bash
python -m pip install requirements.txt
```

Exécuter les commandes suivantes depuis le dossier du projet.

## Jouer contre l'agent

Placer `Q_table.pkl` dans le même dossier que le script de jeu.

```bash
python tic_tac_toe_play_against_Agent_Q.py
```

Aucune interface graphique n'a été faite.
Le joueur humain commence et utilise le symbole `1`. L'ordinateur utilise le symbole `2`. Les cases vides sont représentées par `0`.

Pour jouer, saisir une ligne et une colonne entre 1 et 3, séparées par un espace, une virgule ou un point-virgule. Par exemple, `2 3` désigne la deuxième ligne et la troisième colonne.

À la fin d'une partie, répondre `o` pour rejouer ou `n` pour quitter.

## Entraîner l'agent

```bash
python training_Agent_Q_tic_tac_toe.py
```

Le joueur 1 choisit une case libre au hasard. Le joueur 2 apprend grâce aux résultats des parties. Le script initialise une nouvelle table Q : relancer l'entraînement recommence l'apprentissage et peut remplacer le fichier sauvegardé.

Paramètres utilisés pour l'entraînement présenté ici :

| Paramètre | Valeur |
|---|---:|
| Nombre de parties | 500 000 |
| Probabilité d'exploration | 0,2 |
| Taux d'apprentissage | 0,2 |
| Facteur d'actualisation | 0,9 |

Les résultats sont affichés par blocs de 1 000 parties. La table est sauvegardée dans `Q_table.pkl`. Avec la sauvegarde relative utilisée dans cette version, le fichier est créé dans le répertoire de travail courant.

## Principe du Q-learning

Un état correspond à une configuration de la grille. Les neuf valeurs de la grille sont converties en une chaîne utilisée comme clé d'un dictionnaire. Chaque état rencontré est associé à un tableau NumPy de 3 × 3 valeurs Q : une valeur par case où jouer.

Les valeurs Q estiment l'intérêt des actions en termes de récompenses futures. Elles sont initialisées à zéro. Les cases occupées sont exclues du choix des actions et du calcul de la meilleure valeur future.

Pendant l'entraînement, l'agent choisit une action aléatoire avec une probabilité de 0,2. Sinon, il choisit une case libre ayant la valeur Q maximale. Les égalités sont départagées au hasard.

Les récompenses sont définies du point de vue du joueur 2 :

| Résultat | Récompense |
|---|---:|
| Victoire de l'agent | +1 |
| Défaite de l'agent | −1 |
| Match nul | 0 |
| Partie encore en cours | 0 |

Une transition comprend le coup de l'agent et la réponse de l'adversaire, sauf si le coup de l'agent termine immédiatement la partie. Chaque coup de l'agent est mis à jour une seule fois.

Pour une transition non terminale, la règle utilisée est :

```text
Q(s, a) ← Q(s, a) + lr × [r + gamma × max Q(s', a') − Q(s, a)]
```

Le maximum porte uniquement sur les actions autorisées dans l'état suivant. Lorsque la partie est terminée, la cible est la récompense seule :

```text
Q(s, a) ← Q(s, a) + lr × [r − Q(s, a)]
```

## Évaluer l'agent

```bash
python naive_vs_Agent_Q.py
```

L'évaluation charge la table sauvegardée et lance 20 000 parties contre un adversaire aléatoire. L'agent joue en deuxième, sans exploration et sans modification de Q. Si un état est absent de la table, il choisit une case libre au hasard.

Résultats obtenus lors d'une exécution :

| Résultat de l'agent | Nombre de parties | Pourcentage |
|---|---:|---:|
| Victoires | 18 593 | 93,0 % |
| Défaites | 248 | 1,2 % |
| Matchs nuls | 1 159 | 5,8 % |
| Total | 20 000 | 100 % |

Les résultats peuvent varier entre les exécutions, car l'adversaire, le départage des égalités et le choix dans les états inconnus sont aléatoires.

## Limites et améliorations possibles

L'agent a été entraîné pour jouer en deuxième contre un adversaire aléatoire. Les résultats ci-dessus ne garantissent pas les mêmes performances contre un joueur humain ou un adversaire utilisant une stratégie différente. Il n'est pas imbattable.

Des améliorations possibles sont de tester plusieurs entraînements avec des graines aléatoires fixées, de varier les adversaires, de regrouper les fonctions communes aux scripts et d'améliorer l'affichage de la grille.

## Auteur

David Minloubou
