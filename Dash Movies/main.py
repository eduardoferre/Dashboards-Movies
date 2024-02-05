from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px


data = pd.read_csv('top_movies_by_gender.csv')
data.head()

data2 = data.values.tolist()
list_gen = []
for row in data2:
    if row[0] not in list_gen:
        list_gen.append(row[0])

cont_gen = len(list_gen) * [0]
for movie in data2:
    ix = 0
    while ix < len(list_gen):
        if(list_gen[ix] == movie[0]):
            break
        ix += 1
    cont_gen[ix] += 1

inx = 0
list_gen_qtd = []
while inx < len(list_gen):
    fil_bil = [list_gen[inx], cont_gen[inx]]
    list_gen_qtd.append(fil_bil)
    inx += 1

df = pd.DataFrame(list_gen_qtd, columns=['Gêneros', 'Quantidade'])

graf = px.bar(df, x='Gêneros', y='Quantidade', color="Gêneros",
                 title='GÊNEROS MAIS BEM AVALIADOS NO MUNDO(>95%)',
                 color_discrete_sequence=px.colors.qualitative.Bold,
                 template='plotly_dark')

app = Dash(__name__)

app.layout = html.Main([
    html.Div(className="vertical-container", children=[
        html.H1("Dash - Gêneros mais bem avaliados do mundo"),
    ]),
    html.Div(children=[
        html.Div(className='horizontal-container', children=[
            html.Label('Selecione o intervalo de quantidade:'),
            dcc.RangeSlider(min=0, max=100, step=10, value=[0, 100],
                            id='slider-quantidade', className='slider'),
        ]),
        dcc.Graph(
            id='generos-avaliados'
        )
    ])
])


@app.callback(
    Output('generos-avaliados', 'figure'),
    Input('slider-quantidade', 'value')
)


def update_graph(range_value):
    values_filt = []
    min_value, max_value = range_value

    for gen in cont_gen:
        if gen > min_value and gen < max_value:
            values_filt.append(gen)

    gen_filt = []
    for gen_qtd in list_gen_qtd:
        if gen_qtd[1] > min_value and gen_qtd[1] < max_value:
            gen_filt.append(gen_qtd[0])

    inx = 0
    list_gen2_qtd2 = []
    while inx < len(gen_filt):
        gen_60 = [gen_filt[inx], values_filt[inx]]
        list_gen2_qtd2.append(gen_60)
        inx += 1

    df2 = pd.DataFrame(list_gen2_qtd2, columns=[
                       'Gêneros', 'Frequência'])

    graf = px.bar(df2, x='Gêneros', y='Frequência', color="Gêneros",
                     title=f'GÊNEROS ENTRE {min_value} E {max_value} FILMES APROVADOS',
                     color_discrete_sequence=px.colors.qualitative.Set1,
                     template='plotly_dark')
    return graf


if __name__ == '__main__':
    app.run_server(debug=True)