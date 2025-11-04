# Fichier: algorithme_recuit_simulé.py


import random
import math

# --- Données du Problème (Matrice des Distances) ---
# Matrice représentant les distances entre 10 villes (de 0 à 9)
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


# --- Fonctions Auxiliaires ---

def calculer_distance_totale(solution, matrice):
    """
    Calcule la distance totale d'un parcours (solution).
    Inclut le retour à la ville de départ.
    """
    distance_totale = 0
    nombre_villes = len(solution)
    for i in range(nombre_villes - 1):
        ville_actuelle = solution[i]
        ville_suivante = solution[i + 1]
        distance_totale += matrice[ville_actuelle][ville_suivante]

    # Ajouter la distance pour revenir au point de départ
    distance_totale += matrice[solution[-1]][solution[0]]
    return distance_totale


def generer_voisin(solution):
    """
    Génère une solution voisine en échangeant deux villes au hasard.
    """
    voisin = solution[:]  # Créer une copie de la solution

    # Sélectionner deux indices distincts au hasard
    indices = random.sample(range(len(voisin)), 2)
    idx1, idx2 = indices[0], indices[1]

    # Échanger les villes à ces indices
    voisin[idx1], voisin[idx2] = voisin[idx2], voisin[idx1]
    return voisin


# --- Algorithme Principal : Recuit Simulé ---

def recuit_simule(matrice, temperature_initiale, taux_refroidissement, iterations_max):
    """
    Implémente l'algorithme du recuit simulé pour résoudre le problème du voyageur de commerce.
    """
    nombre_villes = len(matrice)

    # 1. Générer une solution initiale aléatoire
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)

    # 2. Initialiser la meilleure solution trouvée
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(meilleure_solution, matrice)

    # 3. Initialiser la température
    temperature = temperature_initiale

    # 4. Boucle principale de l'algorithme
    for i in range(iterations_max):
        # Générer un voisin
        voisin = generer_voisin(solution_actuelle)

        # Calculer les "énergies" (distances)
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice)
        distance_voisin = calculer_distance_totale(voisin, matrice)

        # Calculer la différence d'énergie
        delta_energie = distance_voisin - distance_actuelle

        # 5. Critère d'acceptation
        # Si le voisin est meilleur, on l'accepte toujours
        if delta_energie < 0:
            solution_actuelle = voisin[:]
        # Si le voisin est moins bon, on l'accepte avec une certaine probabilité
        else:
            probabilite_acceptation = math.exp(-delta_energie / temperature)
            if random.random() < probabilite_acceptation:
                solution_actuelle = voisin[:]

        # Mettre à jour la meilleure solution si nécessaire
        distance_courante_mise_a_jour = calculer_distance_totale(solution_actuelle, matrice)
        if distance_courante_mise_a_jour < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_courante_mise_a_jour

        # 6. Refroidir la température
        temperature *= taux_refroidissement

    return meilleure_solution, meilleure_distance


# --- Bloc d'Exécution ---

if __name__ == "__main__":
    # Paramètres de l'algorithme
    TEMPERATURE_INITIALE = 10000
    TAUX_REFROIDISSEMENT = 0.9995  # Un refroidissement lent est souvent meilleur
    ITERATIONS_MAX = 100000

    # Lancer l'algorithme
    solution_finale, distance_finale = recuit_simule(
        matrice_distances,
        TEMPERATURE_INITIALE,
        TAUX_REFROIDISSEMENT,
        ITERATIONS_MAX
    )

    # Afficher les résultats
    print(f"Meilleure solution trouvée (Recuit Simulé): {solution_finale}")
    print(f"Distance minimale: {distance_finale}")