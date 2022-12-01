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

df = pd.read_csv('posExamples.csv')
neg_df = pd.read_csv('negExamples.csv')
ruleCoverage_df = pd.read_csv('rule_coverage.csv')
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
] # this doesn't seem to have a big impact - maybe affects font,  but as yet unclear. 

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Interactive model maintenance with Inductive Logic Programming"
style_data_conditional = [
    {
        "if": {"state": "active"},
        "backgroundColor": "rgba(150, 180, 225, 0.2)",
        "border": "1px solid blue",
    },
    {
        "if": {"state": "selected"},
        "backgroundColor": "rgba(0, 116, 217, .03)",
        "border": "1px solid blue",
    },
]


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🤖", className="header-emoji"),
                html.H1(
                    children="Symbolic IML", className="header-title"
                ),
                html.P(
                    children="Using Inductive Logic Programming"
                    "and Innteractive Machine Learning techniques"
                    "to mitigate shortcut learning in ML.",
                    className="header-description",
                ),
            ], 
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Generate Hypothesis", className="menu-title"),
                        html.Button('Induce', id = 'induce-button', 
                        style={'font-size': '12px', 'width': '140px', 'display': 'inline-block', 'margin-bottom': '10px', 
                        'margin-left':'10px', 'margin-right': '5px', 'height':'37px', 'verticalAlign': 'top'}, n_clicks=0),
                        dcc.Store(id='hypothesis-store', data=[], storage_type='memory')
                    ],
                ), 
            ],
            className="menu",
        ),
        
        html.Div(       
            children=[
                html.Div([
                    html.Div(children="Positive Examples", className="menu-title"),
                    html.Div(
                        dash_table.DataTable(
                        id="table1",
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict("records"),
                        style_data_conditional=style_data_conditional
                        ),
                        style={'margin-top':'0px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                            'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                    )
                ]),
                html.Div([
                    html.Div(children="Negative Examples", className="menu-title"),
                    html.Div(
                        dash_table.DataTable(
                        id="table2",
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict("records"),
                        style_data_conditional=style_data_conditional
                    ),
                        style={'margin-top':'0px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                            'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                    )
                ]),
                html.Div([
                    html.Div(children="Unknown Examples", className="menu-title"),
                    html.Div(
                        dash_table.DataTable(
                        id="table3",
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict("records"),
                        style_data_conditional=style_data_conditional
                    ),
                        style={'margin-top':'0px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                            'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                    )
                ])
            ], 
        style={'max-width': '2048px', 
            'padding-right': '10px', 'padding-left': '10px', 'margin-bottom':'32px',
             'margin-top': '32px', 'display':'flex'},
        ),
    
        html.Div(
            children=[
                html.Div([
                    html.Div(children="Selected Example Output", className="menu-title"),
                    html.Div(
                        html.P(
                            children=[" Prediction:",
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            " Explanation"
                            ]
                        ),
                        style={'margin-top':'0px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                            'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                    )
                ]),
                html.Div([
                    html.Div(children="Select Example", className="menu-title"),
                    html.Div(
                        html.P("Image Placeholder"),
                        style={'margin-top':'0px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                            'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                    )
                ]
                ),
                
                html.Div([
                    html.Div(children="Rule Coverage", className="menu-title"),
                    html.Div(
                        dash_table.DataTable(
                            id="ruleCoverageTable",
                            columns=[{"name": i, "id": i} for i in ruleCoverage_df.columns],
                            data=ruleCoverage_df.to_dict("records")
                        ),
                        style={'margin-top':'0px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                            'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                    )
                ])
            ],
            style={'max-width': '2048px', 
            'padding-right': '10px', 'padding-left': '10px', 'margin-bottom':'32px',
             'margin-top': '32px', 'display':'flex'},
        ),
    
        html.Div(
            children=[
                html.Div([
                    html.Div(children="Current Hypothesis", className="menu-title"),
                    html.Div(
                        id = 'hypothesis-box', children = [],
                        style={'margin-top':'0px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                            'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                    ),
                ]),
                html.Div([
                    html.Div(children="Integrity Constraint", className="menu-title"),
                    html.Div(
                        id = 'integrityConstraint-box', children = [],
                        style={'margin-top':'0px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                            'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                    )
                ]),
                html.Div([
                    html.Div(children="Bottom Clause", className="menu-title"),
                    html.Div(
                        html.P(
                            children=[" Placeholder for Bottom Clause",
                            html.Br(),
                            " Bottom Clause will appear here"
                            ]
                        ),
                        style={'margin-top':'0px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                            'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                    )
                ])
            ],
            style={'max-width': '2048px',
            'padding-right': '10px', 'padding-left': '10px', 'margin-bottom':'96px',
             'margin-top': '32px', 'display':'flex'},
        
        ),

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
    Output('hypothesis-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_hypothesis(data):
    print(type(data))
    print(data)
    hypothesis_text = data["hypothesis"]
    print(hypothesis_text)

    return html.P(children=[
        f"{hypothesis_text}"
    ])

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
            html.P(id='callback-result', children=''),
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
    return html.Span('Nothing selected', style=dict(color='red'))


@app.callback(
    Output("table1", "style_data_conditional"),
    [Input("table1", "active_cell")]
)
def update_selected_row_color(active):
    # style = style_data_conditional.copy()
    if active:
        style_data_conditional.append(
            {
                "if": {"row_index": active["row"]},
                "backgroundColor": "rgba(150, 180, 225, 0.2)",
                "border": "1px solid blue",
            },
        )
    return style_data_conditional

@app.callback(
    Output("table2", "style_data_conditional"),
    [Input("table2", "active_cell")]
)
def update_selected_row_color(active):
    # style = style_data_conditional.copy()
    if active:
        style_data_conditional.append(
            {
                "if": {"row_index": active["row"]},
                "backgroundColor": "rgba(150, 180, 225, 0.2)",
                "border": "1px solid blue",
            },
        )
    return style_data_conditional

@app.callback(
    Output("table3", "style_data_conditional"),
    [Input("table3", "active_cell")]
)
def update_selected_row_color(active):
    # style = style_data_conditional.copy()
    if active:
        style_data_conditional.append(
            {
                "if": {"row_index": active["row"]},
                "backgroundColor": "rgba(150, 180, 225, 0.2)",
                "border": "1px solid blue",
            },
        )
    return style_data_conditional



if __name__ == "__main__":
    app.run_server(debug=True)