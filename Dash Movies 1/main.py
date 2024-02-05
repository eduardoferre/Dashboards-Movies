from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px


data_frame = pd.read_csv('imdb_top_1000.csv')
data_frame.head(4)



list_total = data_frame.values.tolist()

ratings_printed = []
names_movies = []
for i in list_total:
  if i[6] not in ratings_printed:
    ratings_printed.append(i[6])
    names_movies.append(i[1])

graph_line = px.line(x = names_movies, y = ratings_printed, width=1000,
    height=1000, title='Os Maiores do Cinema - Avaliação IMDB',
    color_discrete_sequence=px.colors.qualitative.Alphabet,
    template = 'plotly_dark')

app = Dash(__name__)

app.layout = html.Main([
    html.Div(className="vertical-container", children=[
        html.H1("DASH: Os Maiores do Cinema - Avaliações"),
        html.Div(className='horizontal-container', children=[
            html.Label('Selecione o intervalo referente a nota:'),
            dcc.RangeSlider(min=0, max=10, step=1, value=[6, 10], id='imb-slider', className='slider')
        ]),
        dcc.Graph(
            id='imb-graphic'
        )
    ])
])

@app.callback(
    Output('imb-graphic', 'figure'),
    Input('imb-slider', 'value')
)
def update_graph(value):
    min_value, max_value = value

    rating_movies = []
    ratings = []
    for i in list_total:
        note = i[6]
        movies_names = i[1]

        if note not in ratings:
            ratings.append(note)
            rating_movies.append([movies_names, note])

    rating_movies_filtered = []
    for mv_note in rating_movies:
        movie = mv_note[0]
        note = mv_note[1]

        if max_value >= note >= min_value:
            rating_movies_filtered.append([movie, note])

    names_movies = []
    ratings_printed = []
    for mv_note in rating_movies_filtered:
        names_movies.append(mv_note[0])
        ratings_printed.append(mv_note[1])

    if len(names_movies) > 0 and len(ratings_printed) > 0:
        graph = px.bar(x=names_movies, y=ratings_printed,
                          labels={'x': 'movies', 'y': 'notes'}, color_discrete_sequence=px.colors.qualitative.Set1, template='plotly_dark')
    else:
        graph = px.bar(x=[0], y=[0], labels={'x': 'movies', 'y': 'notes'}, color_discrete_sequence=px.colors.qualitative.Set1, template='plotly_dark')

    return graph

if __name__ == '__main__':
    app.run_server(debug=True)


