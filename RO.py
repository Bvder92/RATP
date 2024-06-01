import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import random
from itertools import permutations

# Charger les données
feuille1 = pd.read_csv("trafic2021.csv", delimiter=';')
ordre_stations = pd.read_csv("ordre.csv", delimiter=';', usecols=lambda column: column != 'RANG')

feuille1['Latitude'] = feuille1['Latitude'].astype(float)
feuille1['Longitude'] = feuille1['Longitude'].astype(float)

# Initialiser le graphe
G = nx.Graph()

couleurs_lignes = {
    'A': 'red',
    'A.1': 'red',
    'B': 'blue',
    'B.1': 'blue',
    '1': 'gold',
    '2': 'mediumblue',
    '3': 'olive',
    '3BIS': 'paleTurquoise',
    '4': 'purple',
    '5': 'orangered',
    '6': 'palegreen',
    '7': 'pink',
    '7.1': 'pink',
    '7BIS': 'palegreen',
    '8': 'thistle',
    '9': 'olivedrab',
    '10': 'sandybrown',
    '11': 'saddlebrown',
    '12': 'seagreen',
    '13': 'paleTurquoise',
    '13.1': 'paleTurquoise',
    '14': 'indigo'
}

# Ajoute les arêtes et définit les couleurs
for ligne, stations in ordre_stations.items():
    #if ligne == '1':#or ligne == '13.1' : 
    for i in range(len(stations) - 1):
        station_depart = stations[i]
        station_arrivee = stations[i + 1] 
        if isinstance(station_arrivee, float):
            break
        G.add_edge(station_depart, station_arrivee, color=couleurs_lignes[ligne])

pos = {}
for station in G.nodes():
    if station in feuille1['Station'].values:
        longitude = feuille1.loc[feuille1['Station'] == station, 'Longitude'].iloc[0]
        latitude = feuille1.loc[feuille1['Station'] == station, 'Latitude'].iloc[0]
        pos[station] = (float(longitude), float(latitude))

# Parsing des arguments
parser = argparse.ArgumentParser(description='Analyse du réseau RATP')
parser.add_argument('-graphe', action='store_true', help='Affiche le graphe du trafic RATP')
parser.add_argument('-bloquertrafic', action='store_true', help='Bloquer le trafic en bloquant le nombre minimum de stations, premiere approche')
parser.add_argument('-bloquertrafic2', action='store_true', help='Bloquer le trafic en bloquant le nombre minimum de stations, deuxieme approche')
parser.add_argument('-touriste', action='store_true', help='Trouver le plus court chemin pour les monuments touristiques')
parser.add_argument('-congestionpath', action='store_true', help='Identifier les stations congestionnées et la moyenne des plus courts chemins')
args = parser.parse_args()

def afficher_graphe(G):
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, edge_color=[G[u][v]['color'] for u, v in G.edges], node_size=5,with_labels=False-)
    plt.title("Graphe du trafic RATP")
    plt.show()

def bloquer_trafic(G):
    from networkx.algorithms.connectivity import minimum_node_cut

    # Calculate the minimum vertex cut
    min_cut = minimum_node_cut(G)
    min_cut_list = list(min_cut)

    # Affichage des résultats
    print("Stations à bloquer:", min_cut_list)
    print("Nombre de stations à bloquer:", len(min_cut_list))

    # Visualisation
    node_colors = ['red' if node in min_cut_list else 'black' for node in G.nodes]
    node_size = [10 if node in min_cut_list else 5 for node in G.nodes]
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, edge_color=[G[u][v]['color'] for u, v in G.edges], node_size=node_size, node_color = node_colors,with_labels=False, font_size=8)
    plt.title("Stations critiques pour bloquer le trafic")
    plt.show()

def bloquer_trafic2(G):

    station_degrees = dict(G.degree())

    sorted_stations = sorted(station_degrees, key=station_degrees.get, reverse=True)

    top_critical_stations = sorted_stations[:10]
    print("Top critical stations:", top_critical_stations)
    print("Number of top critical stations:", len(top_critical_stations))
     # Visualisation
    node_colors = ['red' if node in top_critical_stations else 'black' for node in G.nodes]
    node_size = [10 if node in top_critical_stations else 5 for node in G.nodes]
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, edge_color=[G[u][v]['color'] for u, v in G.edges], node_size=node_size, node_color = node_colors ,with_labels=False, font_size=8)
    plt.title("Stations critiques pour bloquer le trafic")
    plt.show()





def chemin_touristique(G):
    
    monuments = {
        "Tour Eiffel": "TROCADERO",
        "Louvre": "LOUVRE",
        "Arc de Triomphe": "CHARLES DE GAULLE-ETOILE-RER",
        "Grand Palais": "FRANKLIN D. ROOSEVELT",
        "Opéra Garnier": "OPERA",
        "Notre Dame de Paris": "SAINT-MICHEL-NOTRE-DAME",
        "Invalides": "INVALIDES"
    }

    def find_shortest_path(G, monuments, start_station):
        shortest_path = None
        min_path_length = float('inf')
        best_perm = None

        for perm in permutations(monuments.values()):
            if perm[0] != start_station:
                continue
            path_length = 0
            full_path = []
            for i in range(len(perm) - 1):
                segment_path = nx.shortest_path(G, source=perm[i], target=perm[i+1])
                path_length += len(segment_path) - 1
                full_path.extend(segment_path[:-1])
            full_path.append(perm[-1])

            if path_length < min_path_length:
                min_path_length = path_length
                shortest_path = full_path
                best_perm = perm

        return shortest_path, min_path_length, best_perm

    start_station = random.choice(list(monuments.values()))
    shortest_path, min_path_length, best_perm = find_shortest_path(G, monuments, start_station)
    print("Starting station:", start_station)
    shortest_path_with_lines = [(station, ', '.join(G.nodes[station].get('line', ["Unknown"]))) for station in shortest_path]
    print("Shortest path with lines:")
    for station, lines in shortest_path_with_lines:
        print(f"{station} (Lignes {lines})")
    print("Number of stations in shortest path:", min_path_length)

    edge_list = [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path) - 1)]
    node_sizes = [10 if node in shortest_path  else 5 for node in G.nodes ]
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, node_size=node_sizes, with_labels=False, font_size=8)
    nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='red', width=2)
    plt.title("Chemin touristique le plus court")
    plt.show()


def congestion_path(G):
    degree_dict = dict(G.degree(G.nodes))
    max_degree = max(degree_dict.values())
    congested_stations = [station for station, degree in degree_dict.items() if degree == max_degree]
    print(f"Stations les plus congestionnées (degré = {max_degree}): {congested_stations}")

    def average_shortest_path_length(G):
        try:
            return nx.average_shortest_path_length(G)
        except nx.NetworkXError:
            return float('inf')

    original_avg_path_length = average_shortest_path_length(G)
    print(f"Longueur moyenne des plus courts chemins avant suppression: {original_avg_path_length}")

    G_removed = G.copy()
    G_removed.remove_nodes_from(congested_stations)
    connected_components = list(nx.connected_components(G_removed))

    avg_path_lengths = []
    for component in connected_components:
        subgraph = G_removed.subgraph(component)
        if len(subgraph) > 1:
            avg_path_lengths.append(nx.average_shortest_path_length(subgraph))

    if avg_path_lengths:
        new_avg_path_length = sum(avg_path_lengths) / len(avg_path_lengths)
    else:
        new_avg_path_length = float('inf')

    print(f"Longueur moyenne des plus courts chemins après suppression: {new_avg_path_length}")

    # Position des nœuds
    pos = {}
    for station in G.nodes():
        if station in feuille1['Station'].values:
            longitude = feuille1.loc[feuille1['Station'] == station, 'Longitude'].iloc[0]
            latitude = feuille1.loc[feuille1['Station'] == station, 'Latitude'].iloc[0]
            pos[station] = (float(longitude), float(latitude))

    # Graphe complet avec les stations congestionnées en rouge
    plt.figure(figsize=(10, 10))
    node_colors = ['red' if node in congested_stations else 'black' for node in G.nodes]
    nx.draw(G, pos, edge_color=[G[u][v]['color'] for u, v in G.edges], node_size=10, node_color=node_colors, with_labels=False)
    plt.title("Graphe complet avec les stations congestionnées en rouge")
    plt.show()

    # Visualisation des sous-graphes sans les stations congestionnées
    plt.figure(figsize=(10, 10))
    color_map = plt.cm.get_cmap('hsv', len(connected_components))

    for i, component in enumerate(connected_components):
        nx.draw_networkx_nodes(G_removed, pos, nodelist=component, node_color=[color_map(i / len(connected_components))], node_size=10)
    nx.draw_networkx_edges(G_removed, pos, edgelist=G_removed.edges, edge_color=[G_removed[u][v]['color'] for u, v in G_removed.edges], width=1)

    plt.title("Sous-graphes après suppression des stations congestionnées")
    plt.show()

# Exécuter la fonction appropriée en fonction des arguments
if args.graphe:
    afficher_graphe(G)
elif args.bloquertrafic:
    bloquer_trafic(G)
elif args.touriste:
    chemin_touristique(G)
elif args.congestionpath:
    congestion_path(G)
elif args.bloquertrafic2:
    bloquer_trafic2(G)
else :
    print("Choisir un argument pour l'exécution du code.")
    print("-graphe : affiche le graphe du trafic ratp")
    print("-bloquertrafic : Bloquer un nombre de stations minimum pour bloquer l'ensemble du trafic, Flot Maximum - Coupe Minimale")
    print("-bloquertrafic2: Bloquer un nombre de stations minimum pour bloquer l'ensemble du trafic, degrés des stations")
    print("-touriste : propose un plus court chemin afin de visiter les différents grands monuments parisiens")
    print("-congestionpath : trouve les stations les plus congestionnées et calcule la moyenne des plus courts chemins avant et après leur suppression.")
