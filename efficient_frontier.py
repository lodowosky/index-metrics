import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import itertools

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

def genera_quote_df_equilibrato(summary, step=0.1, min_val=0.1, max_val=0.9, decimali=2):
    n = len(summary)
    valori = np.arange(min_val, max_val + step/2, step)  # aggiungo step/2 per includere max_val
    risultati = set()
    
    for combo in itertools.combinations_with_replacement(valori, n-1):
        if sum(combo) < 1 + 1e-10:  # piccolo margine per evitare errori numerici
            ultimo = 1 - sum(combo)
            if min_val - 1e-10 <= ultimo <= max_val + 1e-10:
                # Arrotondo ogni valore e genero tutte le permutazioni
                arrotondati = tuple(round(v, decimali) for v in combo + (ultimo,))
                for perm in set(itertools.permutations(arrotondati)):
                    risultati.add(perm)
    
    return pd.DataFrame(sorted(risultati), columns=summary['Name'])


#input
summary = pd.read_csv('summary.csv', index_col=0)
daily_returns_outer = pd.read_csv('daily_returns_outer.txt', index_col=0)
daily_returns_inner = daily_returns_outer.dropna()

'''
maxi = 5

if len(summary) >= maxi:
    print(f"Non posso procede con più di {maxi} indici. Selezionare qualcuno con data_selection.py")
    sys.exit(1)
'''

years = int(input("Ora inserisci la durata dell'investimento (in anni): "))
#risk_free_rate = float(input("\nInserisci il risk free return attuale (per il calcolo dello Sharpe ratio): "))
risk_free_rate = 0.02
print(f"Perfetto, iniziamo!\nSto usando un risk_free_rate = {risk_free_rate}.\n")

#calcolo
quote = genera_quote_df_equilibrato(summary, step=0.05, min_val=0.0, max_val=1)
print(quote)
print(f"\nDevo calcolare {len(quote)} combinazioni\n")


for i in range(len(quote)):
    # pesi del portafoglio
    w = quote.loc[i, summary['Name']].values  
    
    # rendimento giornaliero del portafoglio = combinazione lineare dei ritorni
    portfolio_returns = daily_returns_inner.values @ w
    portfolio_returns = pd.Series(portfolio_returns, index=daily_returns_inner.index)

    # calcolo rolling annualizzato del portafoglio
    cumulative_returns = calculate_annualized_cumulative_returns(portfolio_returns, years)

    # statistiche
    mean = cumulative_returns.mean()
    std  = cumulative_returns.std()

    # scrittura nei risultati
    quote.loc[i, "Ann. return (%)"] = round(mean, 3)
    quote.loc[i, "Std. dev. (%)"]   = round(std, 3)
    quote.loc[i, "Sharpe ratio"]    = round((mean - risk_free_rate) / std, 3)

    print(f"{i+1} su {len(quote)}")


#inserisco un etichetta per i portfogli a singoli asset
mask = quote[quote.columns[:len(summary)]].eq(1)
quote["Label"] = mask.apply(lambda row: row.index[row].tolist()[0] if row.any() else np.nan, axis=1)
#e una per i max sharpe e il min std
quote.at[quote["Std. dev. (%)"].idxmin(), 'Label'] = 'MIN STD'
quote.at[quote["Sharpe ratio"].idxmax(), 'Label'] = 'MAX SHARPE'
quote.to_csv("portfolio-results/cumulative_returns.txt") 


#salvo i risultati notevoli
results = quote[quote["Label"].notna()].copy()
results.to_csv("portfolio-results/portfolio_summary.csv") 

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(results)
    
#grafico
plt.scatter(quote.loc[:, "Std. dev. (%)"], quote.loc[:, "Ann. return (%)"], color = 'blue', alpha = 0.25)
# Aggiungo le etichette
for i, label in enumerate(results["Label"]):
        plt.plot(
            results["Std. dev. (%)"].iloc[i], 
            results["Ann. return (%)"].iloc[i], 'o',
            label = label,
        )

plt.xlabel("Std. dev. (%)")
plt.ylabel("Ann. return (%)")
plt.axis('equal')
plt.title(f"Efficient frontier for {years} years investing portfolio")
plt.legend(loc='best')
plt.grid(True)

plt.savefig('portfolio-results/efficient_frontier.png')
# Mostrare il grafico
plt.show()
