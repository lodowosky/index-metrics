import pandas as pd
import numpy as np
import os
import sys

# una funzione che restituisce la lista dei ritorni cumulativi prendendo in input una lista di ritorni giornalieri
def calculate_cumulative_returns(group):
  return (1 + group).cumprod() - 1

# una funzione che restituire il rendimento annualizzato atteso prendendo in input i ritorni giornalieri e il periodo di investimento (la finestra mobile dove calcolare il rend. ann. atteso)
def calculate_annualized_cumulative_returns(daily_returns, years):
    window_size = 253  # giorni di mercato in un anno
    n = len(daily_returns)

    if n < years * window_size:
        print("\nSerie troppo corta per la finestra specificata")
        return None

    annualized_returns = []
    date_corr = []

    for i in range(n - window_size * years + 1):
        selected_returns = daily_returns.iloc[i : i + window_size * years]
        cumulative_returns = calculate_cumulative_returns(selected_returns)

        # rendimento cumulato finale nella finestra
        R_tot = cumulative_returns.iloc[-1]

        # annualizzazione
        annual_return = (1 + R_tot) ** (1 / years) - 1

        annualized_returns.append(annual_return * 100)  # in percentuale
        date_corr.append(selected_returns.index[-1])    # data finale finestra

    return pd.Series(data=annualized_returns, index=date_corr)

#input
summary = pd.read_csv('summary.csv', index_col=0) 
daily_returns_outer = pd.read_csv('daily_returns_outer.txt', index_col=0)

years = int(input("Ora inserisci la durata dell'investimento (in anni): "))
#risk_free_rate = float(input("\nInserisci il risk free return attuale (per il calcolo dello Sharpe ratio): "))
risk_free_rate = 0.02
print(f"Perfetto, iniziamo!\nSto usando un risk_free_rate = {risk_free_rate}.")

#calcolo
all_cumulative_returns =[]
for index, row in summary.iterrows():

    nome = row['Name']
    print(nome)
    daily_returns_selection = daily_returns_outer.loc[:, nome].dropna() #prendo la colonna di dati

    cumulative_returns = calculate_annualized_cumulative_returns(daily_returns_selection, years)
    cumulative_returns.name = nome
    all_cumulative_returns.append(cumulative_returns)

print(all_cumulative_returns)
cumulative_returns_outer = pd.concat(all_cumulative_returns, axis=1, join='outer')
cumulative_returns_outer = cumulative_returns_outer.sort_index()
print(cumulative_returns_outer)