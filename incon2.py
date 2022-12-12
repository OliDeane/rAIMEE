import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, Dash, dcc
import dash
from dash_bootstrap_components._components.Container import Container
import plotly.express as px
import subprocess
import numpy as np
import pandas as pd
from prologUtils import add_constraint


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

def str2lst(hypothesis_text):

    hyp_list = hypothesis_text[1:-2].split(".',")
    
    result = []
    for idx, rule in enumerate(hyp_list):
        result.append(f'R{idx}: {rule}')
        result.append(html.P(html.Br()))

    return result

nlSwitch = dbc.Switch(
                    value=True,
                    id='restricted_search',
                    label='Display in natural language',
                    input_class_name='bg-success'
                    )
shortNlSwitch = dbc.Switch(
                    value=True,
                    id='restricted_search',
                    label='NL',
                    input_class_name='bg-success'
                    )


# Model editing tab
inConHeader = html.Div([
                html.Div([
                    html.H4("Edit Hypothesis", className="card-title"),
                ],
                style={"display": "inline-block"}
                ),
                html.Div([
                    dbc.Button('Show Rules', id = 'induce-button', color = "primary", className='me-2', n_clicks=0),
                    dcc.Store(id='hypothesis-store', data=[], storage_type='memory')
                ], 
                style={"display": "inline-block", "margin-left":"23rem"},
                ),
                html.H6(["Highlight predicates and submit constraints", html.Br(), html.Br()], className="card-subtitle"),
                shortNlSwitch
            ])
inConInnerDiv = html.Div([
    html.Div(id = 'hypothesisIC-box', children = [
        html.P(html.Br()),
        html.P(html.Br()),
        html.P(html.Br()),
        html.P(html.Br()),
        html.P(html.Br()),
        html.P(html.Br()),
        html.P(html.Br()),
        dbc.Button('Add', id = 'remove-button', color = "success", className='me-2', n_clicks=0),
        dbc.Button('Remove', id = 'add-button', color = "danger", className='me-2', n_clicks=0),
        dbc.Button('Reset', id = 'reset-button', color = "secondary", className='me-2', n_clicks=0),
    ])
],
style={"height":"17rem", "margin-bottom":"1rem"} # Add "overflow": "scroll" if needed
)
integrityConstraintCard = dbc.Card(
    [
        dbc.CardBody(
            [
                inConHeader,
                inConInnerDiv,

            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "width": "45rem", "height":"30rem"},
)


app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            integrityConstraintCard,
        ]),    
    ])
])

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
    Output('hypothesisIC-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_IChypothesis(data):

    hypothesis_text = data["hypothesis"]
    print(type(hypothesis_text))
    print(hypothesis_text)

    rule_list = str2lst(hypothesis_text)

    

    return html.Div([
            html.P(id='selection-container', children=rule_list),
            dcc.Input(id='selection-target', value='', style=dict(display='none')),
            dbc.Button(id='submit', children='Add', color = "primary", className='me-2', n_clicks=0),
            dbc.Button(id='remove-button', children='Remove', color = "danger", className='me-2', n_clicks=0),
            dbc.Button('Reset', id = 'reset-button', color = "secondary", className='me-2', n_clicks=0),
            html.P(id='removed-predicate', children=[], style={'top-margin':'0rem'}),
            html.P(id='added-predicate', children=[], style={'top-margin':'0rem'}),
            ])

@app.callback(
    dash.dependencies.Output('added-predicate', 'children'),
    [dash.dependencies.Input('submit', 'n_clicks')],
    [dash.dependencies.State('selection-target', 'value')],)
def update_output(n_clicks, value):
    if value:
        # Add constraint to the background knowledge
        add_constraint(value)

        return html.Span(f'Added Predicate: "{value}"', style=dict(color='blue'))

@app.callback(
    dash.dependencies.Output('removed-predicate', 'children'),
    [dash.dependencies.Input('remove-button', 'n_clicks')],
    [dash.dependencies.State('selection-target', 'value')],)
def removePredicate(n_clicks, value):
    if value:
        # Add constraint to the background knowledge
        print(value)
        add_constraint(value)

        return html.Span(f'Removed Predicate: "{value}"', style=dict(color='red'))
    


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)