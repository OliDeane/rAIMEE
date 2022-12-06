import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, Dash, dcc
from dash_bootstrap_components._components.Container import Container

app = Dash(external_stylesheets=[dbc.themes.JOURNAL])
# app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#app = Dash(external_stylesheets=[dbc.themes.SKETCHY])

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

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

intro = html.Div([
    html.H3("Introduction"),
    html.P("Placeholder text for introduction page")
])

induced_rules = html.Div([

    dbc.Row([
        dbc.Col([
            html.Div(
                html.P(
                    children=["Model Information",
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    "Dataset Information"
                    ],
                    className="menu-title"
                ),
                style={'margin-top':'40px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                    'margin-left':'20px', 'margin-right':'0px', 'margin-bottom': '24px', 'width':535, 'height':212},
            ),
            html.Div(
            html.P(
                children=["Generated Rules By Class",
                "Dataset Information"
                ],
                className="menu-title"
            ),
            style={'margin-top':'40px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                'margin-left':'20px', 'margin-right':'0px', 'width':535, 'height':626},
        ),
        ]),
        
        dbc.Col([
            html.Div(
            html.P(
                children=["Generated Rules By Class",
                "Dataset Information"
                ],
                className="menu-title"
            ),
            style={'margin-top':'40px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                'margin-right':'20px', 'margin-bottom': '24px', 'width':1070, 'height':626},
        ),
        ])
    ])
])



PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


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

# add callback for toggling the collapse on small screens
app.layout = html.Div([
    html.Div(navbar),
    html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Introduction', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Dataset Overview', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Induced Rules', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Model Editer', value='tab-4', style=tab_style, selected_style=tab_selected_style),
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
        return html.Div([
            html.H3('Dataset Overview (Placeholder)')
        ])
    elif tab == 'tab-3':
        return induced_rules
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])


if __name__ == '__main__':
    app.run_server(debug=True)