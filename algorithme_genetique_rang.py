# Fichier: algorithme_genetique_rang.py

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
        ville_arrivee = solution[(i + 1) % len(solution)]
        distance += matrice[ville_depart][ville_arrivee]
    return distance


def calculer_fitness(solution, matrice):
    """
    Calcule la fitness (qualité) d'une solution.
    Pour un problème de minimisation, la fitness est l'inverse de la distance.
    """
    distance = calculer_distance_totale(solution, matrice)
    if distance == 0:
        return float('inf')
    return 1.0 / distance


# --- Opérateurs Génétiques ---

def selection_parents_rang(population, fitnesses):
    """
    Sélectionne deux parents en utilisant la méthode de sélection par rang.
    Cette méthode évite qu'un seul "super" individu domine la sélection.
    """
    # 1. Associer chaque individu à sa fitness et trier du moins bon au meilleur
    population_triee = sorted(zip(population, fitnesses), key=operator.itemgetter(1))

    # 2. Les rangs vont de 1 (pour le moins bon) à N (pour le meilleur)
    rangs = range(1, len(population) + 1)
    total_rangs = sum(rangs)

    parents = []
    # 3. Effectuer une sélection de type roulette, mais sur les RANGS, pas sur la fitness
    for _ in range(2):  # Sélectionner deux parents
        selection = random.uniform(0, total_rangs)
        somme_actuelle = 0
        for i, rang in enumerate(rangs):
            somme_actuelle += rang
            if somme_actuelle >= selection:
                # L'individu sélectionné correspond à l'indice 'i' dans la population triée
                parents.append(population_triee[i][0])
                break
    return parents[0], parents[1]


def croisement(parent1, parent2):
    """
    Effectue un croisement de type Ordered Crossover (OX1).
    """
    taille = len(parent1)
    enfant = [None] * taille
    debut, fin = sorted(random.sample(range(taille), 2))
    segment_parent1 = parent1[debut:fin + 1]
    enfant[debut:fin + 1] = segment_parent1

    index_parent2 = 0
    index_enfant = 0
    while None in enfant:
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
    """
    solution_mutee = solution[:]
    for i in range(len(solution_mutee)):
        if random.random() < taux_mutation:
            j = random.randint(0, len(solution_mutee) - 1)
            solution_mutee[i], solution_mutee[j] = solution_mutee[j], solution_mutee[i]
    return solution_mutee


# --- Algorithme Génétique Principal ---

def algorithme_genetique(matrice, taille_population, nombre_generations, taux_croisement, taux_mutation, taille_elite):
    """
    Implémentation complète de l'algorithme génétique pour le TSP.
    """
    nombre_villes = len(matrice)
    population = [random.sample(range(nombre_villes), nombre_villes) for _ in range(taille_population)]
    meilleure_solution_globale = None
    meilleure_distance_globale = float('inf')

    for generation in range(nombre_generations):
        fitnesses = [calculer_fitness(ind, matrice) for ind in population]

        max_fitness_gen = max(fitnesses)
        index_meilleur_gen = fitnesses.index(max_fitness_gen)
        distance_generation = calculer_distance_totale(population[index_meilleur_gen], matrice)

        if distance_generation < meilleure_distance_globale:
            meilleure_solution_globale = population[index_meilleur_gen]
            meilleure_distance_globale = distance_generation

        nouvelle_population = []

        population_avec_fitness = sorted(zip(population, fitnesses), key=operator.itemgetter(1), reverse=True)
        elite = [individu for individu, fitness in population_avec_fitness[:taille_elite]]
        nouvelle_population.extend(elite)

        while len(nouvelle_population) < taille_population:
            # La seule différence est l'appel à cette fonction de sélection
            parent1, parent2 = selection_parents_rang(population, fitnesses)

            enfant = croisement(parent1, parent2) if random.random() < taux_croisement else parent1[:]

            enfant_mute = mutation(enfant, taux_mutation)

            nouvelle_population.append(enfant_mute)

        population = nouvelle_population

    return meilleure_solution_globale, meilleure_distance_globale


# --- Bloc d'Exécution ---
if __name__ == "__main__":
    # Hyperparamètres de l'algorithme génétique
    TAILLE_POPULATION = 100
    NOMBRE_GENERATIONS = 500
    TAUX_CROISEMENT = 0.8
    TAUX_MUTATION = 0.02
    TAILLE_ELITE = 5

    print("--- Lancement avec la Sélection par Rang ---")

    # Lancer l'algorithme
    solution_finale, distance_finale = algorithme_genetique(
        matrice_distances, TAILLE_POPULATION, NOMBRE_GENERATIONS, TAUX_CROISEMENT, TAUX_MUTATION, TAILLE_ELITE
    )

    # Afficher les résultats
    print(f"Meilleure solution trouvée (Rang): {solution_finale}")
    print(f"Distance minimale: {distance_finale}")