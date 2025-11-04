# Fichier: algorithme_recherche_tabou.py

import random
from collections import deque

# --- Données du Problème (Matrice des Distances) ---
# Matrice représentant les distances entre 10 villes (de 0 à 9).
# matrice_distances[i][j] donne la distance entre la ville i et la ville j.
matrice_distances = [
    [0, 2, 7, 15, 2, 5, 7, 6, 6, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [2, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [7, 10, 4, 2, 0, 7, 3, 2, 2, 7],
    [2, 3, 3, 7, 7, 0, 1, 7, 2, 10],
    [5, 7, 3, 7, 3, 1, 0, 2, 1, 3],
    [7, 7, 4, 7, 2, 7, 2, 0, 1, 10],
    [6, 8, 2, 5, 2, 2, 1, 1, 0, 15],
    [5, 2, 3, 4, 7, 10, 3, 10, 15, 0]
]


# --- Fonctions de l'Algorithme ---

def calculer_distance_totale(solution, matrice_distances):
    """
    Calcule la distance totale d'un parcours (solution).
    Inclut le retour à la ville de départ.
    """
    distance_totale = 0
    # Parcourir la solution pour additionner les distances entre villes consécutives
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]

    # Ajouter la distance pour revenir de la dernière ville à la première
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale


def generer_voisins(solution):
    """
    Génère toutes les solutions voisines en échangeant chaque paire de villes.
    C'est une exploration complète du voisinage de type '2-opt'.
    """
    voisins = []
    # Double boucle pour considérer chaque paire de villes (i, j) une seule fois
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            voisin = solution[:]  # Créer une copie de la solution actuelle
            # Échanger les deux villes pour créer un nouveau voisin
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins


# --- Algorithme Principal : Recherche Tabou ---

def tabu_search(matrice_distances, nombre_iterations, taille_tabu):
    """
    Implémente l'algorithme de Recherche Tabou pour le Problème du Voyageur de Commerce (TSP).
    """
    nombre_villes = len(matrice_distances)

    # 1. Commencer avec une solution aléatoire
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)

    # 2. Initialiser la meilleure solution comme étant la solution de départ
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(meilleure_solution, matrice_distances)

    # 3. Initialiser la liste tabou.
    # deque(maxlen=...) est une file de taille fixe très efficace.
    # Quand un nouvel élément est ajouté et que la file est pleine, l'élément le plus ancien est automatiquement retiré.
    tabu_list = deque(maxlen=taille_tabu)
    tabu_list.append(tuple(solution_actuelle))  # On stocke des tuples car ils sont "hashable" (utilisable dans un set)

    # 4. Boucle principale de l'algorithme
    for _ in range(nombre_iterations):
        # Générer le voisinage de la solution actuelle
        voisins = generer_voisins(solution_actuelle)

        # Filtrer les voisins qui sont dans la liste tabou pour éviter les cycles
        # L'utilisation d'un set pour la recherche est beaucoup plus rapide que de chercher dans une liste.
        voisins = [v for v in voisins if tuple(v) not in tabu_list]

        # S'il n'y a plus de voisins non-tabous, on est potentiellement bloqué.
        if not voisins:
            break

        # 5. Sélectionner le meilleur voisin parmi les non-tabous
        meilleur_voisin = min(voisins, key=lambda v: calculer_distance_totale(v, matrice_distances))

        # 6. Mettre à jour la solution actuelle pour le prochain tour de boucle
        solution_actuelle = meilleur_voisin

        # 7. Ajouter la nouvelle solution (maintenant l'actuelle) à la liste tabou
        tabu_list.append(tuple(solution_actuelle))

        # 8. Mettre à jour la meilleure solution globale si la solution actuelle est meilleure
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)
        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle

    return meilleure_solution, meilleure_distance


# --- Bloc d'Exécution ---

if __name__ == "__main__":
    # Paramètres de l'algorithme
    NOMBRE_ITERATIONS = 1000  # Le nombre de fois où l'on cherche un meilleur voisin
    TAILLE_TABU = 50  # La taille de la mémoire à court terme (nombre de solutions récentes interdites)

    # Lancer l'algorithme
    meilleure_solution, meilleure_distance = tabu_search(
        matrice_distances,
        NOMBRE_ITERATIONS,
        TAILLE_TABU
    )

    # Afficher les résultats
    print(f"Meilleure solution trouvée (Recherche Tabou): {meilleure_solution}")
    print(f"Distance minimale: {meilleure_distance}")