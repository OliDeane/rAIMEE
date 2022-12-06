import dash_bootstrap_components as dbc
from dash import html, Dash

app = Dash(external_stylesheets=[dbc.themes.JOURNAL])
row = html.Div(
    [
        dbc.Row([
            dbc.Col([
                    html.Div(
                        style={'margin-top':'40px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                        'margin-left':'20px', 'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                        ),
                    html.Div(
                        style={'margin-top':'40px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                        'margin-left':'20px', 'margin-right':'20px', 'margin-bottom': '24px', 'width':535, 'height':212},
                        )
                ]),
            
            dbc.Col([
                html.Div(
                        style={'margin-top':'40px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                        'margin-left':'20px', 'margin-right':'20px', 'margin-bottom': '24px', 'width':8000, 'height':424},
                        )
                ])
            
            ])
    ]
)

app.layout = row

if __name__ == '__main__':
    app.run_server(debug=True)

