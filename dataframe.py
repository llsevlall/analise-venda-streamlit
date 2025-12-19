import pandas as pd

caminho_arquivo = "./datasets/compras.csv"

df_compras = pd.read_csv(caminho_arquivo, sep=";", decimal=",", index_col=0)
df_compras.index = pd.to_datetime(df_compras.index)
