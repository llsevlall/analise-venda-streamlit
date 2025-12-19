import plotly.express as px
from utils import df_formas_pagamento, df_genero_grafico

fig = px.bar(
        df_formas_pagamento,
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


fig2 = px.pie(
        df_genero_grafico,
        names='cliente_genero',
        values='count',
        title='Quantidade de compras por gênero',
        color_discrete_sequence=['#616161', '#474747']
    )
