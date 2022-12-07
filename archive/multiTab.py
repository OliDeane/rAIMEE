import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, Dash, dcc
import dash
from dash_bootstrap_components._components.Container import Container
import plotly.express as px
import subprocess
import numpy as np

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# Instantiate app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# Create placeholder rule coverage figure
df = px.data.gapminder().query("year == 2007")
fig = px.treemap(df, path=[px.Constant("world"), 'continent', 'country'], values='pop',
                  color='lifeExp', hover_data=['iso_alpha'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))
fig.update_layout(margin = dict(t=00, l=0, r=0, b=0), paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)')
fig.update(layout_coloraxis_showscale=False)

# Create styles for tab setup
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

# Add navbar
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

# introduction tab
intro = html.Div([
    html.H3("Introduction"),
    html.P("Placeholder text for introduction page")
])

# Dataset Overview
dataset_overview = html.Div([
    html.Div([
        html.H3("Select Dataset"),
        html.P("Use the toggle to select a preloaded dataset or upload a file.")
    ]),
])

# Rule extraction tab
induced_rules = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div(
                children = [
                    html.P(children=["Induce Model", html.Br()], className="menu-title"),

                    html.Div([
                        dbc.Button('Induce', id = 'induce-button', className='me-2', n_clicks=0),
                        dcc.Store(id='hypothesis-store', data=[], storage_type='memory')
                    ]),

                    html.P(children=[
                        "Model Information",
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        "Dataset Information"
                    ]),
                ],
                className = 'infoBox',
            ),
            html.Div(
                children=[
                    html.P(children=["Generated Rules", html.Br()], className="menu-title"),
                    html.Div(id = 'hypothesis-box', children = []),
                    html.P(children=[html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br()])
                    ],
                className='infoBox'
                )
        ]),
        
        dbc.Col([
            html.Div([
                html.P(
                    children=["Generated Rules By Class"],
                    className="menu-title"
                ),
                dcc.Graph(
                    figure=fig,
                    style={'width':1050, 'height':526}
                    )
                ],
                style={'margin-top':'40px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)', 
                'margin-right':'20px', 'margin-bottom': '24px', 'width':1070, 'height':626},
            ),
        ])
    
    ])
])

compare_model = html.Div([
                    html.H3("Model Comparison ()")
                ])

# Main app layout
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
        return dataset_overview
    elif tab == 'tab-3':
        return induced_rules
    elif tab == 'tab-4':
        return compare_model

@app.callback(
    dash.dependencies.Output('hypothesis-store', 'data'),
    [dash.dependencies.Input('induce-button', 'n_clicks')])
def induce_onClick(n_clicks):
    
    if not n_clicks:
        return dash.no_update

    result = subprocess.check_output('python inferenceScript.py', shell=True)  
    theory = subprocess.check_output('python hypothesisScript.py', shell=True)
    
    # convert bytes to string
    output = theory.decode()  
    print(output)
    returnable = {'hypothesis':output}
    # return output
    return returnable

@app.callback(
    Output('hypothesis-box', 'children'),
    Input('hypothesis-store', 'data')
)
def create_hypothesis(data):
    print(type(data))
    print(data)
    hypothesis_text = data["hypothesis"]
    print(hypothesis_text)

    return html.P(children=[
        f"{hypothesis_text}"
    ])


if __name__ == '__main__':
    app.run_server(debug=True)