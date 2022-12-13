import dash
from dash import html, dcc, Input, Output, dash_table
from dash.dependencies import Output, Input
# from dash_selectable import DashSelectable
# import dash_bootstrap_components as dbc
from PIL import Image
import pandas as pd
import numpy as np
import subprocess
import plotly.express as px
from prologUtils import add_constraint

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
] 


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

button = html.Div(
    children=[
        html.Div(children="Generate Hypothesis", className="menu-title"),
        html.Button('Induce', id = 'induce-button', 
        style={'font-size': '12px', 'width': '140px', 'display': 'inline-block', 'margin-bottom': '10px', 
        'margin-left':'10px', 'margin-right': '5px', 'height':'37px', 'verticalAlign': 'top'}, n_clicks=0),
        dcc.Store(id='hypothesis-store', data=[], storage_type='memory')
    ],
)

integrityConstraint = html.Div([
                    html.Div(children="Integrity Constraint", className="menu-title"),
                    html.Div(
                        id = 'integrityConstraint-box', children = [],
                        style={'margin-top':'0px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                            'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                    )
                ])

app.layout = html.Div(
    [
        button,
        integrityConstraint
    ]
)

@app.callback(
    dash.dependencies.Output('hypothesis-store', 'data'),
    [dash.dependencies.Input('induce-button', 'n_clicks')])
def induce_onClick(n_clicks):

    
    if not n_clicks:
        return dash.no_update

    result = subprocess.check_output('python inferenceScript.py', shell=True)  
    theory = subprocess.check_output('python hypothesisScript.py', shell=True)
    
    # convert bytes to string
    output = theory.decode()  

    returnable = {'hypothesis':output}
    # return output
    return returnable

@app.callback(
    Output('integrityConstraint-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_integrityHypothesis(data):
    print(type(data))
    print(data)
    hypothesis_text = data["hypothesis"]
    print(hypothesis_text)

    return html.Div([
            html.P(id='selection-container', children=f'{hypothesis_text[2:-2]}'),
            dcc.Input(id='selection-target', value='', style=dict(display='none')),
            html.Button(id='submit', children='Submit selection',
            style={'font-size': '12px', 'width': '140px', 'display': 'inline-block', 'margin-bottom': '10px', 
                        'margin-left':'10px', 'margin-right': '5px', 'height':'37px', 'verticalAlign': 'top'}),
            html.P(id='callback-result', children=[]),
            ])

@app.callback(
    dash.dependencies.Output('callback-result', 'children'),
    [dash.dependencies.Input('submit', 'n_clicks')],
    [dash.dependencies.State('selection-target', 'value')],)
def update_output(n_clicks, value):
    if value:
        # Add constraint to the background knowledge
        add_constraint(value)

        return html.Span(f'Selected string: "{value}"', style=dict(color='green'))
    return html.Span('Nothing selected', style=dict(color='blue'))


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)