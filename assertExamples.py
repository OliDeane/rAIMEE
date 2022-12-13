import dash
from dash import html, dcc, Input, Output, dash_table, Dash
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from PIL import Image
import pandas as pd
import numpy as np
import subprocess
from prologUtils import add_constraint

unknownExamples_df = pd.read_csv('posExamples.csv')

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

assertTable = html.Div(
    [
        dash_table.DataTable(
            id="table3",
            columns=[{"name": i, "id": i} for i in unknownExamples_df.columns],
            data=unknownExamples_df.to_dict("records"),
            style_cell={'textAlign':'left'},
            style_data_conditional=style_data_conditional
        ),
    ]
)

assertExamplesCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Assert Examples", className="card-title"),
                html.H6("Add counter examples to guide model learning", className="card-subtitle"),
                assertTable
            ]
        ),
    ],
    style={"margin-top":"1rem", "margin-left":"2rem", "margin-right":"2rem", "width": "50rem", "height":"55rem"}
)

app.layout = html.Div(
    [
        assertExamplesCard
    ]
)

@app.callback(
    Output("table3", "style_data_conditional"),
    [Input("table3", "active_cell")]
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


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
    