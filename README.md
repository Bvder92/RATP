# RATP
Ce projet vise à répondre à différentes problématiques de recherche opérationnelle lié au trafic RATP. A l'aide d'un dataset récupéré sur le site OpenData de la RATP, comportant les lignes de métro de 1 à 14 ainsi que le RER A et B, un graphe du trafic ordonné et prenant en compte les connexions et correspondances a été généré.
Il vous faut d'une part installer les dépendances et bibliothèques : 
```
pip install -requirements.txt
```
1) Afficher le graphe des stations
```
python3.11 RO.py -graphe  
```
2) Comment bloquer le trafic en bloquant un nombre minimum de stations ? (Première approche : Ford-Fulkerson)
```
python3.11 RO.py -bloquertrafic
```
3) Comment bloquer le trafic en bloquant un nombre minimum de stations ? (Deuxième approche : Degrés Maximal)
```
python3.11 RO.py -bloquertrafic2
```
4) Quelles sont les stations congestionnées et mesurer l'impact de la suppression de ces stations. (On calculer la longueur moyenne des plus courts chemin avant et après suppression)
```
python3.11 RO.py -congestionpath
```
5)Le plus court chemin pour qu'un touriste puisse visiter l'ensemble des monuments incontournables de Paris 
```
python3.11 RO.py -touriste
```
