import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc, Dash

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


dataset_button_group = html.Div(
    [
        dbc.RadioItems(
            id="radios",
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
        html.H4("Mutagenesis Dataset", className="card-title"),
        html.H6("The dataset comprises of 188 molecules trialed for mutagenicity on Salmonella typhimurium.",
            className="card-subtitle", style={"margin-bottom":"rem"}),
        dataset_button_group
    ]
)

app.layout = html.Div([
    presentDataCard
])

@app.callback(Output("output", "children"), [Input("radios", "value")])
def display_data_table(value):
    mutagDf = pd.read_csv(f"./data/mutag188/Mutag188_{value}.csv")
    return html.Div(
        [
             dbc.Table.from_dataframe(mutagDf.head(5), striped=True, bordered=True, hover=True)
        ],
        style={"margin-top":"1rem", "margin-left":"1rem", "margin-right":"1rem"},
    )
       
    
if __name__ == '__main__':
    app.run_server(debug=True)
