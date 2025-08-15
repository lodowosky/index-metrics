import pandas as pd
import numpy as np

#input
summary = pd.read_csv(
    "summary.csv",
    index_col=0,
    usecols=range(7)  # legge solo le prime 4 colonne (indice 0,1,2,3)
) #questo è importante se hai già calcolato la correlazione, dato che alla fine il codice fa un merge

cumulative_returns_outer = pd.read_csv('cumulative_returns_outer.txt', index_col=0)

correlation_matrix = cumulative_returns_outer.corr().round(2)

# Stampo la matrice di correlazione
print("Matrice di correlazione tra i rendimenti:")
correlation_matrix.index.name = "Name"  # Nome per la "prima colonna"

summary = pd.merge(summary, correlation_matrix, on = 'Name')
summary.to_csv("summary.csv")
print("\nFile aggiornato, ti mostro summary.csv, ho aggiunto un po' di informazioni utili:\n")
print(summary)