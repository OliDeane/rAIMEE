import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, Dash, dcc, dash_table
import dash_cytoscape as cyto
import dash
from dash_bootstrap_components._components.Container import Container
import plotly.express as px
import subprocess
import numpy as np
import pandas as pd
import json
from prologUtils import add_constraint, add_positive
from appUtils import fetch_mutag_arrays

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# Instantiate app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# Create placeholder rule coverage figure
def generate_coverageGraph(data_path="coverageData.csv"):
    df = pd.read_csv(data_path)
    fig = px.treemap(df, path=['label', 'rule_ID'], 
                    values='examples_covered', color='label')
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0), paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)')
    fig.update(layout_coloraxis_showscale=False)
    return fig

# Function for cleaning hypothesis list
def str2lst(hypothesis_text):

    hyp_list = hypothesis_text[1:-2].split(".',")
    
    result = []
    for idx, rule in enumerate(hyp_list):
        result.append(f'R{idx}: {rule}')
        result.append(html.P(html.Br()))

    return result


# Create tab switch for displaying in natural language
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

# Create styles for tab setup
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# Add navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("rAIMEE", className="ms-2")),
                    ],
                    align="left",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            )
        ],
        fluid=True
    ),
    color="dark",
    dark=True,
)

# introduction tab
introCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Relational AIMEE - A.I Model Explorer and Editor for Relational Datasets", className="card-title"),
                html.P("AIMEE is an interactive tool for exploring and editing machine learning models. \
                    It uses sets of generated rules in order to create a model surrogate, which can then \
                    be edited and compared.", 
                    className="card-text"),
                
                html.H4("Inductive Logic Programming (ILP)", className="card-title"),
                html.P("After inspecting the model logic through decision rules, AIMEE allows users to add \
                    new rules to change the decision boundaries through using a pre-processing algorithm. \
                    This underlying algorithm first selects a base population from the original dataset \
                    based on the user-provided rules. It then generates instances using this base population\
                    through a method similar to the well known oversampling technique, SMOTE (Synthetic \
                    Minority Oversampling Technique). Once the data is pre-processed to reflect new \
                    rules, AIMEE retrains the model using the new dataset, and the users can\
                    inspect the new decision boundaries.", 
                    className="card-text"),
                
                html.H4("Interactive Rule Editing", className="card-title"),
                html.P("After inspecting the model logic through decision rules, AIMEE allows users to add \
                    new rules to change the decision boundaries through using a pre-processing algorithm. \
                    This underlying algorithm first selects a base population from the original dataset \
                    based on the user-provided rules. It then generates instances using this base population\
                    through a method similar to the well known oversampling technique, SMOTE (Synthetic \
                    Minority Oversampling Technique). Once the data is pre-processed to reflect new \
                    rules, AIMEE retrains the model using the new dataset, and the users can\
                    inspect the new decision boundaries.", 
                    className="card-text"),
                
                html.H4("Model Comparison", className="card-title"),
                html.P("After inspecting the model logic through decision rules, AIMEE allows users to add \
                    new rules to change the decision boundaries through using a pre-processing algorithm. \
                    This underlying algorithm first selects a base population from the original dataset \
                    based on the user-provided rules. It then generates instances using this base population\
                    through a method similar to the well known oversampling technique, SMOTE (Synthetic \
                    Minority Oversampling Technique). Once the data is pre-processed to reflect new \
                    rules, AIMEE retrains the model using the new dataset, and the users can\
                    inspect the new decision boundaries.", 
                    className="card-text"),
                
                html.H4("References", className="card-title"),
                html.P(["Alkan, Öznur, Dennis Wei, Massimiliano Matteti, Rahul Nair, Elizabeth M. Daly, \
                        and Diptikalyan Saha. 'FROTE: Feedback Rule-Driven Oversampling for Editing Models.' \
                        arXiv preprint arXiv:2201.01070 (2022).", html.Br(),
                    "Nair, Rahul, Massimiliano Mattetti, Elizabeth Daly, Dennis Wei, Oznur Alkan, and \
                            Yunfeng Zhang. 'What Changed? Interpretable Model Comparison.' IJCAI, 2021.", html.Br(),
                    "Alkan, Öznur, Dennis Wei, Massimiliano Matteti, Rahul Nair, Elizabeth M. Daly, \
                        and Diptikalyan Saha. 'FROTE: Feedback Rule-Driven Oversampling for Editing Models.' \
                        arXiv preprint arXiv:2201.01070 (2022).", html.Br(),
                    "Nair, Rahul, Massimiliano Mattetti, Elizabeth Daly, Dennis Wei, Oznur Alkan, and \
                            Yunfeng Zhang. 'What Changed? Interpretable Model Comparison.' IJCAI, 2021.", html.Br(),
                    "Alkan, Öznur, Dennis Wei, Massimiliano Matteti, Rahul Nair, Elizabeth M. Daly, \
                        and Diptikalyan Saha. 'FROTE: Feedback Rule-Driven Oversampling for Editing Models.' \
                        arXiv preprint arXiv:2201.01070 (2022).", html.Br(),], 
                    className="card-text")
                
            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "margin-right":"1rem", "width": "103rem", "height":"45rem"},
)
intro = html.Div([introCard])

# Dataset Overview
datasetDropdown = html.Div(
    [
        dcc.Dropdown(
            options=[
                {'label': 'Mutagenesis', 'value': 'opt1'},
                {'label': 'Trains', 'value': 'opt1'}
            ],
            style={
                'width': '100%',
                'margin-left': '2cm',
                'margin-right': '2cm',
            }
        )
    ], style={'width':'80rem'}
)
selectDataCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Preloaded Datasets", className="card-title"),
                html.H6("Select data", className="card-subtitle", style={"margin-bottom":"rem"}),
                datasetDropdown,
                dbc.Button('Submit', id = 'dataSubmit-button', color = "primary", className='me-2', n_clicks=0),

            ]
        )
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "margin-right":"1rem"},
)

# Graph view 
mol_array, bond_array, atom_array = fetch_mutag_arrays()
nodes = [
    {
        'data': {'id': atom_id, 'label': f'{atom_id}:{element}'}
        # 'position': {'x': 20*lat, 'y': 20*long}
    }
    for atom_id, _, element, _, _ in atom_array
]
edges = [
    {'data': {'source': source, 'target': target}}
    for source, target,_,_ in bond_array
]
cytoscape_graph = dbc.Card(
    [
        cyto.Cytoscape(
            id='cytoscape-event-callbacks-1',
            layout={'name': 'cose'},
            elements=edges+nodes,
            style={'width': '100%', 'height': '450px'}
        ),
        dcc.Store(id='node-store', data=[], storage_type='memory')
    ],
    style={"width":"30rem"}
)

molecule_info = html.Div(
    [
        html.H4("Molecule", className="card-title", style={"margin-left":"1rem", "margin-top":"1rem"}),
        html.H6("ID: D1",
            className="card-subtitle", style={"margin-bottom":"1rem", "margin-left":"1rem"}),
        html.H6("Class: Mutagenic",
            className="card-subtitle", style={"margin-bottom":"1rem", "margin-left":"1rem"}),
        html.H6("ind1: 1",
            className="card-subtitle", style={"margin-bottom":"1rem", "margin-left":"1rem"}),
        html.H6("logp: 4.23",
            className="card-subtitle", style={"margin-bottom":"1rem", "margin-left":"1rem"}),
        html.H6("lumo: -1.246",
            className="card-subtitle", style={"margin-bottom":"1rem", "margin-left":"1rem"}),
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "width": "30rem", "height":"12rem", "overflow-y":"scroll"}
)
atom_info = html.Div(
    [
        html.H4("Selected Atom", className="card-title", style={"margin-left":"1rem", "margin-top":"1rem"}),
        html.H6("Select atom to view relevant features",
            className="card-subtitle", style={"margin-bottom":"1rem", "margin-left":"1rem"}),
        html.Div(
            [
                html.Div(id = 'node-info', children = []),
            ]
        )
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "width": "30rem", "height":"18rem", "overflow-y":"scroll"}
)
graph_view = html.Div([
    dbc.Row([
        html.H4("Mutagenesis Dataset", className="card-title", style={"margin-left":"1rem", "margin-top":"1rem"}),
        html.H6("The dataset comprises of 188 molecules trialed for mutagenicity on Salmonella typhimurium.",
                        className="card-subtitle", style={"margin-bottom":"1rem", "margin-left":"1rem"}),
        dbc.Col([
            molecule_info,
            atom_info
        ]),
        
        dbc.Col([
            cytoscape_graph 
        ])
    
    ])
])



# Display Tables
dataset_button_group = html.Div(
    [
        dbc.RadioItems(
            id="dataset_radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Molecule", "value": "molecule"},
                {"label": "Bond", "value": "bond"},
                {"label": "Atom", "value": "atom"},
            ],
            value="molecule",
        ),
        html.Div(id="output"),
    ],
    className="radio-group",
)
presentDataCard = dbc.Card(
    [   
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        html.H4("Mutagenesis Dataset", className="card-title", style={"margin-left":"1rem", "margin-top":"1rem"}),
                        html.H6("The dataset comprises of 188 molecules trialed for mutagenicity on Salmonella typhimurium.",
                        className="card-subtitle", style={"margin-bottom":"1rem", "margin-left":"1rem"}),
                        dataset_button_group
                    ],
                    title="Table View"
                ),
                dbc.AccordionItem(
                    [
                        graph_view
                    ],
                    title="Graph View"
                )
            ],
            start_collapsed=True

        ),
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "margin-right":"1rem"},
)

# Combine into dataset_overview variable
dataset_overview = html.Div([
    html.Div([
        selectDataCard,
        presentDataCard
    ]),
])

# Rule extraction tab
induceCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Induce Rules", className="card-title"),
                dbc.Button('Induce', id = 'induce-button', color = "primary", className='me-2', n_clicks=0),
                dcc.Store(id='hypothesis-store', data=[], storage_type='memory'),
                dbc.Button('Reset', id = 'reset-button', color = "secondary", className='me-2', n_clicks=0),
                html.H4("Model Information", className="card-title", style={"margin-top":"1rem"}),
                html.Div(id = 'modelInfo-box', children = [html.P(html.Br())]),
                html.H4("Dataset Information", className="card-title", style={"margin-top":"1rem"}),
                html.Div(id = 'datasetInfo-box', children = [])
            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "width": "30rem", "height":"18rem", "overflow-y":"scroll"},
)
hypothesisCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Generated Rules", className="card-title"),
                nlSwitch,
                html.Div(id = 'hypothesis-box', children = []),
                
            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "width": "30rem", "height":"36rem", "overflow-y":"scroll"},
)
ruleCoverageCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Rule Coverage", className="card-title"),
                html.H6("Visualization of the induced rule set", className="card-subtitle"),
                html.Div(id = 'ruleCoverageGraph-box', children=[])
            
            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"2rem", "margin-right":"2rem", "width": "68rem", "height":"55rem"}
)
induced_rules = html.Div([
    dbc.Row([
        dbc.Col([
            induceCard,
            hypothesisCard
        ]),
        
        dbc.Col([
            ruleCoverageCard
        ])
    
    ])
])

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

bottomClauseCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Bottom Clause", className="card-title"),
                html.H6("Add constraints to bottom clause generated for select examples", className="card-subtitile"),
                shortNlSwitch,
               
            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"1rem", "width": "45rem", "height":"30rem"},
)
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
assertExamples_button_group = html.Div(
    [
        dbc.RadioItems(
            id="assertExamples_radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Unknown", "value": "unknown"},
                {"label": "Positive", "value": "positive"},
                {"label": "Negative", "value": "negative"},
            ],
            value="unknown",
        ),
        html.Div(id="assertExamples_output"),
    ],
    className="radio-group",
)

assertExamplesCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Assert Examples", className="card-title"),
                html.H6("Add counter examples to guide model learning", className="card-subtitle", style={"margin-bottom":"1rem"}),
                assertExamples_button_group
            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"2rem", "margin-right":"2rem", "width": "50rem", "height":"55rem"}
)

model_editor = html.Div([
    dbc.Row([
        dbc.Col([
            integrityConstraintCard,
            bottomClauseCard
        ]),
        
        dbc.Col([
            assertExamplesCard
        ])
    
    ])
])

# Main app layout
app.layout = html.Div([
    html.Div(navbar),
    html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Introduction', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Dataset Overview', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Induced Rules', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Model Editor', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
    ])
])

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return intro
    elif tab == 'tab-2':
        return dataset_overview
    elif tab == 'tab-3':
        return induced_rules
    elif tab == 'tab-4':
        return model_editor

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
    print(output)
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

    rule_list = str2lst(hypothesis_text)
    print(rule_list)
    return html.P(children=rule_list)

@app.callback(
    Output('modelInfo-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_modelInfo(data):
    return html.P(
        html.P("Accuracy: 86.08%", className="card-text")
    )

@app.callback(
    Output('datasetInfo-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_datasetInfo(data):

    if data:
        return html.P(
            html.P("Total count: 188 | Label T : 94 (50%) |  Label F : 94 (50%)", 
            className="card-text")
        )

@app.callback(
    Output('ruleCoverageGraph-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_ruleCoverageGraph(data):

    if data:
        return dcc.Graph(figure=generate_coverageGraph(), style={'width':"65rem", 'height':"45rem"})

@app.callback(
    Output("output", "children"),
    [Input("dataset_radios", "value")]
)
def display_data_table(value):
    mutagDf = pd.read_csv(f"./data/mutag188/Mutag188_{value}.csv")
    return html.Div(
        [
             dbc.Table.from_dataframe(mutagDf.head(5), striped=True, bordered=True, hover=True)
        ],
        style={"margin-top":"1rem", "margin-left":"1rem", "margin-right":"1rem"},
    )
       
@app.callback(
    Output("assertExamples_output", "children"),
    [Input("assertExamples_radios", "value")]
)
def display_assertExamples(value):
    df = pd.read_csv(f"./data/mutag188/{value}Examples.csv")    
    return html.Div(
    [
        dash_table.DataTable(
            id="assertExamplesTable",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            style_cell={'textAlign':'left'},
            style_data_conditional=style_data_conditional
        ),
    ],
    style={"margin-top":"1rem"}
)

@app.callback(
    Output('hypothesisIC-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_hypothesis(data):
    print(type(data))
    print(data)
    hypothesis_text = data["hypothesis"]
    print(hypothesis_text)

    rule_list = str2lst(hypothesis_text)


    return html.Div(
        [
            html.Div(
                [
                    html.P(id='selection-container', children=rule_list),
                    dcc.Input(id='selection-target', value='', style=dict(display='none')),
                ],
                style={"height":"17rem", "overflow-y": "scroll", "margin-bottom":"1rem"}
            ),
            dbc.Button(id='submit', children='Add', color = "primary", className='me-2', n_clicks=0),
            dbc.Button(id='remove-button', children='Remove', color = "danger", className='me-2', n_clicks=0),
            dbc.Button('Reset', id = 'reset-button', color = "secondary", className='me-2', n_clicks=0),
            html.P(id='removed-predicate', children=[], style={'top-margin':'0rem'}),
            html.P(id='added-predicate', children=[], style={'top-margin':'0rem'}),
        ]
)

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
    
@app.callback(
    Output("assertExamplesTable", "style_data_conditional"),
    [Input("assertExamplesTable", "active_cell")]
)
def update_selected_row_color(active):
    #style = style_data_conditional.copy()
    print(active["row"])
    if active:
        style_data_conditional.append(
            {
                "if": {"row_index": active["row"]},
                "backgroundColor": "rgba(150, 180, 225, 0.2)",
                "border": "1px solid blue",
            },
        )
    return style_data_conditional


@app.callback(Output('node-store', 'data'),
              Input('cytoscape-event-callbacks-1', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        atom_df = pd.read_csv('/Users/fl20994/Documents/IAI_CDT/Research_Project/XIML_ILP/rAIMEE/data/mutag188/atoms.csv')
        selected_atom = atom_df[atom_df['atom_id']==data['id']].values.tolist()[0]
        output_data = {
            'id':selected_atom[0],
            'molecule_id':selected_atom[1],
            'element': selected_atom[2],
            'atype': selected_atom[3],
            'charge':selected_atom[4]
        }
        return json.dumps(output_data, indent=2)

@app.callback(
    Output('node-info', 'children'),
    Input('node-store', 'data')
)
def create_nodeInfo(data):
    if data:
        # convert string to json (needs fixing)
        node_dict = json.loads(data) 
        return html.Div(
            [
                html.P([f"Atom ID: {node_dict['id']}"]),
                html.P([f"Element: {node_dict['element']}"]),
                html.P([f"atype: {node_dict['atype']}"]),
                html.P([f"charge: {node_dict['charge']}"])
            ],
            style = {"margin-top":"2rem","margin-left":"1rem"}
        )



if __name__ == '__main__':
    app.run_server(debug=True, port=8050)