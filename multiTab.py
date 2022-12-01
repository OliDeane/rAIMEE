from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


app = Dash(__name__)
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

navbar = dbc.Navbar(
    dbc.Container(
        [html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("RAIMEE", className="ms-2")),
                    ],
                    align="left",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
        ],
        fluid=True
    ),
    color="dark",
    dark=True,
)


app.layout = html.Div([
    html.Div(navbar),
    html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Tab 1', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab 2', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab 3', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab 4', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
    ])
])

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])


if __name__ == '__main__':
    app.run_server(debug=True)