#questo programma accede ai dati e chiama simulate.py per ogni serie
import pandas as pd
import os

#accedo ai file che mi servono
summary = pd.read_csv('summary.csv', index_col=0) 
daily_returns_outer = pd.read_csv('daily_returns_outer.txt', index_col=0)
daily_returns_inner = daily_returns_outer.dropna() #trasformo outer in un inner (intersezione dei dati)

serie = daily_returns_inner['GOLD']
#print(serie)
print(daily_returns_inner)