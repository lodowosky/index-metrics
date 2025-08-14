import pandas as pd
import os

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

#accedo ai file che mi servono
summary = pd.read_csv('indexes_available.csv', index_col=0) 
daily_returns_inner = pd.read_csv('daily_returns_inner.txt', index_col=0)

print("Iniziamo subito, quali indici vuoi studiare?")
print(summary)
scelta = input("Inserisci i numeri intervallati da virgole o scrivi tutti: ").strip()

if scelta == "tutti":
    # Se l'utente ha scelto tutti, prende tutti
    selezionati = summary.copy()
    print("Ok, presi tutti.")
else:
    # Converto la scelta in lista di interi e prendo solo quelli selezionati
    scelte_num = [int(x) for x in scelta.split(',')]
    selezionati = summary.loc[scelte_num]
    # Stampo i selezionati
    print("Hai selezionato:")
    print(selezionati)

#da questo momento in poi non toccherai più summary, lavorerai solo su selezionati

years = int(input("Ora inserisci la durata dell'investimento (in anni): "))

#risk_free_rate = float(input("\nInserisci il risk free return attuale (per il calcolo dello Sharpe ratio): "))
risk_free_rate = 0.02
print(f"Perfetto, iniziamo!\nSto usando un risk_free_rate = {risk_free_rate}.")


records = [] # lista dove accumulare i risultati
list_of_rendimenti = []

for index, row in selezionati.iterrows():
  nome = row['Name']

  if nome in daily_returns_inner.columns:
    daily_returns = daily_returns_inner[nome]  # Series pulita
    start = daily_returns.index[0]
    end = daily_returns.index[-1]

    rendimenti = calculate_annualized_cumulative_returns(daily_returns, years)

    if rendimenti is None:
      print(f"Escludo {nome}, avendo la prima quotazione al {start} non è possibile simulare un investimento di durata {years} anni")
      continue

    rendimenti.name = nome
    list_of_rendimenti.append(rendimenti)

    rendimento_medio = rendimenti.mean()
    deviazione_std = rendimenti.std()

    records.append({
        "Name": nome,
        "Start": start,
        "End": end,
        "Ann. return (%)": round(rendimento_medio, 4),
        "Std. dev. (%)": round(deviazione_std, 4),
        "Sharpe ratio": round((rendimento_medio - risk_free_rate)  / deviazione_std, 4)
    })

cumulative_returns_inner = pd.concat(list_of_rendimenti, axis=1, join='inner') #salvo i rendimenti dell'investimento allineati
cumulative_returns_outer = pd.concat(list_of_rendimenti, axis=1, join='outer') #salvo i rendimenti dell'investimento

# Creo il DataFrame
selezionati = pd.DataFrame(records)
#selezionati.index = selezionati.index + 1

# Stampo il DataFrame
print(f"\nDalla mia analisi su un investimento di {years} anni otteniamo le seguenti informazioni:\n")
print(selezionati) 
selezionati.to_csv("Analytics.csv", sep="\t", index=False)
