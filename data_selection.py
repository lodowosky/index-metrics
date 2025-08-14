import pandas as pd
import os

#accedo ai file che mi servono
summary = pd.read_csv('summary.csv', index_col=0) 
daily_returns_inner = pd.read_csv('daily_returns_inner.txt', index_col=0)
daily_returns_outer = pd.read_csv('daily_returns_outer.txt', index_col=0)

print("Iniziamo subito, quali indici vuoi studiare?")
print(summary)
scelta = input("Inserisci i numeri intervallati da virgole o scrivi tutti: ").strip()

if scelta == "tutti":
    print("Ok, presi tutti.")

else:
    # Converto la scelta in lista di interi e prendo solo quelli selezionati
    scelte_num = [int(x) for x in scelta.split(',')]
    selezionati = summary.loc[scelte_num]
    summary = selezionati.copy()
    summary.to_csv("summary.csv")
    print("\nFile aggiornato, ti mostro summary.csv")
    print(summary)

print("\n")

