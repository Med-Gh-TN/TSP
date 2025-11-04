# Fichier: algorithme_genetique_roulette.py

import random
import operator  # Utilisé pour trier facilement la population

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


# --- Fonctions Auxiliaires ---

def calculer_distance_totale(solution, matrice):
    """
    Calcule la distance totale d'un parcours (solution).
    Inclut le retour à la ville de départ.
    """
    distance = 0
    for i in range(len(solution)):
        ville_depart = solution[i]
        # La ville d'arrivée est la suivante dans la liste, ou la première si on est à la fin (boucle)
        ville_arrivee = solution[(i + 1) % len(solution)]
        distance += matrice[ville_depart][ville_arrivee]
    return distance


def calculer_fitness(solution, matrice):
    """
    Calcule la fitness (qualité) d'une solution.
    Pour un problème de minimisation (trouver le plus court chemin),
    la fitness est l'inverse de la distance. Une plus petite distance donne une plus grande fitness.
    """
    distance = calculer_distance_totale(solution, matrice)
    # On évite la division par zéro, bien que peu probable pour un parcours valide
    if distance == 0:
        return float('inf')
    return 1.0 / distance


# --- Opérateurs Génétiques ---

def selection_parents_roulette(population, fitnesses):
    """
    Sélectionne deux parents en utilisant la méthode de la roue de loterie (Roulette Wheel).
    Les individus avec une meilleure fitness ont une plus grande probabilité d'être sélectionnés.
    """
    total_fitness = sum(fitnesses)
    parents = []

    # On effectue deux tours de roue pour sélectionner deux parents
    for _ in range(2):
        # On 'lance la bille' sur la roue en choisissant un nombre aléatoire entre 0 et la fitness totale
        selection = random.uniform(0, total_fitness)
        somme_actuelle = 0

        # Gérer le cas où total_fitness est 0 pour éviter une boucle infinie
        if total_fitness == 0:
            parents.append(random.choice(population))
            continue

        # On parcourt la roue pour voir où la bille s'arrête
        for i, fitness_ind in enumerate(fitnesses):
            somme_actuelle += fitness_ind
            if somme_actuelle >= selection:
                parents.append(population[i])
                break  # Le parent est sélectionné, on sort de la boucle
    return parents[0], parents[1]


def croisement(parent1, parent2):
    """
    Effectue un croisement de type Ordered Crossover (OX1), adapté aux problèmes de permutation.
    Ceci garantit que l'enfant est un parcours valide (chaque ville visitée une seule fois).
    """
    taille = len(parent1)
    enfant = [None] * taille

    # 1. Choisir une sous-séquence aléatoire du parent1
    debut, fin = sorted(random.sample(range(taille), 2))

    # 2. Copier cette sous-séquence dans l'enfant aux mêmes positions
    segment_parent1 = parent1[debut:fin + 1]
    enfant[debut:fin + 1] = segment_parent1

    # 3. Remplir les positions restantes de l'enfant avec les gènes du parent2,
    # dans l'ordre où ils apparaissent, en évitant les doublons.
    index_parent2 = 0
    index_enfant = 0
    while None in enfant:
        # Si on est dans la section déjà remplie, on saute
        if index_enfant >= debut and index_enfant <= fin:
            index_enfant += 1
            continue

        ville_parent2 = parent2[index_parent2]
        if ville_parent2 not in segment_parent1:
            enfant[index_enfant] = ville_parent2
            index_enfant += 1
        index_parent2 += 1

    return enfant


def mutation(solution, taux_mutation):
    """
    Effectue une mutation par échange (Swap Mutation).
    Pour chaque gène de la solution, il y a une petite chance qu'il soit échangé avec un autre.
    """
    solution_mutee = solution[:]  # Créer une copie
    for i in range(len(solution_mutee)):
        if random.random() < taux_mutation:
            # Échanger la ville 'i' avec une autre ville 'j' choisie au hasard
            j = random.randint(0, len(solution_mutee) - 1)
            solution_mutee[i], solution_mutee[j] = solution_mutee[j], solution_mutee[i]
    return solution_mutee


# --- Algorithme Génétique Principal ---

def algorithme_genetique(matrice, taille_population, nombre_generations, taux_croisement, taux_mutation, taille_elite):
    """
    Implémentation complète de l'algorithme génétique pour le TSP.
    """
    nombre_villes = len(matrice)

    # 1. Création de la population initiale de solutions aléatoires
    population = [random.sample(range(nombre_villes), nombre_villes) for _ in range(taille_population)]

    meilleure_solution_globale = None
    meilleure_distance_globale = float('inf')

    # 2. Boucle principale sur les générations
    for generation in range(nombre_generations):
        # 3. Évaluation de chaque individu de la population
        fitnesses = [calculer_fitness(ind, matrice) for ind in population]

        # Mettre à jour la meilleure solution trouvée jusqu'à présent
        max_fitness_gen = max(fitnesses)
        index_meilleur_gen = fitnesses.index(max_fitness_gen)
        distance_generation = calculer_distance_totale(population[index_meilleur_gen], matrice)

        if distance_generation < meilleure_distance_globale:
            meilleure_solution_globale = population[index_meilleur_gen]
            meilleure_distance_globale = distance_generation

        # 4. Création de la nouvelle génération
        nouvelle_population = []

        # 5. Élitism: Conserver les meilleurs individus de la génération actuelle
        # On trie la population par fitness décroissante et on garde les 'taille_elite' meilleurs
        population_avec_fitness = sorted(zip(population, fitnesses), key=operator.itemgetter(1), reverse=True)
        elite = [individu for individu, fitness in population_avec_fitness[:taille_elite]]
        nouvelle_population.extend(elite)

        # 6. Remplir le reste de la nouvelle population par croisement et mutation
        while len(nouvelle_population) < taille_population:
            parent1, parent2 = selection_parents_roulette(population, fitnesses)

            enfant = croisement(parent1, parent2) if random.random() < taux_croisement else parent1[:]

            enfant_mute = mutation(enfant, taux_mutation)

            nouvelle_population.append(enfant_mute)

        # 7. Remplacer l'ancienne population par la nouvelle
        population = nouvelle_population

    return meilleure_solution_globale, meilleure_distance_globale


# --- Bloc d'Exécution ---
if __name__ == "__main__":
    # Hyperparamètres de l'algorithme génétique
    TAILLE_POPULATION = 100  # Nombre d'individus dans chaque génération
    NOMBRE_GENERATIONS = 500  # Nombre de cycles d'évolution
    TAUX_CROISEMENT = 0.8  # Probabilité que deux parents se croisent (80%)
    TAUX_MUTATION = 0.02  # Probabilité de mutation pour un gène (2%)
    TAILLE_ELITE = 5  # Nombre de meilleurs individus à conserver directement

    print("--- Lancement avec la Sélection par Roulette ---")

    # Lancer l'algorithme
    solution_finale, distance_finale = algorithme_genetique(
        matrice_distances, TAILLE_POPULATION, NOMBRE_GENERATIONS, TAUX_CROISEMENT, TAUX_MUTATION, TAILLE_ELITE
    )

    # Afficher les résultats
    print(f"Meilleure solution trouvée (Roulette): {solution_finale}")
    print(f"Distance minimale: {distance_finale}")