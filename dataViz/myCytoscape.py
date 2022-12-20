import json

from dash import Dash, html, Input, Output
import dash_cytoscape as cyto
import pandas as pd
import random
app = Dash(__name__)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

def fetch_mutag_arrays():
    molecule_df = pd.read_csv('/Users/fl20994/Documents/IAI_CDT/Research_Project/XIML_ILP/rAIMEE/data/mutag188/molecule.csv')
    atom_df = pd.read_csv('/Users/fl20994/Documents/IAI_CDT/Research_Project/XIML_ILP/rAIMEE/data/mutag188/atoms.csv')
    bond_df = pd.read_csv('/Users/fl20994/Documents/IAI_CDT/Research_Project/XIML_ILP/rAIMEE/data/mutag188/bond.csv')
    mol_array = molecule_df[molecule_df['molecule_id']=='d1'].values.tolist()
    bond_df['molecule_id'] = [id.split('_')[0] for id in bond_df['atom1_id']]
    bond_array = bond_df[bond_df['molecule_id']=='d1'].values.tolist()
    atom_array = atom_df[atom_df['molecule_id']=='d1'].values.tolist()

    return mol_array, bond_array, atom_array


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
cytoscape_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    }
]



app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-event-callbacks-1',
        layout={'name': 'cose'},
        elements=edges+nodes,
        stylesheet=cytoscape_stylesheet,
        style={'width': '100%', 'height': '450px'}
    ),
    html.Pre(id='cytoscape-tapNodeData-json', style=styles['pre'])
])


@app.callback(Output('cytoscape-tapNodeData-json', 'children'),
              Input('cytoscape-event-callbacks-1', 'tapNodeData'))
def displayTapNodeData(data):
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


if __name__ == '__main__':
    app.run_server(debug=True)