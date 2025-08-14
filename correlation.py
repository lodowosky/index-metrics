import pandas as pd
import numpy as np

#input
summary = pd.read_csv('summary.csv', index_col=0) 
cumulative_returns_outer = pd.read_csv('cumulative_returns_outer.txt', index_col=0)


correlation_matrix = cumulative_returns_outer.corr()

# Stampo la matrice di correlazione
print("Matrice di correlazione tra i rendimenti:")
print(correlation_matrix)