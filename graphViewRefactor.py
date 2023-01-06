import json
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, dcc
import dash_cytoscape as cyto
import pandas as pd
import random
from appUtils import fetch_mutag_arrays

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


left_panel = html.Div(
    [
        html.Div(
            [
                dbc.Input(id="molInput", type="number", value=1, min=0, max=10, step=1),
                dcc.Store(id='selectedExample-store', data=[], storage_type='memory')
            ],
            id="styled-numeric-input",
            style={"width":"5rem"}
        ),
        html.Div(id="selectedExampleInfo")
    ],
    style = {'margin-left':'2rem', 'margin-top':'2rem'}    
)

right_panel = html.Div(
    [
        html.Div([
            dbc.Toast(
            id="sample-info",
            header="Selected Molecule",
            icon="primary",
            dismissable=True,
            is_open=True,
            )
        ],
        style={'margin-bottom':'2rem'}
        ),   
        dbc.Toast(
            id="node-info",
            header="Selected Atom",
            icon="primary",
            dismissable=True,
            is_open=True,
        ),
    ],
    style={'margin-right':'-3rem'}
)

graph_view = html.Div([
    dbc.Row([
        html.H4("Mutagenesis Dataset", className="card-title", style={"margin-left":"1rem", "margin-top":"1rem"}),
        html.H6("The dataset comprises of 188 molecules trialed for mutagenicity on Salmonella typhimurium.",
                        className="card-subtitle", style={"margin-bottom":"1rem", "margin-left":"1rem"}),
        dbc.Col([
            left_panel
        ]),
        
        dbc.Col([
            right_panel
        ]),    
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

@app.callback(
    Output("selectedExample-store", "data"), 
    [Input("molInput", "value")])
def output_selectedMolecule(value):
    '''
    Returns information on the selected molecule.
    Default is molecule_id 1.
    '''
    if value:
        print(value)
        mol_array, bond_array, atom_array = fetch_mutag_arrays(str(value))
        return {
            'molecule': mol_array,
            'atom': atom_array,
            'bond': bond_array
        }

@app.callback(
    Output('selectedExampleInfo', 'children'),
    Input('selectedExample-store', 'data')
)
def returnExample(data):
    if data:

        atom_array = data['atom']
        bond_array = data['bond']
        mol_array = data['molecule'][0]
        mol_dict = {'ID':mol_array[0],
            'Mutagenic':mol_array[5],
            'logP':mol_array[3],
            'ind1':mol_array[4]
        }

        nodes = [
        {'data': {'id': atom_id, 'label': f'{atom_id}:{element}'}}
        for atom_id, _, element, _, _ in atom_array]
        edges = [{'data': {'source': source, 'target': target}}
        for source, target,_,_ in bond_array]

        cytoscape = html.Div(
            [
            html.Div(
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
            ),
            # html.H4(['Selected Molecule:'], className = "card-title"),
            # html.Pre(json.dumps(mol_dict, indent=2))
            ]
        )

        return cytoscape

@app.callback(Output('node-store', 'data'),
              Input('cytoscape-event-callbacks-1', 'tapNodeData'))
def displayTapNodeData(data):
    if not data:
        output_data = {
        'id':'None',
        'molecule_id':'None',
        'element': 'None',
        'atype': 'None',
        'charge': 'None'
        }
        return json.dumps(output_data, indent=2)
    else:
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
    Output('sample-info', 'children'),
    Input('selectedExample-store', 'data')
)
def create_exampleInfo(data):

    mol_array = data['molecule'][0]
    mol_dict = {'ID':mol_array[0],
        'Mutagenic':mol_array[5],
        'logP':mol_array[3],
        'ind1':mol_array[4]
    }
    return html.Pre(json.dumps(mol_dict, indent=2))

@app.callback(
    Output('node-info', 'children'),
    Input('node-store', 'data')
)
def create_nodeInfo(data):
    if data:
        # convert string to json (needs fixing)
        node_dict = json.loads(data) 
        return html.Pre(json.dumps(node_dict, indent=2))


if __name__ == '__main__':
    app.run_server(debug=True)