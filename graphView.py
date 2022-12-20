import json
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, dcc
import dash_cytoscape as cyto
import pandas as pd
import random
from appUtils import fetch_mutag_arrays

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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


accordion_test = dbc.Card(
    [
        dbc.Accordion(
            [
                dbc.AccordionItem([
                    graph_view
                    ], 
                    title='Graph View')
            ]
        )
    ]
)

app.layout = accordion_test


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
    app.run_server(debug=True)