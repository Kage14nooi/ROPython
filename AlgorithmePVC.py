import numpy as np

class LittleAlgorithm:
    def __init__(self, cost_matrix):
        self.cost_matrix = np.array(cost_matrix)
        self.n = len(cost_matrix)
        self.lower_bound = 0
        self.path = []  # Liste des arcs suivis
        self.forbidden_arcs = set()  # Ensemble des arcs interdits (bloqués)

    def reduce_matrix(self, matrix):
        """Bloc 1 : Réduction par ligne et par colonne"""
        print("\n--- Réduction de la matrice ---")
        row_min = np.min(matrix, axis=1)
        row_min[row_min == np.inf] = 0
        matrix -= row_min[:, None]
        self.lower_bound += sum(row_min)
        print(f"  Lignes supprimées : {row_min}")

        col_min = np.min(matrix, axis=0)
        col_min[col_min == np.inf] = 0
        matrix -= col_min
        self.lower_bound += sum(col_min)
        print("Matrice réduite dans reduce  :\n", matrix)
        print("Borne inférieure actuelle :", self.lower_bound)
        return matrix

    def find_zero_with_max_penalty(self, matrix):
        """Bloc 2 : Trouver le zéro avec la pénalité maximale"""
        max_penalty = -1
        best_zero = None

        for i in range(self.n):
            for j in range(self.n):
                if matrix[i, j] == 0 and (i, j) not in self.forbidden_arcs:
                    row_min = np.min(np.delete(matrix[i], j)) if len(matrix[i]) > 1 else 0
                    col_min = np.min(np.delete(matrix[:, j], i)) if len(matrix[:, j]) > 1 else 0
                    penalty = row_min + col_min

                    print(f"  Zéro trouvé à ({i}, {j}) avec pénalité : {penalty} (Ligne min : {row_min}, Colonne min : {col_min})")
                    if penalty > max_penalty:
                        max_penalty = penalty
                        best_zero = (i, j)

        print(f"Zéro avec pénalité max : {best_zero}, pénalité = {max_penalty}")
        return best_zero

    def calculate_b1_b2(self, matrix, i, j):
        """Bloc 3 : Calcul de b1 et b2"""
        b1 = self.lower_bound + self.get_regret(matrix, i, j)
        print(f"Calcul des bornes pour ({i} -> {j}):")
        print(f"  B1 = Borne inférieure actuelle + regret = {self.lower_bound} + {self.get_regret(matrix, i, j)} = {b1}")

        matrix_copy = matrix.copy()
        matrix_copy[i, :] = np.inf  # Supprimer la ligne i
        matrix_copy[:, j] = np.inf  # Supprimer la colonne j
        print(f"  Ligne {i} et colonne {j} supprimées.")

        self.block_parasite_arcs(matrix_copy, i, j)  # Bloquer les arcs parasites

        matrix_reduced = self.reduce_matrix(matrix_copy)
        b2 = self.lower_bound
        print(f"  B2 (borne inférieure après réduction) = {b2}")

        return b1, b2 , matrix_reduced

    def get_regret(self, matrix, i, j):
        """Calcul du regret pour l'arc (i, j)"""
        # Minimum sur la ligne (hors colonne j)
        row_without_j = [matrix[i, k] for k in range(self.n) if k != j]
        row_min = min(row_without_j) if row_without_j else np.inf

        # Minimum sur la colonne (hors ligne i)
        col_without_i = [matrix[k, j] for k in range(self.n) if k != i]
        col_min = min(col_without_i) if col_without_i else np.inf

        return row_min + col_min

    def block_parasite_arcs(self, matrix, i, j):
        """Blocage des arcs parasites pour éviter les boucles"""
        print(f"\n--- Blocage des arcs parasites ---")
        # Vérifier si l'arc inverse existe et doit être bloqué
        if (j, i) not in self.forbidden_arcs:
            matrix[j, i] = np.inf
            print(f"✅ Arc inverse bloqué : ({j} -> {i})")

        # Parcours du chemin actuel pour vérifier les cycles
        for (x, y) in self.path:
            if y == i:  
                print(f"✅ Arc teste : ({y} -> {i})")
                print("teste : ", self.path[0][0])
                matrix[j, self.path[0][0]] = np.inf  # Bloquer l'arc qui fermerait une boucle
                print(f"✅ Arc parasite bloqué : ({self.path[0][0]} -> {j})")

        print("Matrice après blocage des arcs parasites :\n", matrix)

    def solve(self):
        """Résolution complète de l'algorithme de Little"""
        matrix = self.reduce_matrix(self.cost_matrix.copy())
        print("Matrice dans solve  :\n", matrix)
        while len(self.path) < self.n:
            zero = self.find_zero_with_max_penalty(matrix)
            if zero is None:
                break

            i, j = zero
            b1, b2 , matrix_reduced = self.calculate_b1_b2(matrix, i, j)
            print(f" b1 : ({b1} et b2 : {b2}) ")
            print(f"Décision sur l'arc ({i} -> {j}):")
            if b1 < b2:
                print(f"❌ Blocage de l'arc ({i} -> {j}) car b1 ({b1}) est plus optimal.")
                matrix[i, j] = np.inf
                self.forbidden_arcs.add((i, j))
                matrix = self.reduce_matrix(matrix)  # Réduire la matrice après avoir bloqué un arc
                self.lower_bound = b1  # Mise à jour de la borne après blocage
            else:
                print(f"✅ On suit l'arc ({i} -> {j}) car b2 ({b2}) est plus optimal.")
                self.path.append((i, j))
                matrix[i, :] = np.inf  # Supprimer la ligne i
                matrix[:, j] = np.inf  # Supprimer la colonne j
                self.block_parasite_arcs(matrix, i, j)  # Bloquer les arcs parasites
                self.lower_bound = b2  # Mise à jour de la borne après réduction
                print(f"Ambonniny le reduce  b2 ({b2}) djnjdsn.")
                matrix = self.reduce_matrix(matrix_reduced )  # Réduire la matrice après avoir suivi un arc
                print(f"Abaniny le reduce  b2 ({self.lower_bound }) djnjdsn.")

        # Ajout du retour au point de départ
        # self.path.append((self.path[-1][1], self.path[0][0]))  
        print("\n✅ Chemin final :", self.path)
        print("✅ Coût total :", self.lower_bound)
        return self.path, self.lower_bound


# Exemple d'utilisation
cost_matrix = [
    [np.inf, 6, 7, 3, 1, 3],  # A
    [7, np.inf, 8, 2, 9, 7],  # B
    [5, 10, np.inf, 10, 1, 7], # C
    [8, 6, 5, np.inf, 5, 1],  # D
    [7, 7, 6, 7, np.inf, 4],  # E
    [9, 8, 8, 5, 3, np.inf]   # F
]

solver = LittleAlgorithm(cost_matrix)
path, cost = solver.solve()

# Conversion des indices en lettres
cities = ['A', 'B', 'C', 'D', 'E', 'F']
path = [(1, 3), (3, 5), (5, 4), (0, 1), (2, 0), (4, 2)]  # Liste des arcs

# Convertir le chemin en noms de villes
path_named = [(cities[i], cities[j]) for i, j in path]

# Création d'un dictionnaire pour relier chaque ville à sa destination
arc_dict = {arc[0]: arc[1] for arc in path_named}

# Choisir le point de départ : on prend la première ville du premier arc
start_city = path_named[0][0]
ordered_path = [start_city]

# Suivre le cycle jusqu'à revenir au point de départ
current_city = start_city
while True:
    next_city = arc_dict[current_city]
    # Si le prochain est le point de départ, le cycle est complet
    if next_city == start_city:
        break
    ordered_path.append(next_city)
    current_city = next_city

# Affichage des résultats
print("\nArcs suivis :", " | ".join([f"{p[0]} -> {p[1]}" for p in path_named]))
print("Chemin optimal :", " -> ".join(ordered_path))


print("Coût minimum :", cost)
