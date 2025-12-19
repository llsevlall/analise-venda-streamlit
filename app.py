import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Vendas",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            min-width: 320px;
            width: 320px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Análise das Vendas")

caminho_arquivo = "./datasets/compras.csv"

df_compras = pd.read_csv(caminho_arquivo, sep=";", decimal=",", index_col=0)

df_compras.index = pd.to_datetime(df_compras.index)
colunas = list(df_compras.columns)
colunas_selecionadas = st.multiselect("Selecione as colunas:", colunas, colunas)
st.sidebar.subheader("Selecione os dados de compra para filtrar")

if not colunas_selecionadas:
    st.warning("Selecione ao menos uma coluna para visualizar os dados.")
else:
    df_filtrado = df_compras[colunas_selecionadas]
    data_frame = st.dataframe(df_filtrado, height=600)

    col1, col2 = st.sidebar.columns(2)

    colunas_filtro = [c for c in colunas_selecionadas if c != 'id_compra']

    if colunas_filtro:
        col_box = col1.selectbox("Selecione uma coluna", colunas_filtro)
        col_box_2 = col2.selectbox(
            "Selecione uma informação",
            df_filtrado[col_box].unique()
        )

        filtrar = col1.button("Filtrar")
        resetar = col2.button("Resetar")

        if filtrar:
            filtro = df_filtrado[df_filtrado[col_box] == col_box_2]
            data_frame.dataframe(filtro, height=600)
            st.sidebar.header(f"Numero de dados filtrados: {len(filtro)}" )

        if resetar:
            data_frame.dataframe(df_filtrado, height=600)


    st.sidebar.divider()
    st.sidebar.subheader("Adicionar novo cliente")

    col3, col4 = st.sidebar.columns(2)

    loja = col3.selectbox('Qual loja?', df_compras['loja'].unique())
    vendedor = col4.text_input('Quem fez a venda?')
    produto = col3.selectbox('Qual produto?', df_compras['produto'].unique())
    cliente = col4.text_input('Quem fez a compra?')
    genero = col3.selectbox('Qual o gênero do comprador?', df_compras['cliente_genero'].unique())
    pagamento = col4.selectbox('Qual foi a forma de pagamento?', df_compras['forma_pagamento'].unique())

    adicionar = st.sidebar.button('Adicionar coluna')

    if adicionar:
        if not cliente or not vendedor:
            st.sidebar.warning("Adicionar cliente e vendedor.")
        else:
            novo_registro = {
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%m"),
                "loja": loja,
                "id_compra": df_compras['id_compra'].max() + 1,
                "vendedor": vendedor,
                "produto": produto,
                "cliente_nome": cliente,
                "cliente_genero": genero,
                "forma_pagamento": pagamento
            }

            df_nova = pd.DataFrame([novo_registro]).set_index("data")
            df_compras = pd.concat([df_compras, df_nova])
            df_compras.to_csv(
                caminho_arquivo,
                sep=";",
                decimal=","
            )
            st.sidebar.success('Cliente adicionado com sucesso! Recarregue a página para ver o novo cliente.')

    st.sidebar.divider()
    st.sidebar.subheader("Excluir cliente")
    indice = st.sidebar.number_input('Qual o índice do Cliente?', min_value=0,
        step=10)
    col4 = st.sidebar.button('Excluir cliente')

    if col4:
        if indice not in df_compras['id_compra'].values:
            st.sidebar.warning("Coloque um índice compatível.")
        else:
            indice_para_excluir = df_compras[df_compras['id_compra'] == indice].index
            df_compras = df_compras.drop(indice_para_excluir)
            df_compras.to_csv(
                caminho_arquivo,
                sep=";",
                decimal=","
            )
            st.sidebar.success('Cliente excluído com sucesso!')
            st.rerun()

    st.sidebar.divider()
    st.sidebar.subheader("Analisar por data")

    col5, col6 = st.sidebar.columns(2)

    primeira_data = col5.date_input('Qual o começo da data?', value=df_compras.head(1).index[0])
    segunda_data = col6.date_input('Qual o final da data?')
    filtrar_data = st.sidebar.button('Filtrar por data')

    if filtrar_data:
        data_inicio = pd.to_datetime(primeira_data)
        data_fim = pd.to_datetime(segunda_data)

        df_filtrado_data = df_compras[
            (df_compras.index >= data_inicio) &
            (df_compras.index <= data_fim)
            ]

        if df_filtrado_data.empty:
            st.sidebar.warning(
                f'Nenhuma compra encontrada entre {data_inicio.date()} e {data_fim.date()}. Por favor, verifique as datas.')
        else:
            data_frame.dataframe(df_filtrado_data, height=600)
            st.sidebar.header(f"Total de vendas entre esses dois meses: {len(df_filtrado_data)}")
            st.sidebar.header(f"Loja que mais vendeu: {df_filtrado_data['loja'].value_counts().head(1).index[0]}")
            st.sidebar.header(f"Tipo de pagamento que mais vendeu: "
                              f"{df_filtrado_data['forma_pagamento'].value_counts().head(1).index[0]}")

    st.title('Dashboards das Vendas')

    formas_pagamento = df_compras['forma_pagamento'].value_counts().reset_index()

    fig = px.bar(
        formas_pagamento,
        x='forma_pagamento',
        y='count',
        labels={
            'count': 'Quantidade de pagamentos',
            'forma_pagamento': 'Forma de pagamentos'
        },
        hover_data={
            'count': True
        },
        color='forma_pagamento',
        color_discrete_sequence=['#616161', '#474747', '#ADADAD', '#000000']
    )



    st.plotly_chart(fig)

    st.divider()

    df_genero_grafico = df_compras['cliente_genero'].value_counts().reset_index()

    fig = px.pie(
        df_genero_grafico,
        names='cliente_genero',
        values='count',
        title='Quantidade de compras por gênero',
        color_discrete_sequence=['#616161', '#474747']
    )

    st.plotly_chart(fig)
