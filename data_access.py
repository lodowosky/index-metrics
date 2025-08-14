import pandas as pd
import os

summary = pd.DataFrame(columns=["Name", "Start", "End"]) #creo un dataframe di riepilogo dove inserire le informazioni più importanti raccolte

# percorso della cartella
cartella = "/Users/lodovicocaruso/index-metrics/index-data"
file_txt = [f for f in os.listdir(cartella) if f.endswith('.txt')]

print("Ho trovato questi file:")
print(file_txt)

lista_di_serie = []

for file in file_txt:
    percorso_file = os.path.join(cartella, file)
    try:
        print(f"Leggo il file: {file}")
        df = pd.read_csv(percorso_file, index_col=0, parse_dates=[0]) #il file viene letto in un dataframe, la prima colonna è l'indice del dataframe e la legge in formato date 
        serie = df.iloc[:,0]  # Estrae la colonna come Serie conservando intestazione (nome indice) e le date
        summary.loc[len(summary)] = [serie.name, serie.index[0], serie.index[-1],] #inserisce informazioni in summary
        lista_di_serie.append(serie)
    except Exception as e:
        print(f"Errore leggendo {file}: {e}")

summary.to_csv("summary.csv")

# concatenazione
daily_returns_inner = pd.concat(lista_di_serie, axis=1, join='inner')
daily_returns_outer = pd.concat(lista_di_serie, axis=1, join='outer')
daily_returns_outer = daily_returns_outer.sort_index()


daily_returns_inner.to_csv("daily_returns_inner.txt")
daily_returns_outer.to_csv("daily_returns_outer.txt")

print("\nFile aggiornati, ti mostro summary.csv")
print(summary)
print("\n")
