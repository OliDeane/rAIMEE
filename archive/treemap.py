import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, Dash, dcc
from dash_bootstrap_components._components.Container import Container
import plotly.express as px
import numpy as np


df = px.data.gapminder().query("year == 2007")
fig = px.treemap(df, path=[px.Constant("world"), 'continent', 'country'], values='pop',
                  color='lifeExp', hover_data=['iso_alpha'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))

app = Dash(external_stylesheets=[dbc.themes.JOURNAL])

app.layout = html.Div(
    dcc.Graph(figure=fig)
)

if __name__ == '__main__':
    app.run_server(debug=True)