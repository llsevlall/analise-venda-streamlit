from dataframe import df_compras

df_formas_pagamento = df_compras['forma_pagamento'].value_counts().reset_index()

df_genero_grafico = df_compras['cliente_genero'].value_counts().reset_index()
