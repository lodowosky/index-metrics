import pandas as pd
import os

summary = pd.DataFrame(columns=["Index", "Start", "End"]) #creo un dataframe di riepilogo dove inserire le informazioni più importanti raccolte

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

print(summary)
summary.to_csv("summary.txt")

# concatenazione
df_inner = pd.concat(lista_di_serie, axis=1, join='inner')
df_outer = pd.concat(lista_di_serie, axis=1, join='outer')
df_outer_sorted = df_outer.sort_index()

print(df_inner)
df_inner.to_csv("library_inner.txt")

print(df_outer)
df_outer.to_csv("library.txt")
