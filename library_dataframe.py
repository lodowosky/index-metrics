import pandas as pd
import os

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
        df = pd.read_csv(percorso_file, index_col=0, parse_dates=[0])
        serie = df.iloc[:,0]  # Estrae la colonna come Serie
        lista_di_serie.append(serie)
    except Exception as e:
        print(f"Errore leggendo {file}: {e}")

# concatenazione
df_inner = pd.concat(lista_di_serie, axis=1, join='inner')
df_outer = pd.concat(lista_di_serie, axis=1, join='outer')
df_outer_sorted = df_outer.sort_index()

print("\nDataFrame inner:")
print(df_inner)
df_inner.to_csv("library_inner.txt")

print("\nDataFrame outer:")
print(df_outer)
df_outer.to_csv("library.txt")
