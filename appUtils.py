import pandas as pd

def fetch_mutag_arrays(exampleNum):
    molecule_df = pd.read_csv('/Users/fl20994/Documents/IAI_CDT/Research_Project/XIML_ILP/rAIMEE/data/mutag188/molecule.csv')
    atom_df = pd.read_csv('/Users/fl20994/Documents/IAI_CDT/Research_Project/XIML_ILP/rAIMEE/data/mutag188/atoms.csv')
    bond_df = pd.read_csv('/Users/fl20994/Documents/IAI_CDT/Research_Project/XIML_ILP/rAIMEE/data/mutag188/bond.csv')
    mol_array = molecule_df[molecule_df['molecule_id']==f'd{exampleNum}'].values.tolist()
    bond_df['molecule_id'] = [id.split('_')[0] for id in bond_df['atom1_id']]
    bond_array = bond_df[bond_df['molecule_id']==f'd{exampleNum}'].values.tolist()
    atom_array = atom_df[atom_df['molecule_id']==f'd{exampleNum}'].values.tolist()

    return mol_array, bond_array, atom_array

