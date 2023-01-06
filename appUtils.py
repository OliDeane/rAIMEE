import pandas as pd
import plotly.express as px
from dash import html

def fetch_mutag_arrays(exampleNum):
    molecule_df = pd.read_csv('/Users/fl20994/Documents/IAI_CDT/Research_Project/XIML_ILP/rAIMEE/data/mutag188/molecule.csv')
    atom_df = pd.read_csv('/Users/fl20994/Documents/IAI_CDT/Research_Project/XIML_ILP/rAIMEE/data/mutag188/atoms.csv')
    bond_df = pd.read_csv('/Users/fl20994/Documents/IAI_CDT/Research_Project/XIML_ILP/rAIMEE/data/mutag188/bond.csv')
    mol_array = molecule_df[molecule_df['molecule_id']==f'd{exampleNum}'].values.tolist()
    bond_df['molecule_id'] = [id.split('_')[0] for id in bond_df['atom1_id']]
    bond_array = bond_df[bond_df['molecule_id']==f'd{exampleNum}'].values.tolist()
    atom_array = atom_df[atom_df['molecule_id']==f'd{exampleNum}'].values.tolist()

    return mol_array, bond_array, atom_array


# Create placeholder rule coverage figure
def generate_coverageGraph(data_path="coverageData.csv"):
    '''Creates placeholder rule coverage figure'''
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
    '''Cleans hypothesis list'''
    hyp_list = hypothesis_text[1:-2].split(".',")
    
    result = []
    for idx, rule in enumerate(hyp_list):
        result.append(f'R{idx}: {rule}')
        result.append(html.P(html.Br()))

    return result

