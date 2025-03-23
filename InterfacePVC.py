import tkinter as tk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from AlgorithmePVC import LittleAlgorithm

class PVCInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Problème du Voyageur de Commerce")
        self.root.geometry("800x600")  # Taille plus grande pour mieux afficher le graphique
        
        # Création des widgets
        tk.Label(root, text="Matrice de coût (séparée par des espaces et des retours à la ligne)", 
                wraplength=500).pack(pady=10)
        
        self.text_input = tk.Text(root, height=15, width=60, font=('Courier', 10))
        self.text_input.pack(pady=10)
        
        self.solve_button = tk.Button(root, text="Résoudre", command=self.solve_pvc)
        self.solve_button.pack(pady=10)
        
        self.result_label = tk.Label(root, text="Résultat :", wraplength=500)
        self.result_label.pack(pady=10)
        
        # Ajout d'un exemple dans le champ de texte
        example = """0 6 7 3 1 3
                    7 0 8 2 9 7
                    5 10 0 10 1 7
                    8 6 5 0 5 1
                    7 7 6 7 0 4
                    9 8 8 5 3 0"""
        self.text_input.insert('1.0', example)

    def solve_pvc(self):
        try:
            input_text = self.text_input.get("1.0", tk.END).strip()
            # Validation du format de la matrice
            lines = input_text.split('\n')
            if not all(lines):
                raise ValueError("La matrice ne peut pas être vide")
                
            # Conversion en liste de listes
            cost_matrix = []
            for line in lines:
                numbers = list(map(float, line.split()))
                if not numbers:
                    continue
                cost_matrix.append(numbers)
            
            # Validation de la matrice carrée
            size = len(cost_matrix)
            if not all(len(row) == size for row in cost_matrix):
                raise ValueError("La matrice doit être carrée")
            
            # Remplacement des zéros par des valeurs infinies sur la diagonale
            for i in range(size):
                cost_matrix[i][i] = np.inf
            
            solver = LittleAlgorithm(cost_matrix)
            path, cost = solver.solve()
            
            # Conversion des indices en lettres
            cities = [chr(65 + i) for i in range(len(cost_matrix))]
            path_named = [(cities[i], cities[j]) for i, j in path]
            
            # Création du chemin complet
            cities = ['A', 'B', 'C', 'D', 'E', 'F']
            # path = [(1, 3), (3, 5), (5, 4), (0, 1), (2, 0), (4, 2)]  # Liste des arcs

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
            result_text = " -> ".join(ordered_path)
            self.result_label.config(text=f"Chemin optimal : {result_text}\nCoût minimum : {cost}")
            
            self.draw_graph(path_named)
            
        except ValueError as e:
            messagebox.showerror("Erreur", f"Format incorrect de la matrice : {str(e)}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
            print(f"Erreur technique : {str(e)}")

    def draw_graph(self, path):
        G = nx.DiGraph()
        G.add_edges_from(path)
        
        # Création d'une nouvelle fenêtre pour le graphique
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Solution du PVC")
        graph_window.geometry("600x500")
        
        # Création du canvas pour matplotlib
        fig, ax = plt.subplots(figsize=(8, 8))
        pos = nx.spring_layout(G)
        
        # Dessin du graphe
        nx.draw(G, pos, ax=ax, with_labels=True, 
                node_color='red', 
                edge_color='black', 
                node_size=2000, 
                font_size=12,
                font_weight='bold')
        
        # Ajout des étiquettes sur les arêtes
        edge_labels = {(u, v): f"{u}->{v}" for u, v in path}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
        plt.title("Chemin optimal du PVC")
        plt.axis('off')
        
        # Affichage dans la nouvelle fenêtre
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = PVCInterface(root)
    root.mainloop()